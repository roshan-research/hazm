# coding: utf8

from __future__ import unicode_literals
import codecs
from .utils import maketrans

buckwalter_transliteration = maketrans("'>&<}AbptvjHxd*rzs$SDTZEg_fqklmnhwYyFNKaui~o^#`{:@\"[;,.!-+%]", "\u0621\u0623\u0624\u0625\u0626\u0627\u0628\u0629\u062a\u062b\u062c\u062d\u062e\u062f\u0630\u0631\u0632\u0633\u0634\u0635\u0636\u0637\u0638\u0639\u063a\u0640\u0641\u0642\u0643\u0644\u0645\u0646\u0647\u0648\u0649\u064a\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0653\u0654\u0670\u0671\u06dc\u06df\u06e0\u06e2\u06e3\u06e5\u06e6\u06e8\u06ea\u06eb\u06ec\u06ed")


class QuranCorpusReader():
	"""
	interfaces [Quran Corpus](http://corpus.quran.com/download/) that you must download and extract it.

	>>> quran = QuranCorpusReader(quran_file='corpora/quranic-corpus-morphology.txt')
	>>> print(next(quran.words())[1])
	بِسْمِ
	"""

	def __init__(self, quran_file):
		self._quran_file = quran_file

	def parts(self):
		for line in codecs.open(self._quran_file):
			if not line.startswith('('):
				continue
			parts = line.strip().split('\t')

			part = {'loc': eval(parts[0].replace(':', ',')), 'text': parts[1].translate(buckwalter_transliteration), 'tag': parts[2]}

			features = parts[3].split('|')
			for feature in features:
				if feature.startswith('LEM:'):
					part['lem'] = feature[4:].translate(buckwalter_transliteration)
				elif feature.startswith('ROOT:'):
					part['root'] = feature[5:].translate(buckwalter_transliteration)
			yield part

	def words(self):

		def word_item(location, parts):
			text = ''.join([part['text'] for part in parts])
			tag = '-'.join([part['tag'] for part in parts])
			lem = '-'.join([part['lem'] for part in parts if 'lem' in part])
			root = '-'.join([part['root'] for part in parts if 'root' in part])
			return '.'.join(map(str, location)), text, lem, root, tag, parts

		last_location = (0, 0, 0, 0)
		items = []
		for part in self.parts():
			if last_location[:3] == part['loc'][:3]:
				items.append(part)
			else:
				if items:
					yield word_item(last_location[:3], items)
				items = [part]
			last_location = part['loc']
			del part['loc']
		yield word_item(last_location[:3], items)
