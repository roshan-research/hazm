# coding: utf8

from __future__ import unicode_literals, print_function
import os, sys, re,codecs
from xml.dom import minidom
from nltk.tree import Tree


class TreebankReader():

	def __init__(self, root='corpora/treebank'):
		self._root = root
		self._paragraph_pattern = re.compile(r'(\n.{0,50})(?=\n)')

	def trees(self):
		"""
		>>> next(treebank.trees()).leaves()
		['دنیای', 'آدولف', 'بورن', 'دنیای', 'اتفاقات', 'رویایی', 'است', '.']
		"""

		for root, dirs, files in os.walk(self._root):
			for name in sorted(files):
				def traverse(node):
					first = node.childNodes[0]
					if (first.tagName == 'w'):
						return Tree(node.tagName, [first.childNodes[0].data])
					childs = node.childNodes[2:] if node.tagName =='S' else node.childNodes
					return Tree(node.tagName, map(traverse, childs))

				try:
					raw = codecs.open(os.path.join(root, name) , encoding='utf8').read();
					raw = re.sub(r'\n *', '', raw)
					elements = minidom.parseString(raw.encode('utf8'))
					for S in elements.getElementsByTagName('S'):
						yield traverse(S)
				except Exception as e:
					print('error in reading', name, e, file=sys.stderr)
