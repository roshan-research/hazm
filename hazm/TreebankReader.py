# coding: utf8

from __future__ import unicode_literals, print_function
import os, sys, re,codecs
from xml.dom import minidom
from nltk.tree import Tree


def coarse_pos(tags):
	"""
	Coarse POS tags of Treebank corpus:
		N: Noun, V: Verb, A: Adjective, R: Adverb, P: Pronoun, D: Determiner, Sp: Preposition, St: Postposition, M: Number, C: Conjunction, O: Punctuation, X: Residual, Y: Abbreviation, I: Interjection

	>>> coarse_pos(['Nasp---', 'pers', 'prop'])
	'N'
	"""

	map = {'N': 'N', 'V': 'V', 'A': 'AJ', 'R': 'ADV', 'P': 'PRO', 'D': 'DET', 'M': 'NUM', 'C': 'CONJ', 'O':'PUNC', 'X': 'RES', 'I': 'INT', 'Y': 'N'}
	try:
		if tags[0].startswith('Sp'):
			return 'P'
		if tags[0].startswith('St'):
			return 'POSTP'
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
		['دنیای', 'آدولف', 'بورن', 'دنیای', 'اتفاقات', 'رویایی', 'است', '.']
		"""

		def traverse(node):
			first = node.childNodes[0]
			if (first.tagName == 'w'):
				return Tree(node.tagName, [first.childNodes[0].data])
			childs = node.childNodes[2:] if node.tagName =='S' else node.childNodes
			return Tree(node.tagName, map(traverse, childs))

		for doc in self.docs():
			for S in doc.getElementsByTagName('S'):
				yield traverse(S)

	def sents(self):
		"""
		>>> next(treebank.sents())
		[('دنیای', 'Ne'), ('آدولف', 'N'), ('بورن', 'N'), ('دنیای', 'Ne'), ('اتفاقات', 'Ne'), ('رویایی', 'AJ'), ('است', 'V'), ('.', 'PUNC')]
		"""

		for doc in self.docs():
			for S in doc.getElementsByTagName('S'):
				sentence = []
				for W in S.getElementsByTagName('w'):
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

					sentence.append((W.childNodes[0].data, self._pos_map(pos)))

				yield sentence
