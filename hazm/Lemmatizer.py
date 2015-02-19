# coding: utf8

from __future__ import unicode_literals
import codecs
from .utils import default_words, default_verbs
from .Stemmer import Stemmer
from .WordTokenizer import WordTokenizer


class Lemmatizer():
	"""
	>>> lemmatizer = Lemmatizer()
	>>> lemmatizer.lemmatize('کتاب‌ها')
	'کتاب'
	>>> lemmatizer.lemmatize('آتشفشان')
	'آتشفشان'
	>>> lemmatizer.lemmatize('می‌روم')
	'رفت#رو'
	>>> lemmatizer.lemmatize('گفته_شده_است')
	'گفت#گو'
	>>> lemmatizer.lemmatize('نچشیده_است')
	'چشید#چش'
	>>> lemmatizer.lemmatize('مردم', pos='N')
	'مردم'
	>>> lemmatizer.lemmatize('اجتماعی', pos='AJ')
	'اجتماعی'
	"""

	def __init__(self, words_file=default_words, verbs_file=default_verbs, joined_verb_parts=True):
		self.verbs = {}
		self.words = set([])
		self.stemmer = Stemmer()

		if words_file:
			with codecs.open(words_file, encoding='utf8') as words_file:
				self.words = set(map(lambda w: w.strip(), words_file))

		if verbs_file:
			tokenizer = WordTokenizer(verbs_file=verbs_file)
			self.verbs['است'] = '#است'
			for verb in tokenizer.verbs:
				for tense in self.conjugations(verb):
					self.verbs[tense] = verb
			if joined_verb_parts:
				for verb in tokenizer.verbs:
					bon = verb.split('#')[0]
					for after_verb in tokenizer.after_verbs:
						self.verbs[bon +'ه_'+ after_verb] = verb
						self.verbs['ن'+ bon +'ه_'+ after_verb] = verb
					for before_verb in tokenizer.before_verbs:
						self.verbs[before_verb +'_'+ bon] = verb

	def lemmatize(self, word, pos=''):
		if not pos and word in self.words:
			return word

		if (not pos or pos == 'V') and word in self.verbs:
			return self.verbs[word]

		if pos.startswith('AJ') and word[-1] == 'ی':
			return word

		if pos == 'PRO':
			return word

		if word in self.words:
			return word

		stem = self.stemmer.stem(word)
		if stem and stem in self.words:
			return stem

		return word

	def conjugations(self, verb):
		"""
		>>> lemmatizer = Lemmatizer()
		>>> lemmatizer.conjugations('خورد#خور')
		['خوردم', 'خوردی', 'خورد', 'خوردیم', 'خوردید', 'خوردند', 'نخوردم', 'نخوردی', 'نخورد', 'نخوردیم', 'نخوردید', 'نخوردند', 'خورم', 'خوری', 'خورد', 'خوریم', 'خورید', 'خورند', 'نخورم', 'نخوری', 'نخورد', 'نخوریم', 'نخورید', 'نخورند', 'می‌خوردم', 'می‌خوردی', 'می‌خورد', 'می‌خوردیم', 'می‌خوردید', 'می‌خوردند', 'نمی‌خوردم', 'نمی‌خوردی', 'نمی‌خورد', 'نمی‌خوردیم', 'نمی‌خوردید', 'نمی‌خوردند', 'خورده‌ام', 'خورده‌ای', 'خورده', 'خورده‌ایم', 'خورده‌اید', 'خورده‌اند', 'نخورده‌ام', 'نخورده‌ای', 'نخورده', 'نخورده‌ایم', 'نخورده‌اید', 'نخورده‌اند', 'خورم', 'خوری', 'خورد', 'خوریم', 'خورید', 'خورند', 'نخورم', 'نخوری', 'نخورد', 'نخوریم', 'نخورید', 'نخورند', 'می‌خورم', 'می‌خوری', 'می‌خورد', 'می‌خوریم', 'می‌خورید', 'می‌خورند', 'نمی‌خورم', 'نمی‌خوری', 'نمی‌خورد', 'نمی‌خوریم', 'نمی‌خورید', 'نمی‌خورند', 'بخورم', 'بخوری', 'بخورد', 'بخوریم', 'بخورید', 'بخورند', 'نخورم', 'نخوری', 'نخورد', 'نخوریم', 'نخورید', 'نخورند', 'بخور', 'نخور']
		>>> lemmatizer.conjugations('آورد#آور')
		['آوردم', 'آوردی', 'آورد', 'آوردیم', 'آوردید', 'آوردند', 'نیاوردم', 'نیاوردی', 'نیاورد', 'نیاوردیم', 'نیاوردید', 'نیاوردند', 'آورم', 'آوری', 'آورد', 'آوریم', 'آورید', 'آورند', 'نیاورم', 'نیاوری', 'نیاورد', 'نیاوریم', 'نیاورید', 'نیاورند', 'می‌آوردم', 'می‌آوردی', 'می‌آورد', 'می‌آوردیم', 'می‌آوردید', 'می‌آوردند', 'نمی‌آوردم', 'نمی‌آوردی', 'نمی‌آورد', 'نمی‌آوردیم', 'نمی‌آوردید', 'نمی‌آوردند', 'آورده‌ام', 'آورده‌ای', 'آورده', 'آورده‌ایم', 'آورده‌اید', 'آورده‌اند', 'نیاورده‌ام', 'نیاورده‌ای', 'نیاورده', 'نیاورده‌ایم', 'نیاورده‌اید', 'نیاورده‌اند', 'آورم', 'آوری', 'آورد', 'آوریم', 'آورید', 'آورند', 'نیاورم', 'نیاوری', 'نیاورد', 'نیاوریم', 'نیاورید', 'نیاورند', 'می‌آورم', 'می‌آوری', 'می‌آورد', 'می‌آوریم', 'می‌آورید', 'می‌آورند', 'نمی‌آورم', 'نمی‌آوری', 'نمی‌آورد', 'نمی‌آوریم', 'نمی‌آورید', 'نمی‌آورند', 'بیاورم', 'بیاوری', 'بیاورد', 'بیاوریم', 'بیاورید', 'بیاورند', 'نیاورم', 'نیاوری', 'نیاورد', 'نیاوریم', 'نیاورید', 'نیاورند', 'بیاور', 'نیاور']
		"""

		past, present = verb.split('#')
		ends = ['م', 'ی', '', 'یم', 'ید', 'ند']

		if verb == '#هست':
			return ['هست' + end for end in ends] + ['نیست' + end for end in ends]

		past_simples = [past + end for end in ends]
		past_imperfects = ['می‌'+ item for item in past_simples]
		ends = ['ه‌ام', 'ه‌ای', 'ه', 'ه‌ایم', 'ه‌اید', 'ه‌اند']
		past_narratives = [past + end for end in ends]

		imperatives = ['ب'+ present, 'ن'+ present]

		if present.endswith('ا') or present in ('آ', 'گو'):
			present = present + 'ی'

		ends = ['م', 'ی', 'د', 'یم', 'ید', 'ند']
		present_simples = [present + end for end in ends]
		present_imperfects = ['می‌'+ item for item in present_simples]
		present_subjunctives = ['ب'+ item for item in present_simples]
		present_not_subjunctives = ['ن'+ item for item in present_simples]

		with_nots = lambda items: items + list(map(lambda item: 'ن' + item, items))
		aa_refinement = lambda items: list(map(lambda item: item.replace('بآ', 'بیا').replace('نآ', 'نیا'), items)) if items[0].startswith('آ') else items
		return aa_refinement(with_nots(past_simples) + with_nots(present_simples) + with_nots(past_imperfects) + with_nots(past_narratives) + with_nots(present_simples) + with_nots(present_imperfects) + present_subjunctives + present_not_subjunctives + imperatives)
