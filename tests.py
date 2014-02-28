
import sys, inspect, doctest, unittest
from hazm import BijankhanReader, HamshahriReader, SentenceTokenizer, WordTokenizer, Normalizer, Stemmer, Lemmatizer, POSTagger, DependencyParser

modules = {
	'bijankhan': BijankhanReader(),
	'hamshahri': HamshahriReader(),
	'sentence_tokenizer': SentenceTokenizer(),
	'word_tokenizer': WordTokenizer(),
	'normalizer': Normalizer(),
	'stemmer': Stemmer(),
	'lemmatizer': Lemmatizer(),
	'tagger': POSTagger(),
	'parser': DependencyParser(tagger=POSTagger())
}

decode = lambda s: s.decode('utf8')

class UnicodeOutputChecker(doctest.OutputChecker):

	def check_output(self, want, got, optionflags):
		want, got = eval(want), eval(got)

		if type(want) == str:
			want = decode(want)
		elif type(want) == list:
			if type(want[0]) == str:
				want = map(decode, want)
			elif type(want[0]) == tuple:
				want = map(lambda t: tuple(map(decode, t)), want)

		return want == got

PY2 = sys.version_info[0] == 2
if PY2:
	checker = UnicodeOutputChecker()
else:
	checker = None

suites = []
for name, object in modules.items():
	suites.append(doctest.DocTestSuite(inspect.getmodule(object), extraglobs={name: object}, checker=checker))

if not PY2:
	suites.append(doctest.DocFileSuite('README.md'))

runner = unittest.TextTestRunner(verbosity=2)
for suite in suites:
	runner.run(suite)
