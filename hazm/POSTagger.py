# coding: utf8

from __future__ import unicode_literals
from nltk.tag import stanford


class POSTagger(stanford.POSTagger):
	def __init__(self, *args, **kwargs):
		kwargs['encoding'] = 'utf8'
		if 'path_to_model' not in kwargs:
			kwargs['path_to_model'] = 'resources/persian.tagger'
		if 'path_to_jar' not in kwargs:
			kwargs['path_to_jar'] = 'resources/stanford-postagger.jar'

		self._SEPARATOR = '/'
		super(stanford.POSTagger, self).__init__(*args, **kwargs)

	def tag_sents(self, sentences):
		"""
		>>> tagger.tag(['من', 'به', 'مدرسه', 'رفته بودم', '.'])
		[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]
		"""

		refined = map(lambda s: [w.replace(' ', '_') for w in s], sentences)
		return super(stanford.POSTagger, self).tag_sents(refined)
