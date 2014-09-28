# coding: utf8

from __future__ import unicode_literals
import codecs
from nltk.parse import DependencyGraph
from .Chunker import tree2brackets


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
		"""
		>>> next(dadegan.sents())
		[('دنیای', 'Ne'), ('آدولف', 'N'), ('بورن', 'N'), ('دنیای', 'Ne'), ('اتفاقات', 'Ne'), ('رویایی', 'AJ'), ('است', 'V'), ('.', 'PUNC')]
		"""
		for tree in self.trees():
			yield [node['word'] for node in tree.nodelist[1:]]

	def chunked_trees(self):
		"""
		>>> tree2brackets(next(dadegan.chunked_trees()))
		'[این میهمانی NP] [به PP] [منظور آشنایی هم‌تیمی‌های او NP] [با PP] [غذاهای ایرانی NP] [ترتیب داده شد VP] .'
		"""