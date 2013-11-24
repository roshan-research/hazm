#coding=utf8

from nltk.stem.api import StemmerI


class Stemmer(StemmerI):
	def __init__(self):
		self.ends = ['ان', 'م', 'ت', 'ش', 'یی', 'ی', 'ها', '‌']

	def stem(self, text):
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
			if text.endswith(end):
				text = text[:-len(end)]
		return text


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'stemmer': Stemmer()})
