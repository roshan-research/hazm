
from __future__ import print_function
import os, sys, codecs
from hazm import Lemmatizer, POSTagger


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

def train_pos_tagger(model_name, bijankhan_file='resources/bijankhan.txt', use_cpos=False, properties_file='resources/persian-left3words-distsim.tagger.props', path_to_jar='resources/stanford-postagger.jar'):
	bijankhan = BijankhanReader(bijankhan_file)
	temp_file = 'resources/tagger_data.txt'
	output = codecs.open(temp_file, 'w', 'utf8')
	for sent in bijankhan.sents(use_cpos):
		print(sent, file=output)
	POSTagger.train(train_file=temp_file, model_name=model_name, properties_file=properties_file, path_to_jar=path_to_jar)
	#os.remove(temp_file)