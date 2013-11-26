#coding=utf8

import codecs, itertools
from .Stemmer import Stemmer
from .WordTokenizer import WordTokenizer


class Lemmatizer():
	def __init__(self, words_file='data/words.dat', tenses_file='data/tenses.dat', joined_verb_parts=False):
		self.stemmer = Stemmer()
		self.dict = {}
		self.words = set([])

		if words_file:
			self.words = set(map(lambda w: w.strip(), codecs.open(words_file, encoding='utf8')))

		if tenses_file:
			for line in codecs.open(tenses_file, encoding='utf8'):
				if line:
					verb, tenses = line.strip().split(' | ')
					for tense in tenses.split(' '):
						self.dict[tense] = verb

		if joined_verb_parts:
			tokenizer = WordTokenizer(join_verb_parts=True)
			for verbe, after_verb in itertools.product(tokenizer.verbe, tokenizer.after_verbs):
				self.dict[verbe +' '+ after_verb] = verbe[:-1]+'ن'

	def lemmatize(self, word):
		"""
		>>> lemmatizer.lemmatize('کتاب‌ها')
		'کتاب'
		>>> lemmatizer.lemmatize('آتشفشان')
		'آتشفشان'
		>>> lemmatizer.lemmatize('می‌روم')
		'رفتن'
		>>> lemmatizer.lemmatize('گفته شده است')
		'گفتن'
		"""

		if word in self.dict:
			return self.dict[word]

		stem = self.stemmer.stem(word)
		if stem in self.words:
			return stem

		return word


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'lemmatizer': Lemmatizer(joined_verb_parts=True)})
