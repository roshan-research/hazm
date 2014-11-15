# coding: utf8

from __future__ import unicode_literals
import re

from .Tokenizer import *



class StatementTokenizer(Tokenizer):
	## tried to keep the frequency order of delimiters (in Persian texts)
	## to improve the performance
	delimiters = [
		'\n',
		'،' ,
		'.',
		'\t',
		':',
		'\r',
		#'/',
		')',
		'(',
		'«',
		'»',
		'؛',
		'ـ',
		'"',
		'؟',
		'*',
		',',
		'[',
		']',
		'!',
		'=',
		'+',
		'_',
		'–',
		'>',
		'<',
		'%',## FIXME
		';',
		'…',
		'”',
		'?',
		'&',
		'“',
		'\'',
		'#',
		'^',
		'}',
		'{',
		'$',## FIXME
		'@',
		'﴿',
		'﴾',
		'٪',## FIXME
		'~',
		'`',
		'\\',
		#'\x0b',## almost never used
		#'\x0c',## almost never used
		#'-',## FIXME
	]

	word_delimiters = [
		' ',
		'-',
		'ـ',
		'|',
		'٬',
		'0',
		'2',
		'1',
		'3',
		'4',
		'5',
		'6',
		'7',
		'8',
		'9',
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
		Tokenizer.__init__(self)
		self.word_pattern = re.compile(escapeSeq(self.word_delimiters))
	def deepTokenize(self, text):
		stats = []
		for stat in self.splitPattern(self.pattern, text):
			stat_words = self.splitPattern(self.word_pattern, stat)
			if not stat_words:
				continue
			stats.append(stat_words)
		return stats












