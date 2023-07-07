"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ PerDT است.

PerDT حاوی تعداد قابل‌توجهی جملۀ برچسب‌خورده با اطلاعات نحوی و ساخت‌واژی است.

"""
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Tuple
from typing import Type

from nltk.parse import DependencyGraph
from nltk.tree import Tree


def coarse_pos_u(tags: List[str], word: str) -> str:
    """برچسب‌های ریز را به برچسب‌های درشت منطبق با استاندارد جهانی (coarse-grained
    universal pos tags) تبدیل می‌کند.

    Examples:
        >>> coarse_pos_e(['N', 'IANM'], 'امروز')
        'N'

    """
    mapping = {
        "N": "NOUN",
        "V": "VERB",
        "ADJ": "ADJ",
        "ADV": "ADV",
        "PR": "PRON",
        "PREM": "DET",
        "PREP": "ADP",
        "POSTP": "ADP",
        "PRENUM": "NUM",
        "CONJ": "CCONJ",
        "PUNC": "PUNCT",
        "SUBR": "SCONJ",
        "IDEN": "PROPN",
        "POSTNUM": "NUM",
        "PSUS": "INTJ",
        "PART": "PART",
        "ADR": "INTJ",
    }
    pos_mapped = mapping.get(tags[0], "X")
    if pos_mapped == "PART" and word == "را":
        return "ADP"
    if pos_mapped == "PART" and word in ["خوب", "آخر"]:
        return "ADP"
    return pos_mapped


def coarse_pos_e(tags: List[str], word) -> str: # noqa: ARG001
    """برچسب‌های ریز را به برچسب‌های درشت (coarse-grained pos tags) تبدیل می‌کند.

    Examples:
        >>> coarse_pos_e(['N', 'IANM'],'امروز')
        'N'

    """
    mapping = {
        "N": "N",
        "V": "V",
        "ADJ": "AJ",
        "ADV": "ADV",
        "PR": "PRO",
        "PREM": "DET",
        "PREP": "P",
        "POSTP": "POSTP",
        "PRENUM": "NUM",
        "CONJ": "CONJ",
        "PUNC": "PUNC",
        "SUBR": "CONJ",
    }
    return mapping.get(tags[0], "X") + ("e" if "EZ" in tags else "")


def word_nodes(tree: Type[Tree]) -> List[Dict[str, Any]]:
    """نودها را به صورت مرتب‌شده برمی‌گرداند."""
    return sorted(tree.nodes.values(), key=lambda node: node["address"])[1:]


def node_deps(node: List[Dict[str, Any]]) -> List[Any]:
    """مقادیر موجود در فیلد deps نود ورودی را برمی‌گرداند."""
    return sum(list(node["deps"].values()), [])


class DadeganReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ PerDT است.

    Args:
        conll_file: مسیر فایلِ پیکره.
        pos_map: دیکشنری مبدل برچسب‌های ریز به درشت.

    """

    def __init__(
        self: "DadeganReader",
        conll_file: str,
        pos_map: str = coarse_pos_e,
        universal_pos: bool = False,
    ) -> None:
        self._conll_file = conll_file
        if pos_map is None:
            self._pos_map = lambda tags: ",".join(tags)
        elif universal_pos:
            self._pos_map = coarse_pos_u
        else:
            self._pos_map = coarse_pos_e

    def _sentences(self: "DadeganReader") -> Iterator[str]:
        """جملات پیکره را به شکل متن خام برمی‌گرداند.

        Yields:
            جملهٔ بعدی.

        """
        with Path(self._conll_file).open(encoding="utf8") as conll_file:
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

    def trees(self: "DadeganReader") -> Iterator[Type[Tree]]:
        """ساختار درختی جملات را برمی‌گرداند.

        Yields:
            ساختار درختی جملهٔ بعدی.

        """
        for sentence in self._sentences():
            tree = DependencyGraph(sentence)

            for node in word_nodes(tree):
                node["mtag"] = [node["ctag"], node["tag"]]

                if "ezafe" in node["feats"]:
                    node["mtag"].append("EZ")

                node["mtag"] = self._pos_map(node["mtag"], node["word"])

            yield tree

    def sents(self: "DadeganReader") -> Iterator[List[Tuple[str, str]]]:
        """لیستی از جملات را برمی‌گرداند.

        هر جمله لیستی از `(توکن، برچسب)`ها است.

        Examples:
            >>> dadegan = DadeganReader(conll_file='dadegan.conll')
            >>> next(dadegan.sents())
            [('این', 'DET'), ('میهمانی', 'N'), ('به', 'P'), ('منظور', 'Ne'), ('آشنایی', 'Ne'), ('هم‌تیمی‌های', 'Ne'), ('او', 'PRO'), ('با', 'P'), ('غذاهای', 'Ne'), ('ایرانی', 'AJ'), ('ترتیب', 'N'), ('داده_شد', 'V'), ('.', 'PUNC')]

        Yields:
            جملهٔ بعدی.

        """
        for tree in self.trees():
            yield [(node["word"], node["mtag"]) for node in word_nodes(tree)]

    def chunked_trees(self: "DadeganReader") -> Iterator[Type[Tree]]:
        """درخت وابستگی‌های جملات را برمی‌گرداند.

        Examples:
            >>> from hazm.chunker import tree2brackets
            >>> dadegan = DadeganReader(conll_file='dadegan.conll')
            >>> tree2brackets(next(dadegan.chunked_trees()))
            '[این میهمانی NP] [به PP] [منظور آشنایی هم‌تیمی‌های او NP] [با PP] [غذاهای ایرانی NP] [ترتیب داده_شد VP] .'

        Yields:
            درخت وابستگی‌های جملهٔ بعدی.

        """
        for tree in self.trees():
            chunks = []
            for node in word_nodes(tree):
                n = node["address"]
                item = (node["word"], node["mtag"])
                appended = False
                if node["ctag"] in {"PREP", "POSTP"}:
                    for d in node_deps(node):
                        label = "PP"
                        if node["ctag"] == "POSTP":
                            label = "POSTP"
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
                elif node["ctag"] in {"PUNC", "CONJ", "SUBR", "PART"}:
                    if (
                        item[0]
                        in {"'", '"', "(", ")", "{", "}", "[", "]", "-", "#", "«", "»"}
                        and len(chunks) > 0
                        and type(chunks[-1]) == Tree
                    ):
                        for leaf in chunks[-1].leaves():
                            if leaf[1] == item[1]:
                                chunks[-1].append(item)
                                appended = True
                                break
                    if appended is not True:
                        chunks.append(item)
                elif node["ctag"] in {
                    "N",
                    "PREM",
                    "ADJ",
                    "PR",
                    "ADR",
                    "PRENUM",
                    "IDEN",
                    "POSNUM",
                    "SADV",
                }:
                    if node["rel"] in {"MOZ", "NPOSTMOD"}:
                        if len(chunks) > 0:
                            if type(chunks[-1]) == Tree:
                                j = n - len(chunks[-1].leaves())
                                chunks[-1].append(item)
                            else:
                                j = n - 1
                                treenode = Tree("NP", [chunks.pop(), item])
                                chunks.append(treenode)
                            while j > node["head"]:
                                leaves = chunks.pop().leaves()
                                if len(chunks) < 1:
                                    chunks.append(Tree("NP", leaves))
                                    j -= 1
                                elif type(chunks[-1]) == Tree:
                                    j -= len(chunks[-1])
                                    for leaf in leaves:
                                        chunks[-1].append(leaf)
                                else:
                                    leaves.insert(0, chunks.pop())
                                    chunks.append(Tree("NP", leaves))
                                    j -= 1
                            continue
                    elif node["rel"] == "POSDEP" and tree.nodes[node["head"]][
                        "rel"
                    ] in {"NCONJ", "AJCONJ"}:
                        conj = tree.nodes[node["head"]]
                        if tree.nodes[conj["head"]]["rel"] in {
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
                        and chunks[-1].label() != "PP"
                    ):
                        chunks[-1].append(item)
                        appended = True
                    elif node["rel"] == "AJCONJ" and tree.nodes[node["head"]][
                        "rel"
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
                        node["ctag"] == "ADJ"
                        and node["rel"] == "POSDEP"
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
                    for d in node_deps(node):
                        if (
                            d == n - 1
                            and type(chunks[-1]) == Tree
                            and chunks[-1].label() != "PP"
                            and appended is not True
                        ):
                            label = chunks[-1].label()
                            if node["rel"] == "ADV":
                                label = "ADVP"
                            elif label in {"ADJP", "ADVP"}:
                                if node["ctag"] == "N":
                                    label = "NP"
                                elif node["ctag"] == "ADJ":
                                    label = "ADJP"
                            leaves = chunks.pop().leaves()
                            leaves.append(item)
                            chunks.append(Tree(label, leaves))
                            appended = True
                        elif tree.nodes[d]["rel"] == "NPREMOD" and appended is not True:
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
                        if node["ctag"] == "ADJ":
                            label = "ADJP"
                        elif node["rel"] == "ADV":
                            label = "ADVP"
                        chunks.append(Tree(label, [item]))
                elif node["ctag"] in {"V"}:
                    appended = False
                    for d in node_deps(node):
                        if (
                            d == n - 1
                            and type(chunks[-1]) == Tree
                            and tree.nodes[d]["rel"] in {"NVE", "ENC"}
                            and appended is not True
                        ):
                            leaves = chunks.pop().leaves()
                            leaves.append(item)
                            chunks.append(Tree("VP", leaves))
                            appended = True
                        elif tree.nodes[d]["rel"] in {"VPRT", "NVE"}:
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
                elif node["ctag"] in {"PSUS"}:
                    if node["rel"] == "ADV":
                        chunks.append(Tree("ADVP", [item]))
                    else:
                        chunks.append(Tree("VP", [item]))
                elif node["ctag"] in {"ADV", "SADV"}:
                    appended = False
                    for d in node_deps(node):
                        if d == n - 1 and type(chunks[-1]) == Tree:
                            leaves = chunks.pop().leaves()
                            leaves.append(item)
                            chunks.append(Tree("ADVP", leaves))
                            appended = True
                    if not appended:
                        chunks.append(Tree("ADVP", [item]))

            yield Tree("S", chunks)
