# coding: utf8

from __future__ import unicode_literals
import codecs
from nltk.parse import DependencyGraph


class DadeganReader():
	"""
	interfaces [Persian Dependency Treebank](http://dadegan.ir/perdt/download)
	"""

	def __init__(self, dadegan_file='corpora/dadegan.conll'):
		self._dadegan_file = dadegan_file

	def _sentences(self):
		text = codecs.open(self._dadegan_file, encoding='utf8').read()

		# refine text
		text = text.replace('‌‌','‌').replace('\t‌','\t').replace('‌\t','\t').replace('\t ','\t').replace(' \t','\t').replace('\r', '').replace('\u2029', '‌')

		for item in text.replace(' ', '_').split('\n\n'):
			if item.strip():
				yield item

	def trees(self):
		for sentence in self._sentences():
			yield DependencyGraph(sentence)

	def sents(self):
		for tree in self.trees():
			yield [node['word'] for node in tree.nodelist[1:]]
