# coding: utf-8

from __future__ import unicode_literals
from nltk.tag import stanford
from .SequenceTagger import SequenceTagger


class POSTagger(SequenceTagger):
	"""
	>>> tagger = POSTagger(model='resources/postagger.model')
	>>> tagger.tag(['من', 'به', 'مدرسه', 'رفته_بودم', '.'])
	[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]
	"""


class StanfordPOSTagger(stanford.StanfordPOSTagger):
	"""
	>>> tagger = StanfordPOSTagger(model_filename='resources/persian.tagger', path_to_jar='resources/stanford-postagger.jar')
	>>> tagger.tag(['من', 'به', 'مدرسه', 'رفته_بودم', '.'])
	[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]
	"""

	def __init__(self, model_filename, path_to_jar, *args, **kwargs):
		self._SEPARATOR = '/'
		super(stanford.StanfordPOSTagger, self).__init__(model_filename=model_filename, path_to_jar=path_to_jar, *args, **kwargs)

	def tag(self, tokens):
		return self.tag_sents([tokens])[0]

	def tag_sents(self, sentences):
		refined = map(lambda s: [w.replace(' ', '_') for w in s], sentences)
		return super(stanford.StanfordPOSTagger, self).tag_sents(refined)
