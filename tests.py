# coding: utf8

from __future__ import unicode_literals
import sys, inspect, doctest, unittest
from hazm import *

modules = {
	'peykare': PeykareReader,
	'bijankhan': BijankhanReader,
	'hamshahri': HamshahriReader,
	'dadegan': DadeganReader,
	'valency': VerbValencyReader,
	'treebank': TreebankReader,
	'sentence_tokenizer': SentenceTokenizer,
	'word_tokenizer': WordTokenizer,
	'normalizer': Normalizer,
	'stemmer': Stemmer,
	'lemmatizer': Lemmatizer,
	'tagger': SequenceTagger,
	'postagger': POSTagger,
	'chunker': Chunker,
	'parser': DependencyParser
}


class UnicodeOutputChecker(doctest.OutputChecker):

	def check_output(self, want, got, optionflags):
		try:
			want, got = eval(want), eval(got)
		except:
			pass

		try:
			got = got.decode('unicode-escape')
			want = want.replace('آ', 'ا')  # decode issue
		except:
			pass

		if type(want) == unicode:
			want = want.replace('٫', '.')  # eval issue

		return want == got


if __name__ == '__main__':
	# test all modules if no one specified
	all_modules = len(sys.argv) < 2

	suites = []
	checker = UnicodeOutputChecker() if utils.PY2 else None
	for name, object in modules.items():
		if all_modules or name in sys.argv:
			suites.append(doctest.DocTestSuite(inspect.getmodule(object), checker=checker))

	if not utils.PY2 and all_modules:
		suites.append(doctest.DocFileSuite('README.md'))

	failure = False
	runner = unittest.TextTestRunner(verbosity=2)
	for suite in suites:
		if not runner.run(suite).wasSuccessful():
			failure = True

	if failure:
		exit(1)
