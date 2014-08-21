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
		[('من', 'PR'), ('به', 'PREP'), ('مدرسه', 'N'), ('رفته بودم', 'V'), ('.', 'PUNC')]
		"""

		replace_spaces = lambda sentence: [word.replace(' ', '_') for word in sentence]
		return super(stanford.POSTagger, self).tag_sents(map(replace_spaces, sentences))
