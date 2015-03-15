# coding: utf8

from __future__ import print_function, unicode_literals
import os, codecs, tempfile
from nltk.parse import DependencyGraph
from nltk.parse.malt import MaltParser


class DependencyParser(MaltParser):
	"""
	>>> from hazm import POSTagger, Lemmatizer
	>>> parser = DependencyParser(tagger=POSTagger(model='resources/postagger.model'), lemmatizer=Lemmatizer())
	>>> parser.parse(['من', 'به', 'مدرسه', 'رفته بودم', '.']).tree().pprint()
	(رفته_بودم من (به مدرسه) .)
	"""

	def __init__(self, tagger, lemmatizer, model_file='langModel.mco', working_dir='resources'):
		os.environ['MALT_PARSER'] = working_dir
		super(DependencyParser, self).__init__(tagger=tagger, mco=model_file, working_dir=working_dir)
		self.lemmatize = lemmatizer.lemmatize if lemmatizer else lambda w, t: '_'

	def parse_sents(self, sentences, verbose=False):
		tagged_sentences = self.tagger.tag_sents(sentences)
		return self.tagged_parse_sents(tagged_sentences, verbose)

	def tagged_parse_sents(self, sentences, verbose=False):
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
