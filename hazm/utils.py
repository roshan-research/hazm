
import sys
from os import path
from collections import Counter

PY2 = sys.version_info[0] == 2
data_path = path.join(path.dirname(__file__), 'data')
default_words = path.join(data_path, 'words.dat')
default_verbs = path.join(data_path, 'verbs.dat')

def FreqDict(text):
    words = Counter()
    words.update(text.split())
    return words.most_common()
