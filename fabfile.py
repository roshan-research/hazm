
from __future__ import print_function
import os, sys, codecs, subprocess, itertools
from hazm import Lemmatizer, BijankhanReader, POSTagger


def create_words_file(dic_file='resources/persian.dic', output='hazm/data/words.dat'):
	""" prepares list of persian word words from [Virastyar dic](https://sourceforge.net/projects/virastyar/files/Data/1.3.1/persian.dic/download) file.
	"""

	dic_words = [line.split('\t')[0] for line in codecs.open(dic_file, encoding='utf8')]
	print(*dic_words, sep='\n', file=codecs.open(output, 'w', 'utf8'))
	print(output, 'created')


def evaluate_lemmatizer(dependency_corpus='resources/dependency.conll'):
	lemmatizer = Lemmatizer()
	output = codecs.open('resources/lemmatizer_errors.txt', 'w', 'utf8')
	errors = []

	for line in codecs.open(dependency_corpus, encoding='utf8'):
		parts = line.split('\t')
		if len(parts) < 10:
			continue
		word, lemma, pos = parts[1], parts[2], parts[3]
		if lemmatizer.lemmatize(word, pos) != lemma:
			errors.append((word, lemma, lemmatizer.lemmatize(word)))

	print(len(errors), 'errors', file=output)
	from collections import Counter
	counter = Counter(errors)
	for item, count in sorted(counter.items(), key=lambda t: t[1], reverse=True):
		print(count, *item, file=output)


def train_pos_tagger(bijankhan_file='resources/bijankhan.txt', path_to_model='resources/persian.tagger', path_to_jar='resources/stanford-postagger.jar', memory_min='-Xms1g', memory_max='-Xmx2g'):
	bijankhan = BijankhanReader(bijankhan_file)
	train_file = 'resources/tagger_train_data.txt'
	output = codecs.open(train_file, 'w', 'utf8')
	for sentence in bijankhan.sents():
		print(*(map(lambda w: '/'.join(w).replace(' ', '_'), sentence)), file=output)
	properties_file='resources/persian-left3words.tagger.props' # only outputs properties
	cmd = ['java', memory_min, memory_max, '-classpath', path_to_jar, 'edu.stanford.nlp.tagger.maxent.MaxentTagger', '-prop', properties_file, '-model', path_to_model,  '-trainFile', train_file, '-tagSeparator', '/', '-search', 'owlqn2']
	subprocess.Popen(cmd)


def evaluate_pos_tagger(bijankhan_file='resources/bijankhan.txt', path_to_model='resources/persian.tagger', path_to_jar='resources/stanford-postagger.jar'):
	tagger = POSTagger()
	bijankhan = BijankhanReader(bijankhan_file)
	tests = list(itertools.islice(bijankhan.sents(), 0, 1000))
	print(tagger.evaluate(tests))
