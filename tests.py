import inspect, doctest
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

for name, object in modules.items():
	doctest.testmod(inspect.getmodule(object), extraglobs={name: object})

doctest.testfile('README.md')
