# coding: utf-8

import sys, codecs
from os import path

PY2 = sys.version_info[0] == 2

data_path = path.join(path.dirname(__file__), 'data')
default_words = path.join(data_path, 'words.dat')
default_stopwords = path.join(data_path, 'stopwords.dat')
default_verbs = path.join(data_path, 'verbs.dat')
informal_words = path.join(data_path, 'iwords.dat')
informal_verbs = path.join(data_path, 'iverbs.dat')

NUMBERS = '۰۱۲۳۴۵۶۷۸۹'

maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))


def words_list(words_file=default_words):
	with codecs.open(words_file, encoding='utf-8') as words_file:
		items = [line.strip().split('\t') for line in words_file]
		return [(item[0], int(item[1]), tuple(item[2].split(','))) for item in items if len(item) == 3]


def stopwords_list(stopwords_file=default_stopwords):
	with codecs.open(stopwords_file, encoding='utf8') as stopwords_file:
		return list(map(lambda w: w.strip(), stopwords_file))
