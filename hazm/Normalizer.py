# coding: utf8

from __future__ import unicode_literals
import re

from .Lemmatizer import Lemmatizer
from .WordTokenizer import *
from .SentenceTokenizer import *
from .POSTagger import *

maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))
compile_patterns = lambda patterns: [(re.compile(pattern), repl) for pattern, repl in patterns]

class Normalizer():
	def __init__(self, character_refinement=True, punctuation_spacing=True, affix_spacing=True):
		self._character_refinement = character_refinement
		self._punctuation_spacing = punctuation_spacing
		self._affix_spacing = affix_spacing

		self.translations = maketrans(' كي%1234567890;“”', ' کی٪۱۲۳۴۵۶۷۸۹۰؛""')

		punc_after, punc_before = r'!:\.،؛؟»\]\)\}', r'«\[\(\{'
		if character_refinement:
			self.character_refinement_patterns = compile_patterns([
				(r'[ـ\r]', ''), # remove keshide, carriage returns
				(r' +', ' '), # remove extra spaces
				(r'\n\n+', '\n\n'), # remove extra newlines
				('"([^\n"]+)"', r'«\1»'), # replace quotation with gyoome
				('([\d+])\.([\d+])', r'\1٫\2'), # replace dot with momayez
				(r' ?\.\.\.', ' …'), # replace 3 dots
			])

		if punctuation_spacing:
			self.punctuation_spacing_patterns = compile_patterns([
				(' (['+ punc_after +'])', r'\1'), # remove space before
				('(['+ punc_before +']) ', r'\1'), # remove space after
				('(['+ punc_after +'])([^ '+ punc_after +'])', r'\1 \2'), # put space after
				('([^ '+ punc_before +'])(['+ punc_before +'])', r'\1 \2'), # put space before
			])

		if affix_spacing:
			self.affix_spacing_patterns = compile_patterns([
				(r'([^ ]ه) ی ', r'\1‌ی '), # fix ی space
				(r'(^| )(ن?می) ', r'\1\2‌'), # put zwnj after می, نمی
				(r' (تر(ی(ن)?)?|ها(ی)?)(?=[ \n'+ punc_after + punc_before +']|$)', r'‌\1'), # put zwnj before تر, ترین, ها, های
				(r'([^ ]ه) (ا(م|ت|ش|ی))(?=[ \n'+ punc_after +']|$)', r'\1‌\2'), # join ام, ات, اش, ای
			])

	def normalize(self, text):
		if self._character_refinement:
			text = self.character_refinement(text)
		if self._punctuation_spacing:
			text = self.punctuation_spacing(text)
		if self._affix_spacing:
			text = self.affix_spacing(text)
		return text

	def character_refinement(self, text):
		"""
		>>> normalizer = Normalizer()
		>>> normalizer.character_refinement('اصلاح كاف و ياي عربي')
		'اصلاح کاف و یای عربی'

		>>> normalizer.character_refinement('عراق سال 2012 قراردادی به ارزش "4.2 میلیارد دلار" برای خرید تجهیزات نظامی با روسیه امضا  کرد.')
		'عراق سال ۲۰۱۲ قراردادی به ارزش «۴٫۲ میلیارد دلار» برای خرید تجهیزات نظامی با روسیه امضا کرد.'

		>>> normalizer.character_refinement('رمــــان')
		'رمان'
		"""

		text = text.translate(self.translations)
		for pattern, repl in self.character_refinement_patterns:
			text = pattern.sub(repl, text)
		return text

	def punctuation_spacing(self, text):
		"""
		>>> normalizer = Normalizer()
		>>> normalizer.punctuation_spacing('اصلاح ( پرانتزها ) در متن .')
		'اصلاح (پرانتزها) در متن.'
		"""

		# todo: don't put space inside time
		for pattern, repl in self.punctuation_spacing_patterns:
			text = pattern.sub(repl, text)
		return text

	def affix_spacing(self, text):
		"""
		>>> normalizer = Normalizer()
		>>> normalizer.affix_spacing('خانه ی پدری')
		'خانه‌ی پدری'

		>>> normalizer.affix_spacing('فاصله میان پیشوند ها و پسوند ها را اصلاح می کند.')
		'فاصله میان پیشوند‌ها و پسوند‌ها را اصلاح می‌کند.'

		>>> normalizer.affix_spacing('می روم')
		'می‌روم'

		>>> normalizer.affix_spacing('حرفه ای')
		'حرفه‌ای'
		"""

		for pattern, repl in self.affix_spacing_patterns:
			text = pattern.sub(repl, text)
		return text



class InformalNormalizer(Normalizer):
	def __init__(self, **args):
		super(InformalNormalizer, self).__init__(**args)
		lemmatizer = Lemmatizer()
		self.verb_map = {
			'ر': 'رفت#رو', 
			'خوا': 'خواست#خواه',
			'گ': 'گفت#گو',
			'دار': 'داشت#دار',
			'دون': 'دانست#دان',
			'ش': 'شد#شو',
			'کن': 'کرد#کن',
			'تونست': 'توانستن#توانسن',
		}
		self.informal_verbs_mapping = {}
		for informal, formal in self.verb_map.items():
			informal_verbs = self.informal_conjugations(informal)
			formal_verbs = lemmatizer.conjugations(formal)
			for i in range(len(informal_verbs)):
				self.informal_verbs_mapping[informal_verbs[i]] = formal_verbs[i+60]

	def normalize(self, text):
		"""
		>>> normalizer = InformalNormalizer()
		>>> normalizer.normalize('فردا می‌رم')
		'فردا می‌روم'
		"""
		lemmatizer = Lemmatizer()
		tagger = POSTagger(model='/home/afshin/dev/hazm/resources/postagger.model')
		sent_tokenizer = SentenceTokenizer()
		word_tokenizer = WordTokenizer()
		super(InformalNormalizer, self).__init__(punctuation_spacing=False)
		text = super(InformalNormalizer, self).normalize(text)
		sentences = [\
			word_tokenizer.tokenize(sentence)\
			for sentence in sent_tokenizer.tokenize(text)\
		]
		tags = tagger.tag_sents(sentences)
		formal_res = ''
		informal_res = ''
		for sent_tags in tags:
			sent = [word for word, tag in sent_tags]
			formal_res += (' '.join(sent) + '\n')
			i = 0
			for word, tag in sent_tags:
				if tag == 'V': 
					if (word.endswith('ه') and (word + 'د') in lemmatizer.verbs):
						sent[i] = word + 'د'
					elif word.endswith('ه') and (word[:-1] + 'د') in lemmatizer.verbs:
						sent[i] = word[:-1] + 'د'
					elif word.endswith('ن') and word + 'د' in lemmatizer.verbs:
						sent[i] = word + 'د'
					elif (word.endswith('ه') and (word[:-1] + 'ود') in lemmatizer.verbs): 
						sent[i] = word[:-1] + 'ود'
					elif word.endswith('ه') and word[:-1] in lemmatizer.words:
						sent[i] = word[:-1] + ' است'
					elif word in self.informal_verbs_mapping.keys():
						sent[i] = self.informal_verbs_mapping[word]
				if tag == 'N':
					if word.endswith('ونه') and word[:-3] + 'انه' in lemmatizer.words:
						sent[i] = word[:-3] + 'انه'
				i += 1
			informal_res += (' '.join(sent) + '\n')
		return formal_res, informal_res


	def informal_conjugations(self, verb):
	  ends = ['م', 'ی', '', 'یم', 'ین', 'ن']
	  present_simples = [verb + end for end in ends]
	  if verb.endswith('ا'):
	    present_simples[2] = verb + 'د'
	  else:
	    present_simples[2] = verb + 'ه'
	  present_imperfects = ['می‌' + item for item in present_simples]
	  present_not_imperfects = ['ن' + item for item in present_imperfects]
	  present_subjunctives = ['ب'+ item for item in present_simples] 
	  present_not_subjunctives = ['ن'+ item for item in present_simples] 
	  return present_imperfects + present_not_imperfects + present_subjunctives + present_not_subjunctives
