#coding=utf8

import codecs, itertools
from .utils import u, default_words, default_verbs
from .Stemmer import Stemmer
from .WordTokenizer import WordTokenizer


class Lemmatizer():
	def __init__(self, words_file=default_words, verbs_file=default_verbs, joined_verb_parts=True):
		self.dict = {}
		self.words = set([])
		self.stemmer = Stemmer()

		if words_file:
			self.words = set(map(lambda w: w.strip(), codecs.open(words_file, encoding='utf8')))

		if verbs_file:
			for verb in map(lambda v: v.strip(), codecs.open(verbs_file, encoding='utf8')):
				if verb:
					for tense in self.conjugations(verb):
						self.dict[tense] = verb

		if joined_verb_parts:
			tokenizer = WordTokenizer(verbs_file=verbs_file)
			verbs = [verb.strip() for verb in codecs.open(verbs_file, encoding='utf8') if verb]
			for verb, after_verb in itertools.product(verbs, tokenizer.after_verbs):
				self.dict[verb.split('#')[0] +'ه '+ after_verb] = verb

	def lemmatize(self, word):
		"""
		>>> lemmatizer.lemmatize('کتاب‌ها')
		'کتاب'
		>>> lemmatizer.lemmatize('آتشفشان')
		'آتشفشان'
		>>> lemmatizer.lemmatize('می‌روم')
		'رفت#رو'
		>>> lemmatizer.lemmatize('گفته شده است')
		'گفت#گو'
		"""

		if word in self.words:
			return word

		if word in self.dict:
			return self.dict[word]

		stem = self.stemmer.stem(word)
		if stem in self.words:
			return stem

		return word

	def conjugations(self, verb):
		"""
		>>> print(*lemmatizer.conjugations('خورد#خور'))
		خورم خوری خورد خوریم خورید خورند نخورم نخوری نخورد نخوریم نخورید نخورند می‌خوردم می‌خوردی می‌خورد می‌خوردیم می‌خوردید می‌خوردند نمی‌خوردم نمی‌خوردی نمی‌خورد نمی‌خوردیم نمی‌خوردید نمی‌خوردند خورده‌ام خورده‌ام خورده‌ام خورده‌ام خورده‌ام خورده‌ام نخورده‌ام نخورده‌ام نخورده‌ام نخورده‌ام نخورده‌ام نخورده‌ام خورم خوری خورد خوریم خورید خورند نخورم نخوری نخورد نخوریم نخورید نخورند می‌خورم می‌خوری می‌خورد می‌خوریم می‌خورید می‌خورند نمی‌خورم نمی‌خوری نمی‌خورد نمی‌خوریم نمی‌خورید نمی‌خورند بخورم بخوری بخورد بخوریم بخورید بخورند نخورم نخوری نخورد نخوریم نخورید نخورند بخور نخور
		"""

		past, present = verb.split('#')
		with_nots = lambda items: items + list(map(lambda item: 'ن' + item, items))

		ends = ['م', 'ی', '', 'یم', 'ید', 'ند']
		past_simples = [past + end for end in ends]
		past_imperfects = ['می‌'+ item for item in past_simples]
		past_narratives = [past +'ه‌ام' for end in ends]

		ends = ['م', 'ی', 'د', 'یم', 'ید', 'ند']
		present_simples = [present + end for end in ends]
		present_imperfects = ['می‌'+ item for item in present_simples]
		present_subjunctives = ['ب'+ item for item in present_simples]
		present_not_subjunctives = ['ن'+ item for item in present_simples]

		imperatives = ['ب'+ present, 'ن'+ present]

		return with_nots(present_simples) + with_nots(past_imperfects) + with_nots(past_narratives) + with_nots(present_simples) + with_nots(present_imperfects) + present_subjunctives + present_not_subjunctives + imperatives


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'lemmatizer': Lemmatizer()})
