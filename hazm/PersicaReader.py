# coding: utf-8

from __future__ import print_function
import codecs


class PersicaReader():
	"""
	interfaces [Persica Corpus](https://sourceforge.net/projects/persica/)

	>>> persica = PersicaReader('corpora/persica.csv')
	>>> next(persica.docs())['id']
	843656
	"""

	def __init__(self, csv_file):
		self._csv_file = csv_file

	def docs(self):
		lines = []
		for line in codecs.open(self._csv_file, encoding='utf-8-sig'):
			line = line.strip()
			if line:
				if line.endswith(','):
					lines.append(line[:-1])
				else:
					lines.append(line)
					yield {
						'id': int(lines[0]),
						'title': lines[1],
						'text': lines[2],
						'date': lines[3],
						'time': lines[4],
						'category': lines[5],
						'category2': lines[6],
					}
					lines = []

	def texts(self):
		for doc in self.docs():
			yield doc['text']
