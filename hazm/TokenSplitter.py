# coding: utf-8

from __future__ import unicode_literals
from .Lemmatizer import Lemmatizer


class TokenSplitter():
	def __init__(self):
		self.lemmatizer = Lemmatizer()
		self.lemmatize = self.lemmatizer.lemmatize
		self.words = self.lemmatizer.words

	def split_token_words(self, token):
		"""
		>>> splitter = TokenSplitter()
		>>> splitter.split_token_words('صداوسیماجمهوری')
		[('صداوسیما', 'جمهوری')]
		>>> splitter.split_token_words('صداو')
		[('صد', 'او'), ('صدا', 'و')]
		>>> splitter.split_token_words('شهرموشها')
		[('شهر', 'موشها')]
		>>> splitter.split_token_words('داستان‌سرا')
		[('داستان', 'سرا'), ('داستان‌سرا',)]
		>>> splitter.split_token_words('دستان‌سرا')
		[('دستان', 'سرا')]
		"""

		candidates = []
		if '‌' in token:
			candidates.append(tuple(token.split('‌')))

		splits = [(token[:s], token[s:]) for s in range(1, len(token)) if token[s-1] != '‌' and token[s] != '‌'] + [(token, )]
		candidates.extend(list(filter(lambda tokens: set(map(self.lemmatize, tokens)).issubset(self.words), splits)))

		return candidates
