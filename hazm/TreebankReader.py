# coding: utf-8

from __future__ import unicode_literals, print_function
import os, sys, re, codecs
from xml.dom import minidom
from nltk.tree import Tree
from .WordTokenizer import WordTokenizer


def coarse_pos_e(tags):
	"""
	Coarse POS tags of Treebank corpus:
		N: Noun, V: Verb, A: Adjective, D: Adverb, Z: Pronoun, T: Determiner, E: Preposition, P: Postposition, U: Number, J: Conjunction, O: Punctuation, R: Residual, L: Classifier, I: Interjection

	>>> coarse_pos_e(['Nasp---', 'pers', 'prop'])
	'N'
	"""

	map = {'N': 'N', 'V': 'V', 'A': 'AJ', 'D': 'ADV', 'Z': 'PRO', 'T': 'DET', 'E': 'P', 'P': 'POSTP', 'U': 'NUM', 'J': 'CONJ', 'O': 'PUNC', 'R': 'RES', 'L': 'CL', 'I': 'INT'}
	try:
		if tags[0][0] == 'C':
			if 'pronominal' in tags:
				tags[0] = 'Z'
			elif 'verb' in tags:
				tags[0] = 'V'
			elif 'prep' in tags:
				tags[0] = 'E'
			elif 'adv' in tags:
				tags[0] = 'D'
			elif 'det' in tags:
				tags[0] = 'T'
		return map[tags[0][0]] + ('e' if 'ezafe' in tags else '')
	except Exception:
		return ''


class TreebankReader():
	"""
	interfaces [Per­si­an Tree­bank](http://hpsg.fu-berlin.de/~ghayoomi/PTB.html)

	>>> treebank = TreebankReader(root='corpora/treebank')
	>>> print(next(treebank.trees()))
	(S
	  (VPS
	    (NPC (N دنیای/Ne) (MN (N آدولف/N) (N بورن/N)))
	    (VPC
	      (NPC (N دنیای/Ne) (NPA (N اتفاقات/Ne) (ADJ رویایی/AJ)))
	      (V است/V)))
	  (PUNC ./PUNC))

	>>> next(treebank.sents())
	[('دنیای', 'Ne'), ('آدولف', 'N'), ('بورن', 'N'), ('دنیای', 'Ne'), ('اتفاقات', 'Ne'), ('رویایی', 'AJ'), ('است', 'V'), ('.', 'PUNC')]

	>>> from .Chunker import tree2brackets
	>>> tree2brackets(next(treebank.chunked_trees()))
	'[دنیای آدولف بورن NP] [دنیای اتفاقات رویایی NP] [است VP] .'
	"""

	def __init__(self, root, pos_map=coarse_pos_e, join_clitics=False, join_verb_parts=False):
		self._root = root
		self._pos_map = pos_map if pos_map else lambda tags: ','.join(tags)
		self._join_clitics = join_clitics
		self._join_verb_parts = join_verb_parts
		self._tokenizer = WordTokenizer()

	def docs(self):
		for root, dirs, files in os.walk(self._root):
			for name in sorted(files):
				try:
					with codecs.open(os.path.join(root, name), encoding='utf8') as treebank_file:
						raw = re.sub(r'\n *', '', treebank_file.read())
						yield minidom.parseString(raw.encode('utf8'))
				except Exception as e:
					print('error in reading', name, e, file=sys.stderr)

	def trees(self):

		def traverse(node):
			def extract_tags(W):
				pos = [W.getAttribute('lc') if W.getAttribute('lc') else None]
				if W.getAttribute('clitic') in {'ezafe', 'pronominal', 'verb', 'prep', 'adv', 'det'}:
					pos.append(W.getAttribute('clitic'))
				if W.getAttribute('ne_sort'):
					pos.append(W.getAttribute('ne_sort'))
				if W.getAttribute('n_type'):
					pos.append(W.getAttribute('n_type'))
				if W.getAttribute('ya_type'):
					pos.append(W.getAttribute('ya_type'))
				if W.getAttribute('ke_type'):
					pos.append(W.getAttribute('ke_type'))
				if W.getAttribute('type'):
					pos.append(W.getAttribute('type'))
				if W.getAttribute('kind'):
					pos.append(W.getAttribute('kind'))
				return pos

			def clitic_join(tree, clitic):
				if type(tree[-1]) == Tree:
					return clitic_join(tree[-1], clitic)
				else:
					if(clitic[0][0][0] == 'ا'):
						clitic[0] = ('‌' + clitic[0][0], clitic[0][1])
					tree[-1]=(tree[-1][0] + clitic[0][0], clitic[0][1])
					tree.set_label('CLITICS')
					return

			if not len(node.childNodes):
				return
			first = node.childNodes[0]
			if first.tagName == 'w':
				pos=extract_tags(first)
				return Tree(node.tagName, [(first.childNodes[0].data.replace('می ', 'می‌'), self._pos_map(pos))])
			childs = node.childNodes[2:] if node.tagName == 'S' else node.childNodes
			for child in childs:
				if not len(child.childNodes):
					childs.remove(child)
			tree = Tree(node.tagName, map(traverse, childs))
			if self._join_clitics and len(tree) > 1 and type(tree[1]) == Tree and tree[1].label() == 'CLITIC' and tree[1][0][1] not in {'P', 'V'}:
				clitic=tree[-1]
				tree = Tree(tree.label(), [subtree for subtree in tree[0]])
				clitic_join(tree, clitic)
			if self._join_verb_parts and len(tree) > 1 and type(tree[1]) == Tree and type(tree[0]) == Tree and tree[0].label() == 'AUX' and tree[0][0][0] in self._tokenizer.before_verbs:
				tree[1][0] = (tree[0][0][0] + ' ' + tree[1][0][0], tree[1][0][1])
				tree.remove(tree[0])
			if self._join_verb_parts and len(tree.leaves()) > 1 and tree.leaves()[-1][0] in self._tokenizer.after_verbs and tree.leaves()[-2][0] in self._tokenizer.verbe :
				tree[1][0] = (tree[0].leaves()[-1][0] + ' ' + tree[1][0][0], tree[1][0][1])
				path = tree.leaf_treeposition(len(tree.leaves())-2)
				removingtree = tree
				while len(path) > 2 :
					removingtree = removingtree[path[0]]
					path = path[1:]
				removingtree.remove(Tree(tree.pos()[-2][1],[tree.pos()[-2][0]]))
			if self._join_verb_parts and len(tree.leaves()) > 1 and tree.leaves()[-1][0] in self._tokenizer.after_verbs and tree.leaves()[-2][0] in self._tokenizer.verbe :
				tree[1][0] = (tree[0].leaves()[-1][0] + ' ' + tree[1][0][0], tree[1][0][1])
				path = tree.leaf_treeposition(len(tree.leaves())-2)
				removingtree = tree
				while len(path) > 2 :
					removingtree = removingtree[path[0]]
					path = path[1:]
				removingtree.remove(Tree(tree.pos()[-2][1],[tree.pos()[-2][0]]))
			return tree

		for doc in self.docs():
			for S in doc.getElementsByTagName('S'):
				yield traverse(S)

	def sents(self):
		for tree in self.trees():
			yield tree.leaves()


	def chunked_trees(self):
		collapse = lambda node, label: Tree(label, [Tree(pos[1], [pos[0]]) for pos in node.pos()])

		def traverse(node, parent, chunks):
			label = node.label()

			if label.count('-nid') > 0:
				label = label.replace('-nid', '')
			if label.count('-nid') > 0:
				label = label.replace('-nid', '')
			if label.count('-DiscA') > 0:
				label = label.replace('-DiscA', '')

			if label in {'CLITIC', 'CLITICS'}:
				if node[0][1] == 'V':
					label = 'V'
				elif node[0][1] == 'P':
					label = 'PREP'
				elif node[0][1] == 'DET':
					label = 'DET'
				elif node[0][1] == 'ADV':
					label = 'ADV'
				elif node[0][1] == 'PRO':
					label = 'PRON'

			if label in {'CONJ', 'PUNC'} and len(node) == 1:
				chunks.append(node)
				return

			if label == 'PPC' and len(node) == 1:
				chunks.append(Tree('PP', [node[0]]))
				return

			if label == 'PREP':
				chunks.append(Tree('PP', [node]))
				return

			if label == 'PostP':
				chunks.append(Tree('POSTP', [node]))
				return

			for leaf in node.pos():
				if leaf[1] in {'PUNC', 'CONJ', 'PREP', 'PostP'}:
					for i in range(len(node)):
						traverse(node[i], node, chunks)
					return

			if label == 'NPA' and parent.label() in {'CPC', 'PPC'}:
				chunks.append(collapse(node, 'NP'))
				return

			if label == 'NPA' and len(node)>=1:
				if node[0].label() == 'ADV':
					chunks.append(collapse(node, 'NP'))
					return

			if label in {'NPC', 'N', 'INFV', 'DPA', 'CLASS', 'DPC', 'DEM', 'INTJ', 'MN', 'PRON', 'DET', 'NUM', 'RES'}:
				chunks.append(collapse(node, 'NP'))
				return

			if label == 'NPA' and len(node) >= 2:
				if node[0].label() == 'ADJ' and node[1].label() == 'NPC' or node[0].label() in {'N', 'PRON'} and node[1].label() in {'ADJ', 'ADJPA', 'N'} or node[0].label() == 'NUM' and node[1].label() in {'N', 'NPC', 'MN', 'NUM'} or node[0].label() in {'N', 'NPC', 'MN'} and node[1].label() == 'NUM' or node[0].label() == 'NPC' and node[1].label() == 'ADJ' or node[0].label() == 'NPA' and node[1].label() != 'NPC' or node[1].label() == 'NPA' and node[0].label() != 'NPC':
					chunks.append(collapse(node, 'NP'))
					return

			if label == 'DPC' and len(node) >= 2:
				chunkable = True
				for leaf in node[1].pos():
					if leaf[1] in {'PUNC', 'CONJ', 'PREP', 'PostP'}:
						chunkable = False
				if node[1].label() in {'N', 'NPA', 'NPC'} and chunkable:
					chunks.append(collapse(node, 'NP'))
					return

			if label == 'DPA' and len(node)>=2:
				if node[1].label() == 'ADV':
					chunks.append(collapse(node, 'ADVP'))
					return

			if label in {'MV', 'V', 'AUX', 'PPARV'}:
				chunks.append(Tree('VP', [node]))
				return

			if label in {'ADJ', 'ADJPC', 'MADJ', 'ADVPA'}:
				chunks.append(Tree('ADJP', [node]))
				return

			if label in {'ADV', 'MADV', 'ADVPC'}:
				chunks.append(Tree('ADVP', [node]))
				return

			if type(node[0]) != Tree:
				chunks.append(node)
				return

			for i in range(len(node)):
				traverse(node[i], node, chunks)

		for tree in self.trees():
			chunks = []
			traverse(tree, None, chunks)
			for i in range(len(chunks)):
				if chunks[i].label() in {'PUNC', 'CONJ'}:
					chunks[i] = chunks[i][0]
				else:
					chunks[i] = Tree(chunks[i].label(), chunks[i].leaves())
			yield Tree('S', chunks)
