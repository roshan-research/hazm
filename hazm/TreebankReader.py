# coding: utf8

from __future__ import unicode_literals, print_function
import os, sys, re, codecs
from xml.dom import minidom
from nltk.tree import Tree
from .Chunker import tree2brackets


def coarse_pos(tags):
	"""
	Coarse POS tags of Treebank corpus:
		N: Noun, V: Verb, A: Adjective, D: Adverb, Z: Pronoun, T: Determiner, E: Preposition, P: Postposition, U: Number, J: Conjunction, O: Punctuation, R: Residual, L: Classifier, I: Interjection

	>>> coarse_pos(['Nasp---', 'pers', 'prop'])
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
		return map[tags[0][0]]
	except Exception:
		return ''


def coarse_pos_e(tags):
	"""
	Coarse POS tags plus Ezafe.
	Asghari, H., Maleki, J., & Faili, H. (2014). A Probabilistic Approach to Persian Ezafe Recognition. In EACL 2014.

	>>> coarse_pos_e(['Ncsp--z', 'ezafe'])
	'Ne'
	"""

	return coarse_pos(tags) + ('e' if 'ezafe' in tags else '')


class TreebankReader():
	"""
	interfaces [Per­si­an Tree­bank](http://hpsg.fu-berlin.de/~ghayoomi/PTB.html)
	"""

	def __init__(self, root='corpora/treebank', pos_map=coarse_pos_e):
		self._root = root
		self._pos_map = pos_map

	def docs(self):
		for root, dirs, files in os.walk(self._root):
			for name in sorted(files):
				try:
					raw = codecs.open(os.path.join(root, name), encoding='utf8').read();
					raw = re.sub(r'\n *', '', raw)
					yield minidom.parseString(raw.encode('utf8'))
				except Exception as e:
					print('error in reading', name, e, file=sys.stderr)

	def trees(self):
		"""
		>>> print(next(treebank.trees()))
		(S
		  (VPS
		    (NPC (N دنیای/Ne) (MN (N آدولف/N) (N بورن/N)))
		    (VPC
		      (NPC (N دنیای/Ne) (NPA (N اتفاقات/Ne) (ADJ رویایی/AJ)))
		      (V است/V)))
		  (PUNC ./PUNC))
		"""

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

			if not len(node.childNodes):
				return
			first = node.childNodes[0]
			if first.tagName == 'w':
				pos=extract_tags(first)
				return Tree(node.tagName, [(first.childNodes[0].data, self._pos_map(pos))])
			childs = node.childNodes[2:] if node.tagName == 'S' else node.childNodes
			for child in childs:
				if not len(child.childNodes):
					childs.remove(child)
			return Tree(node.tagName, map(traverse, childs))

		for doc in self.docs():
			for S in doc.getElementsByTagName('S'):
				yield traverse(S)

	def sents(self):
		"""
		>>> next(treebank.sents())
		[('دنیای', 'Ne'), ('آدولف', 'N'), ('بورن', 'N'), ('دنیای', 'Ne'), ('اتفاقات', 'Ne'), ('رویایی', 'AJ'), ('است', 'V'), ('.', 'PUNC')]
		"""

		for tree in self.trees():
			yield tree.leaves()


	def chunked_trees(self):
		"""
		>>> tree2brackets(next(treebank.chunked_trees()))
		'[دنیای آدولف بورن NP] [دنیای اتفاقات رویایی NP] [است VP] .'
		"""

		collapse = lambda node, label: Tree(label, [Tree(pos[1], [pos[0]]) for pos in node.pos()])

		def traverse(node, parent, chunks):
			label = node.label()

			if label.count('-nid') > 0:
				label = label.replace('-nid', '')
			if label.count('-nid') > 0:
				label = label.replace('-nid', '')
			if label.count('-DiscA') > 0:
				label = label.replace('-DiscA', '')

			if label == 'CLITIC':
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

			if label in {'CONJ', 'PUNC'}:
				chunks.append(node)
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

			if label in {'NPC', 'N', 'INFV', 'DPA', 'CLASS', 'DPC', 'DEM', 'INTJ', 'MN', 'PRON', 'DET', 'NUM'}:
				chunks.append(collapse(node, 'NP'))
				return

			if label == 'NPA' and len(node) >= 2:
				if node[0].label() == 'ADJ' and node[1].label() == 'NPC' or node[0].label() in {'N', 'PRON'} and node[1].label() in {'ADJ', 'N'} or node[0].label() == 'NUM' and node[1].label() in {'N', 'NPC', 'NPA', 'MN', 'NUM'} or node[0].label() in {'N', 'NPC', 'NPA', 'MN'} and node[1].label() == 'NUM' or node[0].label() == 'NPC' and node[1].label() == 'ADJ':
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

			if label in {'MV', 'V', 'AUX'}:
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
