# coding: utf8

from __future__ import print_function, unicode_literals
import codecs, subprocess
from collections import Counter
from sklearn.cross_validation import train_test_split
from hazm import *
from hazm.Chunker import tree2brackets


def create_words_file(dic_file='resources/persian.dic', output='hazm/data/words.dat'):
	""" prepares list of persian word words from [Virastyar](https://sourceforge.net/projects/virastyar/) dic file.
	"""

	dic_words = sorted([line.split('\t')[0] for line in codecs.open(dic_file, encoding='utf8')])
	print(*dic_words, sep='\n', file=codecs.open(output, 'w', 'utf8'))
	print(output, 'created')


def evaluate_lemmatizer(conll_file='resources/train.conll', bijankhan_file='resources/bijankhan.txt'):
	lemmatizer = Lemmatizer()

	errors = []
	with codecs.open('resources/lemmatizer_errors.txt', 'w', 'utf8') as output:
		dadegan = DadeganReader(conll_file)
		for tree in dadegan.trees():
			for node in tree.nodelist[1:]:
				word, lemma, pos = node['word'], node['lemma'], node['ctag']
				if lemmatizer.lemmatize(word, pos) != lemma:
					errors.append((word, lemma, pos, lemmatizer.lemmatize(word, pos)))
		print(len(errors), 'errors', file=output)
		counter = Counter(errors)
		for item, count in sorted(counter.items(), key=lambda t: t[1], reverse=True):
			print(count, *item, file=output)

	missed = []
	with codecs.open('resources/lemmatizer_missed.txt', 'w', 'utf8') as output:
		bijankhan = BijankhanReader(bijankhan_file)
		for sentence in bijankhan.sents():
			for word in sentence:
				if word[1] == 'V':
					if word[0] == lemmatizer.lemmatize(word[0]):
						missed.append(word[0])
		print(len(missed), 'missed', file=output)
		counter = Counter(missed)
		for item, count in sorted(counter.items(), key=lambda t: t[1], reverse=True):
			print(count, item, file=output)


def evaluate_chunker(treebank_root='corpora/treebank'):
	treebank = TreebankReader(treebank_root)
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


def train_postagger(peykare_root='corpora/peykare', path_to_model='resources/persian.tagger', path_to_jar='resources/stanford-postagger.jar', properties_file='resources/stanford-postagger.props', memory_min='-Xms1g', memory_max='-Xmx6g', test_size=.1):
	peykare = PeykareReader(peykare_root)
	train_file = 'resources/tagger_train_data.txt'
	train, test = train_test_split(list(peykare.sents()), test_size=float(test_size), random_state=0)
	print('Peykare loaded.')

	output = codecs.open(train_file, 'w', 'utf8')
	for sentence in train:
		print(*(map(lambda w: '/'.join(w).replace(' ', '_'), sentence)), file=output)
	subprocess.Popen(['java', memory_min, memory_max, '-classpath', path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-prop', properties_file, '-model', path_to_model,  '-trainFile', train_file, '-tagSeparator', '/', '-search', 'owlqn2']).wait()

	tagger = POSTagger()
	print('Tagger Accuracy on Test Split:')
	print(tagger.evaluate(test))


def train_maltparser(train_file='resources/train.conll', validation_file='resources/validation.conll', test_file='resources/test.conll', model_file='langModel.mco', path_to_jar='resources/malt.jar', options_file='resources/malt-options.xml', features_file='resources/malt-features.xml', memory_min='-Xms7g', memory_max='-Xmx8g'):

	lemmatizer, tagger = Lemmatizer(), POSTagger()
	train, validation, test = DadeganReader(train_file), DadeganReader(validation_file), DadeganReader(test_file)
	train_sents = list(train.sents()) + list(validation.sents())
	train_trees = list(train.trees()) + list(validation.trees())

	train_data = train_file +'.data'
	with codecs.open(train_data, 'w', 'utf8') as output:
		for tree, sentence in zip(train_trees, tagger.tag_sents(train_sents)):
			for i, (node, word) in enumerate(zip(tree.nodelist[1:], sentence), start=1):
				node['tag'] = word[1]
				node['lemma'] = lemmatizer.lemmatize(node['word'].replace('_', ' '), node['tag'])
				print(i, node['word'].replace(' ', '_'), node['lemma'].replace(' ', '_'), node['tag'], node['tag'], '_', node['head'], node['rel'], '_', '_', sep='\t', file=output)
			print(file=output)

	subprocess.Popen(['java', memory_min, memory_max, '-jar', path_to_jar, '-w', 'resources', '-c', model_file, '-i', train_data, '-f', options_file, '-F', features_file, '-m', 'learn']).wait()

	# evaluation
	print('\nEvaluating trained model on test data:')
	parser = DependencyParser(tagger=tagger, model_file=model_file)

	tagged = tagger.tag_sents(test.sents())
	parsed = parser.tagged_parse_sents(tagged)

	test_data, test_results = test_file +'.data', test_file +'.results'
	print('\n'.join([sentence.to_conll(10).replace('/', '') for sentence in test.trees()]).strip(), file=codecs.open(test_data, 'w', 'utf8'))
	print('\n'.join([sentence.to_conll(10) for sentence in parsed]).strip(), file=codecs.open(test_results, 'w', 'utf8'))

	subprocess.Popen(['java', '-jar', 'resources/MaltEval.jar', '-g', test_data, '-s', test_results]).wait()
