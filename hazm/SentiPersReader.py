# coding: utf-8

from __future__ import unicode_literals, print_function
import os, sys, itertools
from xml.dom import minidom


class SentiPersReader():
	"""
	interfaces [SentiPers Corpus](http://nlp.guilan.ac.ir/Dataset.aspx)

	>>> sentipers = SentiPersReader(root='corpora/sentipers')
	>>> next(sentipers.comments())[0][1]
	'بيشتر مناسب است براي کساني که به دنبال تنوع هستند و در همه چيز نو گرايي دارند .'
	"""

	def __init__(self, root):
		self._root = root

	def docs(self):

		def element_sentences(element):
			for sentence in element.getElementsByTagName('Sentence'):
				yield {'text': sentence.childNodes[0].data, 'id': sentence.getAttribute('ID'), 'value': int(sentence.getAttribute('Value')) if comment.getAttribute('Value') else None}

		for root, dirs, files in os.walk(self._root):
			for filename in sorted(files):
				try:
					elements = minidom.parse(os.path.join(root, filename))

					product = elements.getElementsByTagName('Product')[0]
					doc = {
						'Title': product.getAttribute('Title'),
						'Type': product.getAttribute('Type'),
						'comments': [],
					}

					for child in product.childNodes:
						if child.nodeName in {'Voters', 'Performance', 'Capability', 'Production_Quality', 'Ergonomics', 'Purchase_Value'}:
							value = child.getAttribute('Value')
							doc[child.nodeName] = float(value) if '.' in value else int(value)

					for comment in itertools.chain(elements.getElementsByTagName('Opinion'), elements.getElementsByTagName('Criticism')):
						doc['comments'].append({
							'id': comment.getAttribute('ID'),
							'type': comment.nodeName,
							'author': comment.getAttribute('Holder').strip(),
							'value': int(comment.getAttribute('Value')) if comment.getAttribute('Value') else None,
							'sentences': list(element_sentences(comment))
						})

					# todo: Accessories, Features, Review, Advantages, Tags, Keywords, Index

					yield doc

				except Exception as e:
					print('error in reading', filename, e, file=sys.stderr)

	def comments(self):
		for doc in self.docs():
			yield [[sentence['text'] for sentence in text] for text in [comment['sentences'] for comment in doc['comments']]]
