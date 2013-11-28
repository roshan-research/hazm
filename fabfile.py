
from __future__ import print_function
import sys, codecs
from hazm import Lemmatizer


def create_words_file(dic_file='resources/persian.dic', output='hazm/data/words.dat'):
	""" prepares list of persian word words from [Virastyar dic](https://sourceforge.net/projects/virastyar/files/Data/1.3.1/persian.dic/download) file.
	"""

	dic_words = [line.split('\t')[0] for line in codecs.open(dic_file, encoding='utf8')]
	print(*dic_words, sep='\n', file=codecs.open(output, 'w', 'utf8'))
	print(output, 'created')


def create_verbs_file(valency_file='resources/valency.txt', output='hazm/data/verbs.dat'):
	""" prepares list of persian verbs from [Verb Valency](http://dadegan.ir/pervallex) corpus.
	"""

	verbs = []
	for l, line in enumerate(codecs.open(valency_file, encoding='utf8')):
		parts = line.split('\t')
		if l > 1 and len(parts) == 6:
			past, present = parts[0], parts[1]

			if past != '-':
				verb = past+'#'+present
				if verb not in verbs:
					verbs.append(verb)

	print(*verbs, sep='\n', file=codecs.open(output, 'w', 'utf8'))
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
