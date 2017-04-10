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
		"""

		candidates = [(token[:s], token[s:]) for s in range(1, len(token))] + [(token, )]
		candidates = list(filter(lambda tokens: set(map(self.lemmatize, tokens)).issubset(self.words), candidates))

		return candidates
