# coding: utf8

from __future__ import unicode_literals
from nltk.stem.api import StemmerI


class Stemmer(StemmerI):
	"""
	>>> stemmer = Stemmer()
	>>> stemmer.stem('کتابی')
	'کتاب'
	>>> stemmer.stem('کتاب‌ها')
	'کتاب'
	>>> stemmer.stem('کتاب‌هایی')
	'کتاب'
	>>> stemmer.stem('کتابهایشان')
	'کتاب'
	>>> stemmer.stem('اندیشه‌اش')
	'اندیشه'
	"""

	def __init__(self):
		self.ends = ['ات', 'ان', 'ترین', 'تر', 'م', 'ت', 'ش', 'یی', 'ی', 'ها', 'ٔ', '‌ا', '‌']

	def stem(self, word):
		for end in self.ends:
			if word.endswith(end):
				word = word[:-len(end)]

		if word.endswith('ۀ'):
			word = word[:-len(end)] + 'ه'

		return word
