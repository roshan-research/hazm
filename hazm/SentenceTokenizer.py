# coding: utf8

from __future__ import unicode_literals
import re
from nltk.tokenize.api import TokenizerI


class SentenceTokenizer(TokenizerI):
	def __init__(self):
		self.pattern = re.compile(r'([!\.\?⸮؟]+)[ \n]+')

	def tokenize(self, text):
		"""
		>>> sentence_tokenizer.tokenize('جدا کردن ساده است. تقریبا البته!')
		['جدا کردن ساده است.', 'تقریبا البته!']
		"""

		text = self.pattern.sub(r'\1\n\n', text)
		return [sentence.replace('\n', ' ').strip() for sentence in text.split('\n\n') if sentence.strip()]
