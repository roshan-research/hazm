# coding: utf-8

from __future__ import print_function
import os, sys, re
from xml.dom import minidom


class TNewsReader():
	"""
	interfaces [TNews Corpus](http://datasets.tnews.ir/downloads/) that you must download and extract.

	>>> tnews = TNewsReader(root='corpora/tnews')
	>>> next(tnews.docs())['id']
	'14092303482300013653'
	"""

	def __init__(self, root):
		self._root = root
		self.cleaner = re.compile(r'<[^<>]+>')

	def docs(self):
		def get_text(element):
			raw_html = element.childNodes[0].data if element.childNodes else ''
			cleaned_text = re.sub(self.cleaner, '', raw_html)
			return cleaned_text

		for root, dirs, files in os.walk(self._root):
			for name in sorted(files):

				try:
					content = open(os.path.join(root, name)).read()

					# fix xml formating issue
					content = re.sub(r'[]', '', content).replace('</TNews>', '') + '</TNews>'

					elements = minidom.parseString(content)
					for element in elements.getElementsByTagName('NEWS'):
						doc = {}
						doc['id'] = get_text(element.getElementsByTagName('NEWSID')[0])
						doc['url'] = get_text(element.getElementsByTagName('URL')[0])
						doc['datetime'] = get_text(element.getElementsByTagName('UTCDATE')[0])
						doc['category'] = get_text(element.getElementsByTagName('CATEGORY')[0])
						doc['pre-title'] = get_text(element.getElementsByTagName('PRETITLE')[0])
						doc['title'] = get_text(element.getElementsByTagName('TITLE')[0])
						doc['post-title'] = get_text(element.getElementsByTagName('POSTTITLE')[0])
						doc['brief'] = get_text(element.getElementsByTagName('BRIEF')[0])
						doc['text'] = get_text(element.getElementsByTagName('DESCRIPTION')[0])
						yield doc

				except Exception as e:
					print('error in reading', name, e, file=sys.stderr)

	def texts(self):
		for doc in self.docs():
			yield doc['text']
