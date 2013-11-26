#coding=utf8

import codecs
from .utils import list_u
from nltk.stem.api import StemmerI


class Stemmer(StemmerI):
	def __init__(self):
		self.ends = list_u(['ات', 'ان', 'م', 'ت', 'ش', 'یی', 'ی', 'ها', '‌'])

	def stem(self, word):
		"""
		>>> stemmer.stem('کتابی')
		'کتاب'
		>>> stemmer.stem('کتاب‌ها')
		'کتاب'
		>>> stemmer.stem('کتاب‌هایی')
		'کتاب'
		>>> stemmer.stem('کتابهایشان')
		'کتاب'
		"""

		for end in self.ends:
			if word.endswith(end):
				word = word[:-len(end)]

		return word


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'stemmer': Stemmer()})
