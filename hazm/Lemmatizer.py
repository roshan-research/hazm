#coding=utf8

import codecs, itertools
from .utils import u, list_u, default_words, default_verbs
from .Stemmer import Stemmer
from .WordTokenizer import WordTokenizer


class Lemmatizer():
	def __init__(self, words_file=default_words, verbs_file=default_verbs, joined_verb_parts=True):
		self.verbs = {}
		self.words = set([])
		self.stemmer = Stemmer()

		if words_file:
			self.words = set(map(lambda w: w.strip(), codecs.open(words_file, encoding='utf8')))

		if verbs_file:
			tokenizer = WordTokenizer(verbs_file=verbs_file)
			self.verbs[u'است'] = u'#است'
			for verb in tokenizer.verbs:
				for tense in self.conjugations(verb):
					self.verbs[tense] = verb
			if joined_verb_parts:
				for verb, after_verb in itertools.product(tokenizer.verbs, tokenizer.after_verbs):
					self.verbs[verb.split('#')[0] + u'ه ' + after_verb] = verb
				for verb, before_verb in itertools.product(tokenizer.verbs, tokenizer.before_verbs):
					self.verbs[before_verb + u' ' + verb.split('#')[0]] = verb

	def lemmatize(self, word, pos=''):
		"""
		>>> lemmatizer.lemmatize('کتاب‌ها')
		'کتاب'
		>>> lemmatizer.lemmatize('آتشفشان')
		'آتشفشان'
		>>> lemmatizer.lemmatize('می‌روم')
		'رفت#رو'
		>>> lemmatizer.lemmatize('گفته شده است')
		'گفت#گو'
		>>> lemmatizer.lemmatize('مردم', pos='N')
		'مردم'
		"""

		if (not pos or pos == 'V') and word in self.verbs:
			return self.verbs[word]

		if word in self.words:
			return word

		stem = self.stemmer.stem(word)
		if stem in self.words:
			return stem

		return word

	def conjugations(self, verb):
		"""
		>>> lemmatizer.conjugations('خورد#خور')
		['خوردم', 'خوردی', 'خورد', 'خوردیم', 'خوردید', 'خوردند', 'نخوردم', 'نخوردی', 'نخورد', 'نخوردیم', 'نخوردید', 'نخوردند', 'خورم', 'خوری', 'خورد', 'خوریم', 'خورید', 'خورند', 'نخورم', 'نخوری', 'نخورد', 'نخوریم', 'نخورید', 'نخورند', 'می‌خوردم', 'می‌خوردی', 'می‌خورد', 'می‌خوردیم', 'می‌خوردید', 'می‌خوردند', 'نمی‌خوردم', 'نمی‌خوردی', 'نمی‌خورد', 'نمی‌خوردیم', 'نمی‌خوردید', 'نمی‌خوردند', 'خورده‌ام', 'خورده‌ای', 'خورده', 'خورده‌ایم', 'خورده‌اید', 'خورده‌اند', 'نخورده‌ام', 'نخورده‌ای', 'نخورده', 'نخورده‌ایم', 'نخورده‌اید', 'نخورده‌اند', 'خورم', 'خوری', 'خورد', 'خوریم', 'خورید', 'خورند', 'نخورم', 'نخوری', 'نخورد', 'نخوریم', 'نخورید', 'نخورند', 'می‌خورم', 'می‌خوری', 'می‌خورد', 'می‌خوریم', 'می‌خورید', 'می‌خورند', 'نمی‌خورم', 'نمی‌خوری', 'نمی‌خورد', 'نمی‌خوریم', 'نمی‌خورید', 'نمی‌خورند', 'بخورم', 'بخوری', 'بخورد', 'بخوریم', 'بخورید', 'بخورند', 'نخورم', 'نخوری', 'نخورد', 'نخوریم', 'نخورید', 'نخورند', 'بخور', 'نخور']
		"""

		past, present = verb.split('#')
		ends = list_u(['م', 'ی', '', 'یم', 'ید', 'ند'])

		if verb == u'#هست':
			return [u'هست' + end for end in ends] + [u'نیست' + end for end in ends]

		past_simples = [past + end for end in ends]
		past_imperfects = [u'می‌'+ item for item in past_simples]
		ends = list_u(['ه‌ام', 'ه‌ای', 'ه', 'ه‌ایم', 'ه‌اید', 'ه‌اند'])
		past_narratives = [past + end for end in ends]

		ends = list_u(['م', 'ی', 'د', 'یم', 'ید', 'ند'])
		present_simples = [present + end for end in ends]
		present_imperfects = [u'می‌'+ item for item in present_simples]
		present_subjunctives = [u'ب'+ item for item in present_simples]
		present_not_subjunctives = [u'ن'+ item for item in present_simples]

		imperatives = [u'ب'+ present, u'ن'+ present]

		with_nots = lambda items: items + list(map(lambda item: u'ن' + item, items))
		return with_nots(past_simples) + with_nots(present_simples) + with_nots(past_imperfects) + with_nots(past_narratives) + with_nots(present_simples) + with_nots(present_imperfects) + present_subjunctives + present_not_subjunctives + imperatives


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'lemmatizer': Lemmatizer()})
