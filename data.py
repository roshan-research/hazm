#encoding=utf8

from __future__ import print_function, unicode_literals
import os, sys, codecs, subprocess, itertools
from collections import Counter
from nltk.parse import DependencyGraph
from hazm import Lemmatizer, BijankhanReader, POSTagger


def dadegan_text(conll_file='resources/train.conll'):
	text = codecs.open(conll_file, encoding='utf8').read()
	return text.replace('‌‌','‌').replace('\t‌','\t').replace('‌\t','\t').replace('\t ','\t').replace(' \t','\t').replace('\r', '').replace('\u2029', '‌')


def create_words_file(dic_file='resources/persian.dic', output='hazm/data/words.dat'):
	""" prepares list of persian word words from [Virastyar dic](https://sourceforge.net/projects/virastyar/files/Data/1.3.1/persian.dic/download) file.
	"""

	dic_words = [line.split('\t')[0] for line in codecs.open(dic_file, encoding='utf8')]
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


def train_pos_tagger(bijankhan_file='resources/bijankhan.txt', path_to_model='resources/persian.tagger', path_to_jar='resources/stanford-postagger.jar', properties_file='resources/persian.tagger.props', memory_min='-Xms1g', memory_max='-Xmx2g', test_split=.1):
	bijankhan = BijankhanReader(bijankhan_file)
	train_file = 'resources/tagger_train_data.txt'
	output = codecs.open(train_file, 'w', 'utf8')
	sentences = list(bijankhan.sents())
	train_part = int(len(sentences) * (1 - test_split))

	for sentence in sentences[:train_part]:
		print(*(map(lambda w: '/'.join(w).replace(' ', '_'), sentence)), file=output)
	cmd = ['java', memory_min, memory_max, '-classpath', path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-prop', properties_file, '-model', path_to_model,  '-trainFile', train_file, '-tagSeparator', '/', '-search', 'owlqn2']
	process = subprocess.Popen(cmd)
	process.wait()

	tagger = POSTagger()
	print('\n\n', 'Tagger Accuracy on Test Split:', tagger.evaluate(sentences[train_part:]))


def train_dependency_parser(conll_file='resources/train.conll', model_file='langModel.mco', path_to_jar='resources/malt.jar', options_file='resources/options.xml', features_file='resources/features.xml', memory_min='-Xms7g', memory_max='-Xmx8g'):
	lemmatizer, tagger = Lemmatizer(), POSTagger()
	train_file = 'resources/parser_train_data.conll'
	output = codecs.open(train_file, 'w', 'utf8')
	nodelists = [DependencyGraph(item).nodelist[1:] for item in dadegan_text(conll_file).replace(' ', '_').split('\n\n')]

	sentences = [[node['word'] for node in nodelist] for nodelist in nodelists]
	tagged = tagger.batch_tag(sentences)

	for nodelist, sentence in zip(nodelists, tagged):
		for i, (node, word) in enumerate(zip(nodelist, sentence), start=1):
			node['tag'] = word[1]
			node['lemma'] = lemmatizer.lemmatize(node['word'].replace('_', ' '), node['tag'])
			print(i, node['word'].replace(' ', '_'), node['lemma'].replace(' ', '_'), node['tag'], node['tag'], '_', node['head'], node['rel'], '_', '_', sep='\t', file=output)
		print(file=output)

	cmd = ['java', memory_min, memory_max, '-jar', path_to_jar, '-w', 'resources', '-c', model_file, '-i', train_file, '-f', options_file, '-F', features_file, '-m', 'learn']
	process = subprocess.Popen(cmd)
	process.wait()
