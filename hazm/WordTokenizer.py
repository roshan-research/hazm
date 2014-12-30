# coding: utf8

from __future__ import unicode_literals
import re, codecs
from .utils import default_verbs
from nltk.tokenize.api import TokenizerI


class WordTokenizer(TokenizerI):
	"""
	>>> tokenizer = WordTokenizer()
	>>> tokenizer.tokenize('این جمله (خیلی) پیچیده نیست!!!')
	['این', 'جمله', '(', 'خیلی', ')', 'پیچیده', 'نیست', '!!!']
	"""

	def __init__(self, verbs_file=default_verbs, join_verb_parts=True):
		self._join_verb_parts = join_verb_parts
		self.pattern = re.compile(r'([؟!\?]+|[:\.،؛»\]\)\}"«\[\(\{])')

		if join_verb_parts:
			self.after_verbs = set([
				'ام', 'ای', 'است', 'ایم', 'اید', 'اند', 'بودم', 'بودی', 'بود', 'بودیم', 'بودید', 'بودند', 'باشم', 'باشی', 'باشد', 'باشیم', 'باشید', 'باشند',
				'شده_ام', 'شده_ای', 'شده_است', 'شده_ایم', 'شده_اید', 'شده_اند', 'شده_بودم', 'شده_بودی', 'شده_بود', 'شده_بودیم', 'شده_بودید', 'شده_بودند', 'شده_باشم', 'شده_باشی', 'شده_باشد', 'شده_باشیم', 'شده_باشید', 'شده_باشند',
				'نشده_ام', 'نشده_ای', 'نشده_است', 'نشده_ایم', 'نشده_اید', 'نشده_اند', 'نشده_بودم', 'نشده_بودی', 'نشده_بود', 'نشده_بودیم', 'نشده_بودید', 'نشده_بودند', 'نشده_باشم', 'نشده_باشی', 'نشده_باشد', 'نشده_باشیم', 'نشده_باشید', 'نشده_باشند',
				'شوم', 'شوی', 'شود', 'شویم', 'شوید', 'شوند', 'شدم', 'شدی', 'شد', 'شدیم', 'شدید', 'شدند',
				'نشوم', 'نشوی', 'نشود', 'نشویم', 'نشوید', 'نشوند', 'نشدم', 'نشدی', 'نشد', 'نشدیم', 'نشدید', 'نشدند',
				'می‌شوم', 'می‌شوی', 'می‌شود', 'می‌شویم', 'می‌شوید', 'می‌شوند', 'می‌شدم', 'می‌شدی', 'می‌شد', 'می‌شدیم', 'می‌شدید', 'می‌شدند',
				'نمی‌شوم', 'نمی‌شوی', 'نمی‌شود', 'نمی‌شویم', 'نمی‌شوید', 'نمی‌شوند', 'نمی‌شدم', 'نمی‌شدی', 'نمی‌شد', 'نمی‌شدیم', 'نمی‌شدید', 'نمی‌شدند',
				'خواهم_شد', 'خواهی_شد', 'خواهد_شد', 'خواهیم_شد', 'خواهید_شد', 'خواهند_شد',
				'نخواهم_شد', 'نخواهی_شد', 'نخواهد_شد', 'نخواهیم_شد', 'نخواهید_شد', 'نخواهند_شد',
			])

			self.before_verbs = set([
				'خواهم', 'خواهی', 'خواهد', 'خواهیم', 'خواهید', 'خواهند',
				'نخواهم', 'نخواهی', 'نخواهد', 'نخواهیم', 'نخواهید', 'نخواهند'
			])

			with codecs.open(verbs_file, encoding='utf8') as verbs_file:
				self.verbs = list(reversed([verb.strip() for verb in verbs_file if verb]))
				self.bons = set([verb.split('#')[0] for verb in self.verbs])
				self.verbe = set([bon +'ه' for bon in self.bons] + ['ن'+ bon +'ه' for bon in self.bons])

	def tokenize(self, text):
		text = self.pattern.sub(r' \1 ', text.replace('\n', ' '))
		tokens = [word for word in text.split(' ') if word]
		if self._join_verb_parts:
			tokens = self.join_verb_parts(tokens)
		return tokens

	def join_verb_parts(self, tokens):
		"""
		>>> tokenizer = WordTokenizer()
		>>> tokenizer.join_verb_parts(['خواهد', 'رفت'])
		['خواهد_رفت']
		>>> tokenizer.join_verb_parts(['رفته', 'است'])
		['رفته_است']
		>>> tokenizer.join_verb_parts(['گفته', 'شده', 'است'])
		['گفته_شده_است']
		>>> tokenizer.join_verb_parts(['گفته', 'خواهد', 'شد'])
		['گفته_خواهد_شد']
		>>> tokenizer.join_verb_parts(['خسته', 'شدید'])
		['خسته', 'شدید']
		"""

		result = ['']
		for token in reversed(tokens):
			if token in self.before_verbs or (result[-1] in self.after_verbs and token in self.verbe):
				result[-1] = token +'_'+ result[-1]
			else:
				result.append(token)
		return list(reversed(result[1:]))
