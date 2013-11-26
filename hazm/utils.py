
import sys
from os import path
PY3 = sys.version_info.major == 3


if PY3:
	u = lambda s: s
	list_u = u
else:
	u = lambda s: s.decode('utf8')
	list_u = lambda l: map(u, l)


data_path = path.join(path.dirname(__file__), 'data')
default_words = path.join(data_path, 'words.dat')
default_verbs = path.join(data_path, 'verbs.dat')
