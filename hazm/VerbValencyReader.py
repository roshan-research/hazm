# coding: utf8

from __future__ import unicode_literals
import codecs
from collections import namedtuple


Verb = namedtuple('Verb', ('past_light_verb', 'present_light_verb', 'prefix', 'nonverbal_element', 'preposition', 'valency'))


class VerbValencyReader():
	"""
	interfaces [Verb Valency Corpus](http://dadegan.ir/catalog/pervallex)
	Mohammad Sadegh Rasooli, Amirsaeid Moloodi, Manouchehr Kouhestani, & Behrouz Minaei Bidgoli. (2011). A Syntactic Valency Lexicon for Persian Verbs: The First Steps towards Persian Dependency Treebank. in 5th Language & Technology Conference (LTC): Human Language Technologies as a Challenge for Computer Science and Linguistics (pp. 227–231). Poznań, Poland.
	"""

	def __init__(self, valency_file='corpora/valency.txt'):
		self._valency_file = valency_file

	def verbs(self):
		with codecs.open(self._valency_file, encoding='utf-8') as valency_file:
			for line in valency_file:
				if 'بن ماضی' in line:
					continue

				line = line.strip().replace('-\t', '\t')
				parts = line.split('\t')
				if len(parts) == 6:
					yield Verb(*parts)
