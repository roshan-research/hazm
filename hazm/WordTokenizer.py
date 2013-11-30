#coding=utf8

from __future__ import unicode_literals
import re, codecs
from .utils import default_verbs
from nltk.tokenize.api import TokenizerI


class WordTokenizer(TokenizerI):
	def __init__(self, verbs_file=default_verbs, join_verb_parts=True):
		self._join_verb_parts = join_verb_parts
		self.pattern = re.compile(r'([!:\.،؛؟»\]\)\}«\[\(\{\?]+)')

		if join_verb_parts:
			self.after_verbs = set([
				'ام', 'ای', 'است', 'ایم', 'اید', 'اند', 'بودم', 'بودی', 'بود', 'بودیم', 'بودید', 'بودند', 'باشم', 'باشی', 'باشد', 'باشیم', 'باشید', 'باشند',
				'شده ام', 'شده ای', 'شده است', 'شده ایم', 'شده اید', 'شده اند', 'شده بودم', 'شده بودی', 'شده بود', 'شده بودیم', 'شده بودید', 'شده بودند', 'شده باشم', 'شده باشی', 'شده باشد', 'شده باشیم', 'شده باشید', 'شده باشند',
				'نشده ام', 'نشده ای', 'نشده است', 'نشده ایم', 'نشده اید', 'نشده اند', 'نشده بودم', 'نشده بودی', 'نشده بود', 'نشده بودیم', 'نشده بودید', 'نشده بودند', 'نشده باشم', 'نشده باشی', 'نشده باشد', 'نشده باشیم', 'نشده باشید', 'نشده باشند',
				'شوم', 'شوی', 'شود', 'شویم', 'شوید', 'شوند', 'شدم', 'شدی', 'شد', 'شدیم', 'شدید', 'شدند',
				'نشوم', 'نشوی', 'نشود', 'نشویم', 'نشوید', 'نشوند', 'نشدم', 'نشدی', 'نشد', 'نشدیم', 'نشدید', 'نشدند',
				'می‌شوم', 'می‌شوی', 'می‌شود', 'می‌شویم', 'می‌شوید', 'می‌شوند', 'می‌شدم', 'می‌شدی', 'می‌شد', 'می‌شدیم', 'می‌شدید', 'می‌شدند',
				'نمی‌شوم', 'نمی‌شوی', 'نمی‌شود', 'نمی‌شویم', 'نمی‌شوید', 'نمی‌شوند', 'نمی‌شدم', 'نمی‌شدی', 'نمی‌شد', 'نمی‌شدیم', 'نمی‌شدید', 'نمی‌شدند',
				'خواهم شد', 'خواهی شد', 'خواهد شد', 'خواهیم شد', 'خواهید شد', 'خواهند شد',
				'نخواهم شد', 'نخواهی شد', 'نخواهد شد', 'نخواهیم شد', 'نخواهید شد', 'نخواهند شد',
			])

			self.before_verbs = set([
				'خواهم', 'خواهی', 'خواهد', 'خواهیم', 'خواهید', 'خواهند',
				'نخواهم', 'نخواهی', 'نخواهد', 'نخواهیم', 'نخواهید', 'نخواهند'
			])

			self.verbs = list(reversed([verb.strip() for verb in codecs.open(verbs_file, encoding='utf8') if verb]))
			self.verbe = set([verb.split('#')[0] + 'ه' for verb in self.verbs])

	def tokenize(self, text):
		"""
		>>> tokenizer.tokenize('این جمله معمولی است.')
		['این', 'جمله', 'معمولی', 'است', '.']
		"""

		text = self.pattern.sub(r' \1', text)
		tokens = [word for word in text.split(' ') if word]
		if self._join_verb_parts:
			tokens = self.join_verb_parts(tokens)
		return tokens

	def join_verb_parts(self, tokens):
		"""
		>>> tokenizer.join_verb_parts(['خواهد', 'رفت'])
		['خواهد رفت']
		>>> tokenizer.join_verb_parts(['رفته', 'است'])
		['رفته است']
		>>> tokenizer.join_verb_parts(['گفته', 'شده', 'است'])
		['گفته شده است']
		>>> tokenizer.join_verb_parts(['گفته', 'خواهد', 'شد'])
		['گفته خواهد شد']
		>>> tokenizer.join_verb_parts(['خسته', 'شدید'])
		['خسته', 'شدید']
		"""

		result = ['']
		for token in reversed(tokens):
			if token in self.before_verbs or (result[-1] in self.after_verbs and token in self.verbe):
				result[-1] = token +' '+ result[-1]
			else:
				result.append(token)
		return list(reversed(result[1:]))


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'tokenizer': WordTokenizer(join_verb_parts=True)})
