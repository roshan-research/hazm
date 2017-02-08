# coding: utf-8

from __future__ import print_function, unicode_literals
import os, codecs, tempfile
from nltk.parse import DependencyGraph
from nltk.parse.api import ParserI
from nltk.parse.malt import MaltParser


class MaltParser(MaltParser):
	"""
	interfaces [MaltParser](http://www.maltparser.org/)
	"""

	def __init__(self, tagger, lemmatizer, working_dir='resources', model_file='langModel.mco'):
		self.tagger = tagger
		self.working_dir = working_dir
		self.mco = model_file
		self._malt_bin = os.path.join(working_dir, 'malt.jar')
		self.lemmatize = lemmatizer.lemmatize if lemmatizer else lambda w, t: '_'

	def parse_sents(self, sentences, verbose=False):
		tagged_sentences = self.tagger.tag_sents(sentences)
		return self.parse_tagged_sents(tagged_sentences, verbose)

	def parse_tagged_sents(self, sentences, verbose=False):
		input_file = tempfile.NamedTemporaryFile(prefix='malt_input.conll', dir=self.working_dir, delete=False)
		output_file = tempfile.NamedTemporaryFile(prefix='malt_output.conll', dir=self.working_dir, delete=False)

		try:
			for sentence in sentences:
				for i, (word, tag) in enumerate(sentence, start=1):
					word = word.strip()
					if not word:
						word = '_'
					input_file.write(('\t'.join([str(i), word.replace(' ', '_'), self.lemmatize(word, tag).replace(' ', '_'), tag, tag, '_', '0', 'ROOT', '_', '_', '\n'])).encode('utf8'))
				input_file.write('\n\n'.encode('utf8'))
			input_file.close()

			cmd = ['java', '-jar', self._malt_bin, '-w', self.working_dir, '-c', self.mco, '-i', input_file.name, '-o', output_file.name, '-m', 'parse']
			if self._execute(cmd, verbose) != 0:
				raise Exception("MaltParser parsing failed: %s" % (' '.join(cmd)))

			return (DependencyGraph(item) for item in codecs.open(output_file.name, encoding='utf8').read().split('\n\n') if item.strip())

		finally:
			input_file.close()
			os.remove(input_file.name)
			output_file.close()
			os.remove(output_file.name)


class TurboParser(ParserI):
	"""
	interfaces [TurboParser](http://www.ark.cs.cmu.edu/TurboParser/) which you must manually install
	"""

	def __init__(self, tagger, lemmatizer, model_file):
		self.tagger = tagger
		self.lemmatize = lemmatizer.lemmatize if lemmatizer else lambda w, t: '_'

		import turboparser
		self._pturboparser = turboparser.PTurboParser()
		self.interface = self._pturboparser.create_parser()
		self.interface.load_parser_model(model_file)

	def parse_sents(self, sentences):
		tagged_sentences = self.tagger.tag_sents(sentences)
		return self.tagged_parse_sents(tagged_sentences)

	def tagged_parse_sents(self, sentences):
		input_file = tempfile.NamedTemporaryFile(prefix='turbo_input.conll', dir='resources', delete=False)
		output_file = tempfile.NamedTemporaryFile(prefix='turbo_output.conll', dir='resources', delete=False)

		try:
			for sentence in sentences:
				for i, (word, tag) in enumerate(sentence, start=1):
					word = word.strip()
					if not word:
						word = '_'
					input_file.write(('\t'.join([str(i), word.replace(' ', '_'), self.lemmatize(word, tag).replace(' ', '_'), tag, tag, '_', '0', 'ROOT', '_', '_', '\n'])).encode('utf8'))
				input_file.write('\n'.encode('utf8'))
			input_file.close()

			self.interface.parse(input_file.name, output_file.name)

			return (DependencyGraph(item, cell_extractor=lambda cells: cells[1:8]) for item in codecs.open(output_file.name, encoding='utf8').read().split('\n\n') if item.strip())

		finally:
			input_file.close()
			os.remove(input_file.name)
			output_file.close()
			os.remove(output_file.name)


class DependencyParser(MaltParser):
	"""
	>>> from hazm import POSTagger, Lemmatizer
	>>> parser = DependencyParser(tagger=POSTagger(model='resources/postagger.model'), lemmatizer=Lemmatizer())
	>>> parser.parse(['من', 'به', 'مدرسه', 'رفته بودم', '.']).tree().pprint()
	(رفته_بودم من (به مدرسه) .)
	"""
