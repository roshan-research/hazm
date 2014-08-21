# coding: utf8

from __future__ import print_function, unicode_literals
import codecs, subprocess
from collections import Counter
from nltk.parse import DependencyGraph
from sklearn.cross_validation import train_test_split
from hazm import *
from hazm.Chunker import tree2brackets


def dadegan_text(conll_file='resources/train.conll'):
	text = codecs.open(conll_file, encoding='utf8').read()
	return text.replace('‌‌','‌').replace('\t‌','\t').replace('‌\t','\t').replace('\t ','\t').replace(' \t','\t').replace('\r', '').replace('\u2029', '‌')


def create_words_file(dic_file='resources/persian.dic', output='hazm/data/words.dat'):
	""" prepares list of persian word words from [Virastyar dic](https://sourceforge.net/projects/virastyar/files/Data/1.3.1/persian.dic/download) file.
	"""

	dic_words = sorted([line.split('\t')[0] for line in codecs.open(dic_file, encoding='utf8')])
	print(*dic_words, sep='\n', file=codecs.open(output, 'w', 'utf8'))
	print(output, 'created')


def evaluate_lemmatizer(conll_file='resources/train.conll', bijankhan_file='resources/bijankhan.txt'):
	lemmatizer = Lemmatizer()

	errors = []
	output = codecs.open('resources/lemmatizer_errors.txt', 'w', 'utf8')
	for line in dadegan_text(conll_file).split('\n'):
		parts = line.split('\t')
		if len(parts) < 10:
			continue
		word, lemma, pos = parts[1], parts[2], parts[3]
		if lemmatizer.lemmatize(word, pos) != lemma:
			errors.append((word, lemma, pos, lemmatizer.lemmatize(word, pos)))
	print(len(errors), 'errors', file=output)
	counter = Counter(errors)
	for item, count in sorted(counter.items(), key=lambda t: t[1], reverse=True):
		print(count, *item, file=output)

	missed = []
	output = codecs.open('resources/lemmatizer_missed.txt', 'w', 'utf8')
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

	print(chunker.evaluate(treebank.chunked_trees()))

	output = codecs.open('resources/chunker_errors.txt', 'w', 'utf8')
	for sentence, gold in zip(treebank.sents(), treebank.chunked_trees()):
		chunked = chunker.parse(sentence)
		if chunked != gold:
			print(tree2brackets(chunked), file=output)
			print(tree2brackets(gold), file=output)
			print(file=output)


def train_pos_tagger(peykare_root='corpora/peykare', path_to_model='resources/persian.tagger', path_to_jar='resources/stanford-postagger.jar', properties_file='resources/persian.tagger.props', memory_min='-Xms1g', memory_max='-Xmx8g', test_size=.1):
	peykare = PeykareReader(peykare_root)
	train_file = 'resources/tagger_train_data.txt'
	train, test = train_test_split(list(peykare.sents()), test_size=test_size, random_state=0)

	output = codecs.open(train_file, 'w', 'utf8')
	for sentence in train:
		print(*(map(lambda w: '/'.join(w).replace(' ', '_'), sentence)), file=output)
	subprocess.Popen(['java', memory_min, memory_max, '-classpath', path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-prop', properties_file, '-model', path_to_model,  '-trainFile', train_file, '-tagSeparator', '/', '-search', 'owlqn2']).wait()

	tagger = POSTagger()
	print('\n\n', 'Tagger Accuracy on Test Split:', tagger.evaluate(test))


def train_dependency_parser(train_file='resources/train.conll', test_file='resources/test.conll', model_file='langModel.mco', path_to_jar='resources/malt.jar', options_file='resources/options.xml', features_file='resources/features.xml', memory_min='-Xms7g', memory_max='-Xmx8g'):

	def read_conll(conll_file):
		trees = [DependencyGraph(item) for item in dadegan_text(conll_file).replace(' ', '_').split('\n\n') if item.strip()]
		sentences = [[node['word'] for node in tree.nodelist[1:]] for tree in trees]
		return trees, sentences

	lemmatizer, tagger = Lemmatizer(), POSTagger()

	trees, sentences = read_conll(train_file)
	tagged = tagger.batch_tag(sentences)

	train_data = train_file +'.data'
	with codecs.open(train_data, 'w', 'utf8') as output:
		for tree, sentence in zip(trees, tagged):
			for i, (node, word) in enumerate(zip(tree.nodelist[1:], sentence), start=1):
				node['tag'] = word[1]
				node['lemma'] = lemmatizer.lemmatize(node['word'].replace('_', ' '), node['tag'])
				print(i, node['word'].replace(' ', '_'), node['lemma'].replace(' ', '_'), node['tag'], node['tag'], '_', node['head'], node['rel'], '_', '_', sep='\t', file=output)
			print(file=output)

	cmd = ['java', memory_min, memory_max, '-jar', path_to_jar, '-w', 'resources', '-c', model_file, '-i', train_data, '-f', options_file, '-F', features_file, '-m', 'learn']
	process = subprocess.Popen(cmd)
	process.wait()

	# evaluation
	print('\nEvaluating trained model on test data:')
	parser = DependencyParser(tagger=tagger, model_file=model_file)

	trees, sentences = read_conll(test_file)
	tagged = tagger.batch_tag(sentences)
	parsed = parser.tagged_batch_parse(tagged)

	test_data, test_results = test_file +'.data', test_file +'.results'
	print('\n'.join([sentence.to_conll(10) for sentence in trees]).strip(), file=codecs.open(test_data, 'w', 'utf8'))
	print('\n'.join([sentence.to_conll(10) for sentence in parsed]).strip(), file=codecs.open(test_results, 'w', 'utf8'))

	cmd = ['java', '-jar', 'resources/MaltEval.jar', '-g', test_data, '-s', test_results]
	process = subprocess.Popen(cmd)
	process.wait()
