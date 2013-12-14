#coding=utf8

from __future__ import print_function
import os, codecs
from .Lemmatizer import Lemmatizer
from .POSTagger import POSTagger
from nltk.parse import DependencyGraph
from nltk.parse.malt import MaltParser


class DependencyParser(MaltParser):
	def __init__(self, tagger, lemmatizer=Lemmatizer(), model_file='langModel.mco', working_dir='resources'):
		os.environ['MALTPARSERHOME'] = working_dir
		super(DependencyParser, self).__init__(tagger=tagger, mco=model_file, working_dir=working_dir)
		self.lemmatizer = lemmatizer

	def tagged_batch_parse(self, sentences, verbose=False):
		"""
		>>> parser.parse(['من', 'به', 'مدرسه', 'رفته بودم', '.']).tree().pprint()
		'(رفته_بودم من (به مدرسه) .)'
		"""

		input_filename, output_filename = os.path.join(self.working_dir, 'malt_input.conll'), os.path.join(self.working_dir, 'malt_output.conll')

		if self.lemmatizer:
			lemmatize = self.lemmatizer.lemmatize
		else:
			lemmatize = lambda w: '_'

		with codecs.open(input_filename, 'w', 'utf8') as input_file:
			for sentence in sentences:
				for i, (word, tag) in enumerate(sentence, start=1):
					print(i, word.replace(' ', '_'), lemmatize(word).replace(' ', '_'), tag, tag, '_', '0', 'ROOT', '_', '_', sep='\t', file=input_file)
				print(file=input_file)

		cmd = ['java', '-jar', self._malt_bin, '-w', self.working_dir, '-c', self.mco, '-i', input_filename, '-o', output_filename, '-m', 'parse']
		if self._execute(cmd, verbose) != 0:
			raise Exception("MaltParser parsing failed: %s" % (' '.join(cmd)))

		with codecs.open(output_filename, encoding='utf8') as output_file:
			return [DependencyGraph(item) for item in output_file.read().split('\n\n')]


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'parser': DependencyParser(tagger=POSTagger())})
