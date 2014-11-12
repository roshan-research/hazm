# coding: utf8

from __future__ import unicode_literals
import re

from .Tokenizer import Tokenizer



class StatementTokenizer(Tokenizer):
	delimiters = [
		'\n',
		'\t',
		'\r',
		'\x0b',
		'\x0c',
		######
		'!',
		'"',
		'#',
		'$',
		'%',
		'&',
		'\'',
		'(',
		')',
		'*',
		'+',
		',',
		#'-',## FIXME
		'.',
		'/',
		':',
		';',
		'<',
		'=',
		'>',
		'?',
		'@',
		'[',
		'\\',
		']',
		'^',
		'_',
		'`',
		'{',
		'}',
		'~',
		######
		'؛',
		'؟',
		'…',
		'«',
		'»',
		'ـ',
		'،' ,
		'–',
		'“',
		'”',
		'٪',
		'﴿',
		'﴾',
		######
	]



