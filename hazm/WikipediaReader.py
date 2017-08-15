# coding: utf-8

from __future__ import unicode_literals, print_function
import re, subprocess


class WikipediaReader():
	"""
	interfaces [Persian Wikipedia dump](http://download.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2)
	"""

	def __init__(self, fawiki_dump, wiki_extractor='resources/WikiExtractor.py'):
		self.wiki_extractor = wiki_extractor
		self.fawiki_dump = fawiki_dump

	def docs(self):
		proc = subprocess.Popen(['python', self.wiki_extractor, '--no-templates', '--output', '-', self.fawiki_dump], stdout=subprocess.PIPE)
		doc_pattern = re.compile(r'<doc id="(\d+)" url="([^\"]+)" title="([^\"]+)">')

		doc = []
		for line in iter(proc.stdout.readline, ''):
			line = line.strip().decode('utf8')
			if line:
				doc.append(line)

			if line == '</doc>':
				del doc[1]
				id, url, title = doc_pattern.match(doc[0]).groups()
				html = '\n'.join(doc[1:-1])

				yield {'id': id, 'url': url, 'title': title, 'html': html, 'text': html}
				doc = []

	def texts(self):
		for doc in self.docs():
			yield doc['text']
