# coding: utf8

from __future__ import unicode_literals
from nltk.chunk import RegexpParser, tree2conlltags


class Chunker(RegexpParser):
	"""
		>>> tree2brackets(chunker.parse([('نامه', 'Ne'), ('۱۰', 'NUM'), ('فوریه', 'Ne'), ('شما', 'PRO'), ('را', 'POSTP'), ('دریافت', 'N'), ('داشتم', 'V'), ('.', 'PUNC')]))
		'[نامه ۱۰ فوریه شما را NP] [دریافت داشتم VP] .'
	"""

	def __init__(self):
		grammar = r"""

			VP:
				{<N>?<V>}

			ADVP:
				{<ADV><AJ>?}

			NP:
				{<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?|AJe?|PRO|POSTP|CL|RESe?>*}
				<N>}{<Ne?>

			PP:
				{<Pe?>}

			ADJP:
				{<AJe?><Pe?>}

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

	return str.strip()
