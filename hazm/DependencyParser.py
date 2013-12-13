#coding=utf8

from __future__ import print_function
import os, codecs
from .Lemmatizer import Lemmatizer
from .POSTagger import POSTagger
from nltk.parse.malt import MaltParser


class DependencyParser(MaltParser):
	def __init__(self, tagger, lemmatizer=Lemmatizer(), model_file='langModel.mco', working_dir='resources'):
		os.environ['MALTPARSERHOME'] = working_dir
		super(DependencyParser, self).__init__(tagger=tagger, mco=model_file, working_dir=working_dir)
		self.lemmatizer = lemmatizer

	def tagged_batch_parse(self, sentences, verbose=False):
		"""
		>>> parser.parse(['من', 'به', 'مدرسه', 'رفته بودم', '.'])
		"""

		input_file, output_file = os.path.join(self.working_dir, 'malt_input.conll'), os.path.join(self.working_dir, 'malt_output.conll')

		if self.lemmatizer:
			lemmatize = self.lemmatizer.lemmatize
		else:
			lemmatize = lambda w: '_'

		_input = codecs.open(input_file, 'w', 'utf8')
		for sentence in sentences:
			for i, (word, tag) in enumerate(sentence, start=1):
				print(i, word.replace(' ', '_'), lemmatize(word).replace(' ', '_'), tag, tag, '_', '0', 'ROOT', '_', '_', sep='\t', file=_input)
			print(file=_input)

		cmd = ['java', '-jar', self._malt_bin, '-w', self.working_dir, '-c', self.mco, '-i', input_file, '-o', output_file, '-m', 'parse']
		if self._execute(cmd, verbose) != 0:
			raise Exception("MaltParser parsing failed: %s" % (' '.join(cmd)))

		return DependencyGraph.load(codecs.open(output_file, encoding='utf8'))


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'parser': DependencyParser(tagger=POSTagger())})
