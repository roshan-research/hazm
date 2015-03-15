# coding: utf8

from __future__ import print_function, unicode_literals
import codecs, subprocess
from collections import Counter
from itertools import islice
from nltk.tag import untag
from nltk.parse import DependencyEvaluator
from sklearn.cross_validation import train_test_split
from hazm import *
from hazm.Chunker import tree2brackets
from hazm.PeykareReader import coarse_pos_e as peykare_coarse_pos_e
from hazm.DadeganReader import coarse_pos_e as dadegan_coarse_pos_e


def create_words_file(dic_file='resources/persian.dic', output='hazm/data/words.dat'):
	""" prepares list of persian word words from [Virastyar](https://sourceforge.net/projects/virastyar/) dic file.
	"""

	dic_words = sorted([line.split('\t')[0] for line in codecs.open(dic_file, encoding='utf8')])
	print(*dic_words, sep='\n', file=codecs.open(output, 'w', 'utf8'))
	print(output, 'created')


def evaluate_lemmatizer(conll_file='resources/train.conll', peykare_root='corpora/peykare'):
	lemmatizer = Lemmatizer()

	errors = []
	with codecs.open('resources/lemmatizer_errors.txt', 'w', 'utf8') as output:
		dadegan = DadeganReader(conll_file)
		for tree in dadegan.trees():
			for node in tree.nodelist[1:]:
				word, lemma, pos = node['word'], node['lemma'], node['mtag']
				if lemmatizer.lemmatize(word, pos) != lemma:
					errors.append((word, lemma, pos, lemmatizer.lemmatize(word, pos)))
		print(len(errors), 'errors', file=output)
		counter = Counter(errors)
		for item, count in sorted(counter.items(), key=lambda t: t[1], reverse=True):
			print(count, *item, file=output)

	missed = []
	with codecs.open('resources/lemmatizer_missed.txt', 'w', 'utf8') as output:
		peykare = PeykareReader(peykare_root)
		for sentence in peykare.sents():
			for word in sentence:
				if word[1] == 'V':
					if word[0] == lemmatizer.lemmatize(word[0]):
						missed.append(word[0])
		print(len(missed), 'missed', file=output)
		counter = Counter(missed)
		for item, count in sorted(counter.items(), key=lambda t: t[1], reverse=True):
			print(count, item, file=output)


def evaluate_chunker(treebank_root='corpora/treebank'):
	treebank = TreebankReader(treebank_root, join_clitics=True, join_verb_parts=True)
	chunker = Chunker()
	chunked_trees = list(treebank.chunked_trees())

	print(chunker.evaluate(chunked_trees))

	output = codecs.open('resources/chunker_errors.txt', 'w', 'utf8')
	for sentence, gold in zip(treebank.sents(), chunked_trees):
		chunked = chunker.parse(sentence)
		if chunked != gold:
			print(tree2brackets(chunked), file=output)
			print(tree2brackets(gold), file=output)
			print(file=output)


def train_postagger(peykare_root='corpora/peykare', model_file='resources/postagger.model', test_size=.1, sents_limit=None, pos_map=peykare_coarse_pos_e):

	tagger = SequencePOSTagger(type='crf', algo='rprop', compact=True, patterns=[
		'*',

		'u:wll=%x[-2,0]',
		'u:wl=%x[-1,0]',
		'u:w=%x[0,0]',
		'u:wr=%x[1,0]',
		'u:wrr=%x[2,0]',

		# 'u:w2l=%x[-1,0]/%x[0,0]',
		# 'u:w2r=%x[0,0]/%x[1,0]',

		'*:p1=%m[0,0,"^.?"]',
		'*:p2=%m[0,0,"^.?.?"]',
		'*:p3=%m[0,0,"^.?.?.?"]',

		'*:s1=%m[0,0,".?$"]',
		'*:s2=%m[0,0,".?.?$"]',
		'*:s3=%m[0,0,".?.?.?$"]',

		'*:p?l=%t[-1,0,"\p"]',
		'*:p?=%t[0,0,"\p"]',
		'*:p?r=%t[1,0,"\p"]',
		'*:p?a=%t[0,0,"^\p*$"]',

		'*:n?l=%t[-1,0,"\d"]',
		'*:n?=%t[0,0,"\d"]',
		'*:n?r=%t[1,0,"\d"]',
		'*:n?a=%t[0,0,"^\d*$"]',
	])

	peykare = PeykareReader(peykare_root, pos_map=pos_map)
	train_sents, test_sents = train_test_split(list(islice(peykare.sents(), sents_limit)), test_size=test_size, random_state=0)

	tagger.train(train_sents)
	tagger.save_model(model_file)

	print(tagger.evaluate(test_sents))


def train_chunker(train_file='corpora/train.conll', dev_file='corpora/dev.conll', test_file='corpora/test.conll', model_file='resources/chunker.model', pos_map=dadegan_coarse_pos_e):

	tagger = POSTagger(model='resources/postagger.model')
	chunker = Chunker(type='crf', algo='l-bfgs', compact=True, patterns=[
		'*',

		'u:wll=%x[-2,0]',
		'u:wl=%x[-1,0]',
		'u:w=%x[0,0]',
		'u:wr=%x[1,0]',
		'u:wrr=%x[2,0]',

		'*:tll=%x[-2,1]',
		'*:tl=%x[-1,1]',
		'*:t=%x[0,1]',
		'*:tr=%x[1,1]',
		'*:trr=%x[2,1]',
	])

	def retag_trees(trees, sents):
		for tree, sentence in zip(trees, tagger.tag_sents(map(untag, sents))):
			for (n, word) in zip(tree.treepositions('leaves'), sentence):
				tree[n] = word

	train, test = DadeganReader(train_file, pos_map=pos_map), DadeganReader(test_file, pos_map=pos_map)
	train_trees = list(train.chunked_trees())
	retag_trees(train_trees, train.sents())
	chunker.train(train_trees)
	chunker.save_model(model_file)

	test_trees = list(test.chunked_trees())
	retag_trees(test_trees, test.sents())
	print(chunker.evaluate(test_trees))


def train_maltparser(train_file='corpora/train.conll', dev_file='corpora/dev.conll', test_file='corpora/test.conll', model_file='langModel.mco', path_to_jar='resources/malt.jar', options_file='resources/malt-options.xml', features_file='resources/malt-features.xml', memory_min='-Xms7g', memory_max='-Xmx8g'):

	lemmatizer, tagger = Lemmatizer(), POSTagger(model='resources/postagger.model')

	train, test = DadeganReader(train_file), DadeganReader(test_file)
	train_data = train_file +'.data'
	with codecs.open(train_data, 'w', 'utf8') as output:
		for tree, sentence in zip(train.trees(), tagger.tag_sents(map(untag, train.sents()))):
			for i, (node, word) in enumerate(zip(list(tree.nodes.values())[1:], sentence), start=1):
				node['mtag'] = word[1]
				node['lemma'] = lemmatizer.lemmatize(node['word'], node['mtag'])
				print(i, node['word'].replace(' ', '_'), node['lemma'].replace(' ', '_'), node['mtag'], node['mtag'], '_', node['head'], node['rel'], '_', '_', sep='\t', file=output)
			print(file=output)

	subprocess.Popen(['java', memory_min, memory_max, '-jar', path_to_jar, '-w', 'resources', '-c', model_file, '-i', train_data, '-f', options_file, '-F', features_file, '-m', 'learn']).wait()

	# evaluation
	parser = DependencyParser(tagger=tagger, lemmatizer=lemmatizer, model_file=model_file)
	parsed_trees = parser.parse_sents(map(untag, test.sents()))

	test_data, test_results = test_file +'.data', test_file +'.results'
	print('\n'.join([tree.to_conll(10) for tree in test.trees()]).strip(), file=codecs.open(test_data, 'w', 'utf8'))
	print('\n'.join([tree.to_conll(10) for tree in parsed_trees]).strip(), file=codecs.open(test_results, 'w', 'utf8'))
	subprocess.Popen(['java', '-jar', 'resources/MaltEval.jar', '-g', test_data, '-s', test_results]).wait()


def train_stanford_postagger(peykare_root='corpora/peykare', path_to_model='resources/persian.tagger', path_to_jar='resources/stanford-postagger.jar', properties_file='resources/stanford-postagger.props', memory_min='-Xms1g', memory_max='-Xmx6g', test_size=.1, pos_map=peykare_coarse_pos_e):
	peykare = PeykareReader(peykare_root, pos_map=pos_map)
	train_file = 'resources/tagger_train_data.txt'
	train, test = train_test_split(list(peykare.sents()), test_size=test_size, random_state=0)

	output = codecs.open(train_file, 'w', 'utf8')
	for sentence in train:
		print(*(map(lambda w: '/'.join(w).replace(' ', '_'), sentence)), file=output)
	subprocess.Popen(['java', memory_min, memory_max, '-classpath', path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-prop', properties_file, '-model', path_to_model,  '-trainFile', train_file, '-tagSeparator', '/', '-search', 'owlqn2']).wait()

	tagger = StanfordPOSTagger(path_to_jar=path_to_jar, path_to_model=path_to_model)
	print(tagger.evaluate(test))
