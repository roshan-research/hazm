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
	with codecs.open(words_file, encoding='utf8') as words_file:
		return list(map(lambda w: w.strip(), words_file))


def stopwords_list(stopwords_file=default_stopwords):
	return words_list(stopwords_file)
