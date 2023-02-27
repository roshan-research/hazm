# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ PerDT است.

PerDT حاوی تعداد قابل‌توجهی جملۀ برچسب‌خورده با اطلاعات نحوی و ساخت‌واژی است.

"""

from __future__ import unicode_literals
import codecs
from nltk.tree import Tree
from conllu import *


def coarse_pos_e(tags):
    """برچسب‌های ریز را به برچسب‌های درشت (coarse-grained pos tags) تبدیل می‌کند.
    
    Examples:
        >>> coarse_pos_e(['N', 'IANM'])
        'N'
    
    """

    map = {
        "NOUN": "N",
        "VERB": "V",
        "ADJ": "AJ",
        "ADV": "ADV",
        "PRON": "PRO",        
        "ADP": "P",
        "DET":"DET",
        "ADP": "POSTP",     
        "CCONJ": "CONJ",
        "PUNCT": "PUNC",
        "SCONJ": "CONJ",
    }
    x=map.get(tags[0], "X")
    return map.get(tags[0], "X") + ("e" if "EZ" in tags else "")


word_nodes = lambda tree: sorted(tree, key=lambda node: node["id"])
node_deps = lambda node: sum(node["deps"].values(), [])


class DadeganReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ PerDT است.
    
    Args:
        conll_file(str): مسیر فایلِ پیکره.
        pos_map(str,optionl): دیکشنری مبدل برچسب‌های ریز به درشت.
    
    """

    def __init__(self, conll_file, pos_map=coarse_pos_e):
        self._conll_file = conll_file
        self._pos_map = pos_map if pos_map else lambda tags: ",".join(tags)

    def _sentences(self):
        """جملات پیکره را به شکل متن خام برمی‌گرداند.
        
        Yields:
            (str): جملهٔ بعدی.
        
        """
        with codecs.open(self._conll_file, encoding="utf8") as conll_file:
            text = conll_file.read()

            # refine text
            text = (
                text.replace("‌‌", "‌")
                .replace("\t‌", "\t")
                .replace("‌\t", "\t")
                .replace("\t ", "\t")
                .replace(" \t", "\t")
                .replace("\r", "")
                .replace("\u2029", "‌")
            )

            for item in text.replace(" ", "_").split("\n\n"):
                if item.strip():
                    yield item

    def trees(self):
        """ساختار درختی جملات را برمی‌گرداند.
        
        Yields:
            (str): ساختار درختی جملهٔ بعدی.
        
        """
        
        with open(self._conll_file,"r",encoding="utf-8") as conllu:                            
            for sent in parse(conllu.read()):                
                for node in word_nodes(sent):
                    node["mtag"] = [node["upos"], node["xpos"]]
                    if node["feats"] is not None:
                        if "ezafe" in node["feats"]:
                            node["mtag"].append("EZ")

                    node["mtag"] = self._pos_map(node["mtag"])

                yield sent.to_tree()

    def sents(self):
        """لیستی از جملات را برمی‌گرداند.
        
        هر جمله لیستی از `(توکن، برچسب)`ها است.
        
        Examples:
            >>> dadegan = DadeganReader(conll_file='corpora/dadegan.conll')
            >>> next(dadegan.sents())
            [('این', 'DET'), ('میهمانی', 'N'), ('به', 'P'), ('منظور', 'Ne'), ('آشنایی', 'Ne'), ('هم‌تیمی‌های', 'Ne'), ('او', 'PRO'), ('با', 'P'), ('غذاهای', 'Ne'), ('ایرانی', 'AJ'), ('ترتیب', 'N'), ('داده_شد', 'V'), ('.', 'PUNC')]
        
        Yields:
            (List[Tuple[str,str]]): جملهٔ بعدی.
        
        """
        with open(self._conll_file,"r",encoding="utf-8") as conllu:  
            text = conllu.read()
            for sent in parse(text):
                for node in word_nodes(sent):
                    node["mtag"] = [node["upos"], node["xpos"]]
                    if node["feats"] is not None:
                        if "ezafe" in node["feats"]:
                            node["mtag"].append("EZ")

                    node["mtag"] = self._pos_map(node["mtag"])        
                yield [(node["form"], node["mtag"]) for node in word_nodes(sent)]

    
    def chunked_trees(self):
        """درخت وابستگی‌های جملات را برمی‌گرداند.
        
        Examples:
            >>> from hazm.Chunker import tree2brackets
            >>> tree2brackets(next(dadegan.chunked_trees()))
            '[این میهمانی NP] [به PP] [منظور آشنایی هم‌تیمی‌های او NP] [با PP] [غذاهای ایرانی NP] [ترتیب داده_شد VP] .'
        
        Yields:
            (str): درخت وابستگی‌های جملهٔ بعدی.
        
        """
        with open(self._conll_file,"r",encoding="utf-8") as conllu:                            
            for sent in parse(conllu.read()):
                chunks = []
                for node in word_nodes(sent):
                    node["mtag"] = [node["upos"], node["xpos"]]
                    if node["feats"] is not None:
                        if "ezafe" in node["feats"]:
                            node["mtag"].append("EZ")

                    node["mtag"] = self._pos_map(node["mtag"]) 
                    n = node["id"]
                    item = (node["form"], node["mtag"])
                    appended = False                    
                    if node["upos"] in {"ADP"}:
                        if node_deps(node) is not None:                        
                            for d in node_deps(node):
                                label = "PP"
                                if node["upos"] == "ADP":
                                    label = "ADP"
                                if (
                                    d == n - 1
                                    and type(chunks[-1]) == Tree
                                    and chunks[-1].label() == label
                                ):
                                    chunks[-1].append(item)
                                    appended = True
                        if (
                            node["head"] == n - 1
                            and len(chunks) > 0
                            and type(chunks[-1]) == Tree
                            and chunks[-1].label() == label
                        ):
                            chunks[-1].append(item)
                            appended = True
                        if not appended:
                            chunks.append(Tree(label, [item]))
                    elif node["upos"] in {"PUNCT", "CCONJ", "SCONJ", "PART"}:
                        if (
                            item[0]
                            in {"'", '"', "(", ")", "{", "}", "[", "]", "-", "#", "«", "»"}
                            and len(chunks) > 0
                            and type(chunks[-1]) == Tree
                        ):
                            for l in chunks[-1].leaves():
                                if l[1] == item[1]:
                                    chunks[-1].append(item)
                                    appended = True
                                    break
                        if appended is not True:
                            chunks.append(item)
                    elif node["upos"] in {
                        "NOUN",
                        "DET",
                        "ADJ",
                        "PRON",
                        "INTJ",
                        "NUM",
                        "PROPN",                   
                    }:
                        if node["deprel"] in {"nmod", "amod"}:
                            if len(chunks) > 0:
                                if type(chunks[-1]) == Tree:
                                    j = n - len(chunks[-1].leaves())
                                    chunks[-1].append(item)
                                else:
                                    j = n - 1
                                    treeNode = Tree("NP", [chunks.pop(), item])
                                    chunks.append(treeNode)
                                while j > node["head"]:
                                    leaves = chunks.pop().leaves()
                                    if len(chunks) < 1:
                                        chunks.append(Tree("NP", leaves))
                                        j -= 1
                                    elif type(chunks[-1]) == Tree:
                                        j -= len(chunks[-1])
                                        for l in leaves:
                                            chunks[-1].append(l)
                                    else:
                                        leaves.insert(0, chunks.pop())
                                        chunks.append(Tree("NP", leaves))
                                        j -= 1
                                continue
                        elif node["deprel"] == "POSDEP" and tree.nodes[node["head"]][
                            "deprel"
                        ] in {"NCONJ", "AJCONJ"}:
                            conj = tree.nodes[node["head"]]
                            if tree.nodes[conj["head"]]["deprel"] in {
                                "MOZ",
                                "NPOSTMOD",
                                "AJCONJ",
                                "POSDEP",
                            }:
                                label = "NP"
                                leaves = [item]
                                j = n - 1
                                while j >= conj["head"]:
                                    if type(chunks[-1]) is Tree:
                                        j -= len(chunks[-1].leaves())
                                        label = chunks[-1].label()
                                        leaves = chunks.pop().leaves() + leaves
                                    else:
                                        leaves.insert(0, chunks.pop())
                                        j -= 1
                                chunks.append(Tree(label, leaves))
                                appended = True
                        elif (
                            node["head"] == n - 1
                            and len(chunks) > 0
                            and type(chunks[-1]) == Tree
                            and not chunks[-1].label() == "PP"
                        ):
                            chunks[-1].append(item)
                            appended = True
                        elif node["deprel"] == "AJCONJ" and tree.nodes[node["head"]][
                            "deprel"
                        ] in {"NPOSTMOD", "AJCONJ"}:
                            np_nodes = [item]
                            label = "ADJP"
                            i = n - node["head"]
                            while i > 0:
                                if type(chunks[-1]) == Tree:
                                    label = chunks[-1].label()
                                    leaves = chunks.pop().leaves()
                                    i -= len(leaves)
                                    np_nodes = leaves + np_nodes
                                else:
                                    i -= 1
                                    np_nodes.insert(0, chunks.pop())
                            chunks.append(Tree(label, np_nodes))
                            appended = True
                        elif (
                            node["upos"] == "ADJ"
                            and node["deprel"] == "POSDEP"
                            and tree.nodes[node["head"]]["ctag"] != "CONJ"
                        ):
                            np_nodes = [item]
                            i = n - node["head"]
                            while i > 0:
                                label = "ADJP"
                                if type(chunks[-1]) == Tree:
                                    label = chunks[-1].label()
                                    leaves = chunks.pop().leaves()
                                    i -= len(leaves)
                                    np_nodes = leaves + np_nodes
                                else:
                                    i -= 1
                                    np_nodes.insert(0, chunks.pop())
                            chunks.append(Tree(label, np_nodes))
                            appended = True
                        if node_deps(node) is not None: 
                            for d in node_deps(node):
                                if (
                                    d == n - 1
                                    and type(chunks[-1]) == Tree
                                    and chunks[-1].label() != "PP"
                                    and appended is not True
                                ):
                                    label = chunks[-1].label()
                                    if node["deprel"] == "ADV":
                                        label = "ADVP"
                                    elif label in {"ADJP", "ADVP"}:
                                        if node["upos"] == "N":
                                            label = "NP"
                                        elif node["upos"] == "ADJ":
                                            label = "ADJP"
                                    leaves = chunks.pop().leaves()
                                    leaves.append(item)
                                    chunks.append(Tree(label, leaves))
                                    appended = True
                                elif tree.nodes[d]["deprel"] == "NPREMOD" and appended is not True:
                                    np_nodes = [item]
                                    i = n - d
                                    while i > 0:
                                        if type(chunks[-1]) == Tree:
                                            leaves = chunks.pop().leaves()
                                            i -= len(leaves)
                                            np_nodes = leaves + np_nodes
                                        else:
                                            i -= 1
                                            np_nodes.insert(0, chunks.pop())
                                    chunks.append(Tree("NP", np_nodes))
                                    appended = True
                        if not appended:
                            label = "NP"
                            if node["upos"] == "ADJ":
                                label = "ADJP"
                            elif node["deprel"] == "ADV":
                                label = "ADVP"
                            chunks.append(Tree(label, [item]))
                    elif node["upos"] in {"V"}:
                        appended = False
                        if node_deps(node) is not None: 
                            for d in node_deps(node):
                                if (
                                    d == n - 1
                                    and type(chunks[-1]) == Tree
                                    and tree.nodes[d]["deprel"] in {"NVE", "ENC"}
                                    and appended is not True
                                ):
                                    leaves = chunks.pop().leaves()
                                    leaves.append(item)
                                    chunks.append(Tree("VP", leaves))
                                    appended = True
                                elif tree.nodes[d]["deprel"] in {"VPRT", "NVE"}:
                                    vp_nodes = [item]
                                    i = n - d
                                    while i > 0:
                                        if type(chunks[-1]) == Tree:
                                            leaves = chunks.pop().leaves()
                                            i -= len(leaves)
                                            vp_nodes = leaves + vp_nodes
                                        else:
                                            i -= 1
                                            vp_nodes.insert(0, chunks.pop())
                                    chunks.append(Tree("VP", vp_nodes))
                                    appended = True
                                    break
                        if not appended:
                            chunks.append(Tree("VP", [item]))
                    elif node["upos"] in {"PSUS"}:
                        if node["deprel"] == "ADV":
                            chunks.append(Tree("ADVP", [item]))
                        else:
                            chunks.append(Tree("VP", [item]))
                    elif node["upos"] in {"ADV", "SADV"}:
                        appended = False
                        if node_deps(node) is not None: 
                            for d in node_deps(node):
                                if d == n - 1 and type(chunks[-1]) == Tree:
                                    leaves = chunks.pop().leaves()
                                    leaves.append(item)
                                    chunks.append(Tree("ADVP", leaves))
                                    appended = True
                        if not appended:
                            chunks.append(Tree("ADVP", [item]))

                yield Tree("S", chunks)
