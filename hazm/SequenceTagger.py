# coding: utf-8

from __future__ import unicode_literals
from nltk.tag.api import TaggerI
from nltk.metrics import accuracy


class SequenceTagger(TaggerI):
	""" wrapper for [Wapiti](http://wapiti.limsi.fr) sequence tagger

	>>> tagger = SequenceTagger(patterns=['*', 'u:word-%x[0,0]'])
	>>> tagger.train([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
	>>> tagger.tag_sents([['من', 'به', 'مدرسه', 'رفته_بودم', '.']])
	[[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]]

	>>> tagger.save_model('resources/test.model')
	>>> SequenceTagger(model='resources/test.model').tag_sents([['من', 'به', 'مدرسه', 'رفته_بودم', '.']])
	[[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]]
	"""

	def __init__(self, patterns=[], **options):
		from wapiti import Model
		self.model = Model(patterns='\n'.join(patterns), **options)

	def train(self, sentences):
		self.model.train(['\n'.join([' '.join(word) for word in sentence]) for sentence in sentences])

	def save_model(self, filename):
		self.model.save(filename)

	def tag(self, tokens):
		return self.tag_sents([tokens])[0]

	def tag_sents(self, sentences):
		sentences = list(sentences)
		lines = '\n\n'.join(['\n'.join(sentence) for sentence in sentences]).replace(' ', '_')
		results = self.model.label_sequence(lines).decode('utf8')
		tags = iter(results.strip().split('\n'))
		return [[(word, next(tags)) for word in sentence] for sentence in sentences]


class IOBTagger(SequenceTagger):
	""" wrapper for [Wapiti](http://wapiti.limsi.fr) sequence tagger

	>>> tagger = IOBTagger(patterns=['*', 'U:word-%x[0,0]', 'U:word-%x[0,1]'])
	>>> tagger.train([[('من', 'PRO', 'B-NP'), ('به', 'P', 'B-PP'), ('مدرسه', 'N', 'B-NP'), ('رفته_بودم', 'V', 'B-VP'), ('.', 'PUNC', 'O')]])
	>>> tagger.tag_sents([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
	[[('من', 'PRO', 'B-NP'), ('به', 'P', 'B-PP'), ('مدرسه', 'N', 'B-NP'), ('رفته_بودم', 'V', 'B-VP'), ('.', 'PUNC', 'O')]]
	"""

	def tag_sents(self, sentences):
		sentences = list(sentences)
		lines = '\n\n'.join(['\n'.join(['\t'.join(word) for word in sentence]) for sentence in sentences]).replace(' ', '_')
		results = self.model.label_sequence(lines).decode('utf8')
		tags = iter(results.strip().split('\n'))
		return [[word + (next(tags),) for word in sentence] for sentence in sentences]

	def evaluate(self, gold):
		tagged_sents = self.tag_sents(([word[:-1] for word in sentence] for sentence in gold))
		return accuracy(sum(gold, []), sum(tagged_sents, []))
