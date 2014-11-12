# coding: utf8

from __future__ import unicode_literals
import re

from .Tokenizer import Tokenizer

class SentenceTokenizer(Tokenizer):
	delimiters = [
		'!',
		'.',
		'?',
		'⸮',
		'؟',
		'\n',
	]

	def tokenize(self, text):
		## overriding from parent class just to add the doc
		"""
		>>> sentence_tokenizer.tokenize('جدا کردن ساده است. تقریبا البته!')
		['جدا کردن ساده است.', 'تقریبا البته!']
		"""
		
		return Tokenizer.tokenize(self, text)


