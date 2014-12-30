# coding: utf8

from __future__ import unicode_literals
from nltk.tag.api import TaggerI
from wapiti import Model


class SequenceTagger(TaggerI):
	""" wrapper for [Wapiti](http://wapiti.limsi.fr) sequence tagger

	>>> tagger = SequenceTagger(patterns=['*', 'U:word-%x[0,0]'])
	>>> tagger.train([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
	>>> tagger.tag_sents([['من', 'به', 'مدرسه', 'رفته_بودم', '.']])
	[[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]]

	>>> tagger.save_model('test.tagger')
	>>> SequenceTagger(model='test.tagger').tag_sents([['من', 'به', 'مدرسه', 'رفته_بودم', '.']])
	[[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]]
	"""

	def __init__(self, patterns=[], **options):
		self.model = Model(patterns='\n'.join(patterns), **options)

	def train(self, sentences):
		self.model.train(['\n'.join([' '.join(word) for word in sentence]) for sentence in sentences])

	def save_model(self, filename):
		self.model.save(filename)

	def tag_sents(self, sentences):
		lines = '\n\n'.join(['\n'.join(sentence) for sentence in sentences])
		results = self.model.label_sequence(lines).decode('utf8')
		tags = iter(results.strip().split('\n'))
		return [[(word, next(tags)) for word in sentence] for sentence in sentences]
