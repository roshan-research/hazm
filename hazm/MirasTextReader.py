# coding: utf-8

from __future__ import unicode_literals
import codecs


class MirasTextReader():
	"""
	interfaces [MirasText Corpus](https://github.com/miras-tech/MirasText) that you must download and extract it.

	>>> miras_text = MirasTextReader(filename='corpora/MirasText.txt')
	>>> next(miras_text.texts())[:42]  # first 42 characters of fitst text
	'ایرانی‌ها چقدر از اینترنت استفاده می‌کنند؟'
	"""

	def __init__(self, filename):
		self._filename = filename

	def docs(self):
		for line in codecs.open(self._filename, encoding='utf-8'):
			parts = line.split('***')
			# todo: extract link, tags, ...
			yield {'text': parts[0].strip()}

	def texts(self):
		for doc in self.docs():
			yield doc['text']
