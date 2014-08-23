# coding: utf8

from __future__ import unicode_literals
from nltk.chunk import RegexpParser, tree2conlltags


class Chunker(RegexpParser):
	"""
		>>> tree2brackets(chunker.parse([('نامه', 'Ne'), ('۱۰', 'NUM'), ('فوریه', 'Ne'), ('شما', 'PRO'), ('را', 'POSTP'), ('دریافت', 'N'), ('داشتم', 'V'), ('.', 'PUNC')]))
		'[نامه ۱۰ فوریه شما NP] [را POSTP] [دریافت داشتم VP] .'


		# VP

		>>> tree2brackets(chunker.parse([('تقدیم', 'Ne'), ('حضورتان', 'N'), ('نمایم', 'V')]))
		'[تقدیم حضورتان NP] [نمایم VP]'

		>>> tree2brackets(chunker.parse([('به', 'P'), ('سه', 'NUM'), ('رأی', 'N'), ('افزایش', 'N'), ('می‌یابد', 'V')]))
		'[به PP] [سه رأی NP] [افزایش می‌یابد VP]'

		>>> tree2brackets(chunker.parse([('عملیات', 'Ne'), ('نظامی', 'AJe'), ('روسیه', 'N'), ('را', 'POSTP'), ('در', 'P'), ('چچن', 'N'), ('محکوم', 'AJ'), ('کردند', 'V')]))
		'[عملیات نظامی روسیه NP] [را POSTP] [در PP] [چچن NP] [محکوم کردند VP]'

		>>> tree2brackets(chunker.parse([('در', 'P'), ('مورد', 'Ne'), ('پیوستن', 'Ne'), ('آنها', 'PRO'), ('به', 'P'), ('اتحادیه', 'N'), ('است', 'V')]))
		'[در PP] [مورد پیوستن آنها NP] [به PP] [اتحادیه NP] [است VP]'


		# ADJP

		>>> tree2brackets(chunker.parse([('از', 'P'), ('خط', 'Ne'), ('جبهه', 'Ne'), ('اولیه', 'AJ'), ('ناگزیر', 'AJ'), ('به', 'P'), ('فرود', 'Ne'), ('اجباری', 'AJ'), ('شده‌اند', 'V')]))
		'[از PP] [خط جبهه اولیه NP] [ناگزیر به ADJP] [فرود اجباری NP] [شده‌اند VP]'

		>>> tree2brackets(chunker.parse([('پیروزی', 'Ne'), ('مشترکمان', 'AJ'), ('بر', 'P'), ('ستمگران', 'Ne')]))
		'[پیروزی مشترکمان NP] [بر PP] [ستمگران NP]'

	"""

	def __init__(self):
		grammar = r"""

			VP:
				<N|AJ|POSTP>{<N|AJ><V>}
				{<V>}

			ADVP:
				{<ADV><AJ>?}

			ADJP:
				<.*[^e]>{<AJe?><Pe?>}

			NP:
				{<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?|AJe?|PRO|CL|RESe?>*}
				<N>}{<Ne?>

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
