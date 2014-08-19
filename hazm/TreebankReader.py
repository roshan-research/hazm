# coding: utf8

from __future__ import unicode_literals, print_function
import os, sys, re,codecs
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

	map = {'N': 'N', 'V': 'V', 'A': 'AJ', 'D': 'ADV', 'Z': 'PRO', 'T': 'DET', 'E': 'P', 'P': 'POSTP', 'U': 'NUM', 'J': 'CONJ', 'O': 'PUNC', 'R': 'RES', 'L': 'CL', 'I': 'INT', 'C': 'V'}
	try:
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

	def __init__(self, root='corpora/treebank', pos_map=coarse_pos_e):
		self._root = root
		self._paragraph_pattern = re.compile(r'(\n.{0,50})(?=\n)')
		self._pos_map = pos_map

	def docs(self):
		for root, dirs, files in os.walk(self._root):
			for name in sorted(files):
				try:
					raw = codecs.open(os.path.join(root, name) , encoding='utf8').read();
					raw = re.sub(r'\n *', '', raw)
					yield minidom.parseString(raw.encode('utf8'))
				except Exception as e:
					print('error in reading', name, e, file=sys.stderr)

	def trees(self):
		"""
		>>> next(treebank.trees()).leaves()
		[('دنیای', 'Ne'), ('آدولف', 'N'), ('بورن', 'N'), ('دنیای', 'Ne'), ('اتفاقات', 'Ne'), ('رویایی', 'AJ'), ('است', 'V'), ('.', 'PUNC')]
		"""

		def traverse(node):
			def extract_tags(W):
				pos = [W.getAttribute('lc') if W.getAttribute('lc') else None]
				if W.getAttribute('clitic')=='ezafe':
					pos.append('ezafe')
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
			if (first.tagName == 'w'):
				pos=extract_tags(first)
				return Tree(node.tagName,[(first.childNodes[0].data ,self._pos_map(pos))])
			childs = node.childNodes[2:] if node.tagName =='S' else node.childNodes
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

		def collapse(node, new_label):
			poses=node.pos()
			return Tree(new_label, [Tree(poses[i][1], [poses[i][0]]) for i in range(len(poses))])


		def traverse(node, parent, chunks):
			if ( node.label().count('-nid') > 0 ):
				node.set_label(node.label().replace('-nid', ''))
			if ( node.label().count('-nid') > 0 ):
				node.set_label(node.label().replace('-nid', ''))
			if ( node.label().count('-DiscA') > 0 ):
				node.set_label(node.label().replace('-DiscA', ''))

			if node.label() in {'CONJ', 'PUNC'}:
				chunks.append(node)
				return 1

			if node.label() == 'PREP':
				chunks.append(Tree('PP', [node]))
				return 1

			if node.label() == 'PostP':
				chunks.append(Tree('POSTPP', [node]))
				return


			for leaf in node.pos():
				if leaf[1] in { 'PUNC', 'CONJ', 'PREP', 'PostP'}:
					for i in range(len(node)):
						traverse(node[i], node, chunks)
					return

			if node.label() == 'NPA' and parent.label() in  {'CPC','PPC'}:
				chunks.append(collapse(node, 'NP'))
				return

			if node.label() == 'NPA' and len(node)>=1:
				if (node[0].label()=='ADV'):
					chunks.append(collapse(node,'NP'))
					return

			if node.label() in {'NPC', 'N', 'PRON', 'INFV', 'DPA', 'CLASS', 'DPC', 'DET', 'DEM', 'INTJ'}:
				chunks.append(collapse(node, 'NP'))
				return

			if node.label() == 'DPC' and len(node) >= 2:
				chunkable = True
				for leaf in node[1].pos():
					if leaf[1] in {'PUNC', 'CONJ', 'PREP', 'PostP'}:
						chunkable = False
				if (node[1].label() in {'N', 'NPA', 'NPC'} and chunkable):
					chunks.append(collapse(node, 'NP'))
					return

			if node.label() == 'DPA' and len(node)>=2:
				if (node[1].label()=='ADV'):
					chunks.append(collapse(node, 'ADVP'))
					return

			if node.label() in {'MV', 'V', 'AUX'}:
				chunks.append(Tree('VP', [node]))
				return

			if node.label() in {'ADJ', 'ADJPC', 'MADJ', 'ADVPA'}:
				chunks.append(Tree('ADJP', [node]))
				return

			if node.label() in {'ADV', 'MADV', 'ADVPC'}:
				chunks.append(Tree('ADVP', [node]))
				return

			if type(node[0]) != Tree:
				chunks.append(node)
				return

			for i in range(len(node)):
				traverse(node[i], node, chunks)

		for tree in self.trees():
			chunks=[]
			traverse(tree, None, chunks)
			for i in range(len(chunks)):
				if(chunks[i].label()== 'PUNC'):
					chunks[i]=chunks[i][0]
				else:
					chunks[i]=Tree(chunks[i].label(), chunks[i].leaves())
			yield Tree('S', chunks)
