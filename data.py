
from __future__ import print_function
import sys, codecs
from hazm import Normalizer, Stemmer


def create_words_file(freqs_file='resources/word-freq-utf8.txt', output='data/words.dat'):
	"""
	"""

	words = []
	normalizer = Normalizer()
	stemmer = Stemmer()
	words_file = codecs.open(output, 'w', 'utf8')
	for line in codecs.open(freqs_file, 'r', 'utf8'):
		word, count = line.strip().split(',')
		if int(count) > 10:
			words.append(normalizer.normalize(word))

	word_set = set(words)
	for word in words:
		stem = stemmer.stem(word)
		if stem == word or stem not in word_set:
			print(word, file=words_file)

	print(output, 'created')


def create_verbs_file(valency_file='resources/valency.txt', output='data/verbs.dat'):
	"""
	"""

	verbs = []
	for l, line in enumerate(codecs.open(valency_file, 'r', 'utf8')):
		parts = line.split('\t')
		if l > 1 and len(parts) == 6:
			mazi, pishvand = parts[0], parts[2]

			if mazi != '-':
				verb = mazi if pishvand == '-' else pishvand + mazi
				if verb not in verbs:
					verbs.append(verb)

	print(*verbs, sep='\n', file=codecs.open(output, 'w', 'utf8'))
	print(output, 'created')


if __name__ == '__main__':
	if len(sys.argv) == 2:
		if sys.argv[1] == 'create_words_file':
			create_words_file()
		elif sys.argv[1] == 'create_verbs_file':
			create_verbs_file()
