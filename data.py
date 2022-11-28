# coding: utf-8

from __future__ import print_function, unicode_literals
import codecs, subprocess, random
import multiprocessing
from collections import Counter
from itertools import islice
from nltk.tag import untag
from sklearn.model_selection import train_test_split
from hazm import *
from hazm.Chunker import tree2brackets
from hazm.PeykareReader import coarse_pos_e as peykare_coarse_pos_e
from hazm.DadeganReader import coarse_pos_e as dadegan_coarse_pos_e
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models import FastText
from gensim.utils import simple_preprocess
from gensim.test.utils import datapath
from hazm import Normalizer



def create_words_file(dic_file='resources/persian.dic', output='hazm/data/words.dat'):
	""" prepares list of persian word words from [Virastyar](https://sourceforge.net/projects/virastyar/) dic file. """

	dic_words = [line.strip().replace(', ', ',').split('\t') for line in codecs.open(dic_file, encoding='utf-8') if len(line.strip().split('\t')) == 3]
	dic_words = filter(lambda item: not item[2].startswith('V') and 'NEG' not in item[2], dic_words)
	dic_words = ['\t'.join(item) for item in sorted(dic_words, key=lambda item: item[0])]
	print(*dic_words, sep='\n', file=codecs.open(output, 'w', 'utf-8'))
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


def evaluate_normalizer(tnews_root='corpora/tnews'):

	tnews = TNewsReader(root=tnews_root)
	normalizer = Normalizer(persian_style=False, persian_numbers=False, remove_diacritics=False, token_based=False, affix_spacing=True)
	token_normalizer = Normalizer(persian_style=False, persian_numbers=False, remove_diacritics=False, token_based=True, affix_spacing=False)

	with codecs.open('resources/normalized.txt', 'w', 'utf8') as output1, codecs.open('resources/normalized_token_based.txt', 'w', 'utf8') as output2:
		random.seed(0)
		for text in tnews.texts():
			if random.randint(0, 100) != 0:
				continue

			for sentence in sent_tokenize(text):
				print(normalizer.normalize(sentence), '\n', file=output1)
				print(token_normalizer.normalize(sentence), '\n', file=output2)


def evaluate_informal_normalizer(sentipars_root='corpora/sentipers'):
	sentipers = SentiPersReader(root=sentipars_root)
	normalizer = Normalizer()
	informal_normalizer = InformalNormalizer()

	output = codecs.open('resources/normalized.txt', 'w', 'utf8')
	for comments in sentipers.comments():
		for comment in comments:
			for sentence in comment:
				print(normalizer.normalize(sentence), file=output)
				sents = informal_normalizer.normalize(sentence)
				sents = [[word[0] for word in sent] for sent in sents]
				sents = [' '.join(sent) for sent in sents]
				text = '\n'.join(sents)
				text = normalizer.normalize(text)
				print(text, file=output)
				print(file=output)


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

	tagger = POSTagger(type='crf', algo='rprop', compact=True, patterns=[
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


def train_chunker(train_file='corpora/train.conll', dev_file='corpora/dev.conll', test_file='corpora/test.conll', model_file='resources/chunker.model'):

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

	train, test = DadeganReader(train_file), DadeganReader(test_file)
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
	parser = MaltParser(tagger=tagger, lemmatizer=lemmatizer, model_file=model_file)
	parsed_trees = parser.parse_sents(map(untag, test.sents()))

	test_data, test_results = test_file +'.data', test_file +'.results'
	print('\n'.join([tree.to_conll(10) for tree in test.trees()]).strip(), file=codecs.open(test_data, 'w', 'utf8'))
	print('\n'.join([tree.to_conll(10) for tree in parsed_trees]).strip(), file=codecs.open(test_results, 'w', 'utf8'))
	subprocess.Popen(['java', '-jar', 'resources/MaltEval.jar', '-g', test_data, '-s', test_results]).wait()


def train_turboparser(train_file='corpora/train.conll', dev_file='corpora/dev.conll', test_file='corpora/test.conll', model_file='resources/turboparser.model'):

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

	subprocess.Popen(['./resources/TurboParser', '--train', '--file_train='+train_data, '--file_model='+model_file, '--logtostderr']).wait()

	# evaluation
	parser = TurboParser(tagger=tagger, lemmatizer=lemmatizer, model_file=model_file)
	parsed_trees = parser.parse_sents(map(untag, test.sents()))

	test_data, test_results = test_file +'.data', test_file +'.results'
	print('\n'.join([tree.to_conll(10) for tree in test.trees()]).strip(), file=codecs.open(test_data, 'w', 'utf8'))
	print('\n'.join([tree.to_conll(10) for tree in parsed_trees]).strip(), file=codecs.open(test_results, 'w', 'utf8'))
	subprocess.Popen(['java', '-jar', 'resources/MaltEval.jar', '-g', test_data, '-s', test_results, '--pattern', '0.####', '--Metric', 'LAS;UAS']).wait()


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


class SentenceEmbeddingCorpus:

    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        corpus_path = datapath(self.data_path)
        normalizer = Normalizer()
        for i, list_of_words in enumerate(open(corpus_path)):
            yield TaggedDocument(word_tokenize(normalizer.normalize(list_of_words)), [i])


def train_sentence_embedding(dataset_path, model_file='sent_embedding.model',min_count=5, workers=multiprocessing.cpu_count()-1, windows=5, vector_size=300, epochs=10, return_model=False):
	workers = 1 if workers == 0 else workers
	doc = SentenceEmbeddingCorpus(dataset_path)
	model = Doc2Vec(min_count=min_count,
         window=windows,
         vector_size=vector_size,
         workers=workers,
        )
	model.build_vocab(doc)
	model.train(doc, total_examples=model.corpus_count, epochs=epochs)
	model.save(model_file)
	if return_model:
		return model
	else:
		print('Model trained.')


class WordEmbeddingCorpus:

    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        corpus_path = datapath(self.data_path)
        normalizer = Normalizer()
        for line in open(corpus_path):
            yield simple_preprocess(normalizer.normalize(line))


def train_word_embedding(dataset_path, dest_path='word_embedding.model',min_count=5, workers=multiprocessing.cpu_count()-1, windows=5, vector_size=200, epochs=10, return_model=False):
	workers = 1 if workers == 0 else workers
	doc = WordEmbeddingCorpus(dataset_path)
	model = FastText(min_count=min_count,
         window=windows,
         vector_size=vector_size,
         workers=workers,
        )
	model.build_vocab(doc)
	model.train(doc, total_examples=model.corpus_count, epochs=epochs)
	model.save(dest_path)
	if return_model:
		return model
	else:
		print('Model trained.s')

