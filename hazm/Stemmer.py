#coding=utf8

import codecs
from nltk.stem.api import StemmerI


class Stemmer(StemmerI):
	def __init__(self, words_file='data/words.dat', tenses_file='data/tenses.dat'):
		self.ends = ['ان', 'م', 'ت', 'ش', 'یی', 'ی', 'ها', '‌']
		self.tenses = {}
		self.words = set([])

		if words_file:
			self.words = set(map(lambda w: w.strip(), codecs.open(words_file, encoding='utf8')))

		if tenses_file:
			for line in codecs.open(tenses_file, encoding='utf8'):
				if line:
					verb, tenses = line.strip().split(' | ')
					for tense in tenses.split(' '):
						self.tenses[tense] = verb

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
		>>> stemmer.stem('لبنان')
		'لبنان'
		>>> stemmer.stem('می‌روم')
		'رفتن'
		"""

		if self.tenses and word in self.tenses:
			return self.tenses[word]

		stemmed = word
		for end in self.ends:
			if stemmed.endswith(end):
				stemmed = stemmed[:-len(end)]

		if self.words and stemmed not in self.words:
			return word

		return stemmed


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'stemmer': Stemmer()})
