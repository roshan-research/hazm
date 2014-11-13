# coding: utf8

from __future__ import unicode_literals
import re

from .Tokenizer import Tokenizer



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



