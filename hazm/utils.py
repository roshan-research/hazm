
import six

if six.PY2:
	u = lambda s: s.decode('utf8')
else:
	u = lambda s: s
