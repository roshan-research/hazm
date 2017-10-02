# coding: utf-8

from __future__ import unicode_literals
import re
from .Lemmatizer import Lemmatizer
from .WordTokenizer import WordTokenizer
from .utils import maketrans

compile_patterns = lambda patterns: [(re.compile(pattern), repl) for pattern, repl in patterns]


class Normalizer(object):
	def __init__(self, remove_extra_spaces=True, persian_style=True, persian_numbers=True, remove_diacritics=True, affix_spacing=True, token_based=False, punctuation_spacing=True):
		self._punctuation_spacing = punctuation_spacing
		self._affix_spacing = affix_spacing
		self._token_based = token_based

		translation_src, translation_dst = ' كي“”', ' کی""'
		if persian_numbers:
			translation_src += '0123456789%'
			translation_dst += '۰۱۲۳۴۵۶۷۸۹٪'
		self.translations = maketrans(translation_src, translation_dst)

		if self._token_based:
			lemmatizer = Lemmatizer()
			self.words = lemmatizer.words
			self.verbs = lemmatizer.verbs
			self.tokenizer = WordTokenizer(join_verb_parts=False)
			self.suffixes = {'ی', 'ای', 'ها', 'های', 'تر', 'تری', 'ترین', 'گر', 'گری', 'ام', 'ات', 'اش'}

		self.character_refinement_patterns = []

		if remove_extra_spaces:
			self.character_refinement_patterns.extend([
				(r' +', ' '),  # remove extra spaces
				(r'\n\n+', '\n\n'),  # remove extra newlines
				(r'[ـ\r]', ''),  # remove keshide, carriage returns
			])

		if persian_style:
			self.character_refinement_patterns.extend([
				('"([^\n"]+)"', r'«\1»'),  # replace quotation with gyoome
				('([\d+])\.([\d+])', r'\1٫\2'),  # replace dot with momayez
				(r' ?\.\.\.', ' …'),  # replace 3 dots
			])

		if remove_diacritics:
			self.character_refinement_patterns.append(
				('[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]', ''),  # remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
			)

		self.character_refinement_patterns = compile_patterns(self.character_refinement_patterns)

		punc_after, punc_before = r'\.:!،؛؟»\]\)\}', r'«\[\(\{'
		if punctuation_spacing:
			self.punctuation_spacing_patterns = compile_patterns([
				('" ([^\n"]+) "', r'"\1"'),  # remove space before and after quotation
				(' (['+ punc_after +'])', r'\1'),  # remove space before
				('(['+ punc_before +']) ', r'\1'),  # remove space after
				('(['+ punc_after[:3] +'])([^ \d'+ punc_after +'])', r'\1 \2'),  # put space after . and :
				('(['+ punc_after[3:] +'])([^ '+ punc_after +'])', r'\1 \2'),  # put space after
				('([^ '+ punc_before +'])(['+ punc_before +'])', r'\1 \2'),  # put space before
			])

		if affix_spacing:
			self.affix_spacing_patterns = compile_patterns([
				(r'([^ ]ه) ی ', r'\1‌ی '),  # fix ی space
				(r'(^| )(ن?می) ', r'\1\2‌'),  # put zwnj after می, نمی
				(r'(?<=[^\n\d '+ punc_after + punc_before +']{2}) (تر(ین?)?|گری?|های?)(?=[ \n'+ punc_after + punc_before +']|$)', r'‌\1'),  # put zwnj before تر, تری, ترین, گر, گری, ها, های
				(r'([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n'+ punc_after +']|$)', r'\1‌\2'),  # join ام, ایم, اش, اند, ای, اید, ات
			])

	def normalize(self, text):
		text = self.character_refinement(text)
		if self._affix_spacing:
			text = self.affix_spacing(text)

		if self._token_based:
			tokens = self.tokenizer.tokenize(text.translate(self.translations))
			text = ' '.join(self.token_spacing(tokens))

		if self._punctuation_spacing:
			text = self.punctuation_spacing(text)

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

		>>> normalizer.character_refinement('بُشقابِ مَن را بِگیر')
		'بشقاب من را بگیر'
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

		>>> normalizer.punctuation_spacing('نسخه 0.5 در ساعت 22:00 تهران،1396')
		'نسخه 0.5 در ساعت 22:00 تهران، 1396'
		"""

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

		>>> normalizer.affix_spacing('محبوب ترین ها')
		'محبوب‌ترین‌ها'
		"""

		for pattern, repl in self.affix_spacing_patterns:
			text = pattern.sub(repl, text)
		return text

	def token_spacing(self, tokens):
		"""
		>>> normalizer = Normalizer(token_based=True)
		>>> normalizer.token_spacing(['کتاب', 'ها'])
		['کتاب‌ها']

		>>> normalizer.token_spacing(['او', 'می', 'رود'])
		['او', 'می‌رود']

		>>> normalizer.token_spacing(['ماه', 'می', 'سال', 'جدید'])
		['ماه', 'می', 'سال', 'جدید']

		>>> normalizer.token_spacing(['اخلال', 'گر'])
		['اخلال‌گر']

		>>> normalizer.token_spacing(['پرداخت', 'شده', 'است'])
		['پرداخت', 'شده', 'است']

		>>> normalizer.token_spacing(['زمین', 'لرزه', 'ای'])
		['زمین‌لرزه‌ای']
		"""

		result = []
		for t, token in enumerate(tokens):
			joined = False

			if result:
				token_pair = result[-1]+'‌'+token
				if token_pair in self.verbs or token_pair in self.words and self.words[token_pair][0] > 0:
					joined = True

					if t < len(tokens)-1 and token+'_'+tokens[t+1] in self.verbs:
						joined = False

				elif token in self.suffixes and result[-1] in self.words:
					joined = True

			if joined:
				result.pop()
				result.append(token_pair)
			else:
				result.append(token)

		return result
