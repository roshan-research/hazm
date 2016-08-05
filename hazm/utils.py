# coding: utf8

import sys
from os import path

PY2 = sys.version_info[0] == 2

data_path = path.join(path.dirname(__file__), 'data')
default_words = path.join(data_path, 'words.dat')
default_stop_words = path.join(data_path, 'stopwords.dat')
default_verbs = path.join(data_path, 'verbs.dat')
informal_words = path.join(data_path, 'iwords.dat')
informal_verbs = path.join(data_path, 'iverbs.dat')

NUMBERS = '۰۱۲۳۴۵۶۷۸۹'

maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))