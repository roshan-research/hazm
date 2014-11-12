# coding: utf8

from __future__ import unicode_literals
import re
from nltk.tokenize.api import TokenizerI

from .utils import escapeSeq

ZWNJ = '\u200c'



class Tokenizer(TokenizerI):
	delimiters = [
	]

	digits = [
		'0',
		'1',
		'2',
		'3',
		'4',
		'5',
		'6',
		'7',
		'8',
		'9',
		######
		'۰',
		'۱',
		'۲',
		'۳',
		'۴',
		'۵',
		'۶',
		'۷',
		'۸',
		'۹',
	]

	def __init__(self):
		self.pattern = re.compile(escapeSeq(self.delimiters))

	def tokenize(self, text):
		tokens = []
		for token in self.pattern.split(text):
			token = token.strip()
			if token:
				tokens.append(token)
		return tokens



