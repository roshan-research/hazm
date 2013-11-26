
import six
from os import path


if six.PY2:
	u = lambda s: s.decode('utf8')
else:
	u = lambda s: s


data_path = path.join(path.dirname(__file__), 'data')
default_words = path.join(data_path, 'words.dat')
default_verbs = path.join(data_path, 'verbs.dat')
