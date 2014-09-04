# coding: utf8

from __future__ import unicode_literals
from nltk.chunk import RegexpParser, tree2conlltags


class Chunker(RegexpParser):
	"""
		>>> tree2brackets(chunker.parse([('نامه', 'Ne'), ('۱۰', 'NUM'), ('فوریه', 'Ne'), ('شما', 'PRO'), ('را', 'POSTP'), ('دریافت', 'N'), ('داشتم', 'V'), ('.', 'PUNC')]))
		'[نامه ۱۰ فوریه شما NP] [را POSTP] [دریافت داشتم VP] .'
	"""

	def __init__(self):
		grammar = r"""

			NP:
				<P>{<N>}<V>

			VP:
				<.*[^e]>{<N>?<V>}
				{<V>}

			ADVP:
				{<ADVe?><AJ>?}

			ADJP:
				<.*[^e]>{<AJe?>}

			NP:
				{<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?|AJe?|PRO|CL|RESe?>*}
				<N>}{<.*e?>

			ADJP:
				{<AJe?>}

			POSTP:
				{<POSTP>}

			PP:
				{<Pe?>+}

		"""

		super(Chunker, self).__init__(grammar=grammar)


def tree2brackets(tree):
	str, tag = '', ''
	for item in tree2conlltags(tree):
		if item[2][0] in {'B', 'O'} and tag:
			str += tag +'] '
			tag = ''

		if item[2][0] == 'B':
			tag = item[2].split('-')[1]
			str += '['
		str += item[0] +' '

	if tag:
		str += tag +'] '

	return str.strip()
