# coding: utf8

from __future__ import unicode_literals
import os, codecs
from .Normalizer import *
from .WordTokenizer import *

tokenizer = WordTokenizer()


def universal_pos(tags):
	"""
	Map function for converting Peykare tags to Universial POS tags.
	Petrov, S., Das, D., & McDonald, R. (2012). A Universal Part-of-Speech Tagset. In Proceedings of LREC.

	>>> universal_pos(['N','COM','SING'])
	'NOUN'
	"""

	peykare_universal = {'N': 'NOUN', 'V': 'VERB', 'AJ': 'ADJ', 'ADV': 'ADV', 'PRO': 'PRON', 'DET': 'DET', 'P': 'ADP', 'POSTP': 'ADP', 'NUM': 'NUM', 'CONJ': 'CONJ', 'PUNC': '.', 'CL': 'X', 'INT': 'X', 'RES': 'X'}
	return [peykare_universal[tag] for tag in tags if tag in peykare_universal][0]


def universal_pos_e(tags):
	"""
	Universal POS tags plus Ezafe.
	Asghari, H., Maleki, J., & Faili, H. (2014). A Probabilistic Approach to Persian Ezafe Recognition. In EACL 2014.

	>>> universal_pos_e(['AJ','SIM','EZ'])
	'ADJe'
	"""

	return universal_pos(tags) + ('e' if 'EZ' in tags else '')


def join_verb_parts(sentence):
	"""
	Join verb parts like Dadedgan corpus.

	>>> join_verb_parts([('اولین', 'ADJ'), ('سیاره', 'NOUNe'), ('خارج', 'ADJ'), ('از', 'ADP'), ('منظومه', 'NOUNe'), ('شمسی', 'ADJ'), ('دیده', 'ADJ'), ('شد', 'VERB'), ('.', '.')])
	[('اولین', 'ADJ'), ('سیاره', 'NOUNe'), ('خارج', 'ADJ'), ('از', 'ADP'), ('منظومه', 'NOUNe'), ('شمسی', 'ADJ'), ('دیده شد', 'VERB'), ('.', '.')]
	"""

	result = [('', '')]
	for word in reversed(sentence):
		if word[0] in tokenizer.before_verbs or (result[-1][0] in tokenizer.after_verbs and word[0] in tokenizer.verbe):
			result[-1] = (word[0] +' '+ result[-1][0], result[-1][1])
		else:
			result.append(word)
	return list(reversed(result[1:]))


class PeykareReader():
	"""
	interfaces [Peykare Corpus](http://dadegan.ir/catalog/D3920121a)
	Bijankhan, M., Sheykhzadegan, J., Bahrani, M., & Ghayoomi, M. (2011). Lessons from building a Persian written corpus: Peykare. Language Resources and Evaluation, 45, 143–164.

	Peykare POS tags:
		N: Noun, V: Verb, AJ: Adjective, ADV: Adverb, PRO: Pronoun, DET: Determiner, P: Preposition, POSTP: Postposition, NUM: Number, CONJ: Conjunction, PUNC: Punctuation, RES: Residual, CL: Classifier, INT: Interjection
	"""

	def __init__(self, root='corpora/peykare', joined_verb_parts=True, pos_map=universal_pos_e):
		self._root = root
		self._pos_map = pos_map
		self._joined_verb_parts = joined_verb_parts
		self._normalizer = Normalizer(punctuation_spacing=False)

	def docs(self):
		for root, dirs, files in os.walk(self._root):
			for name in files:
				text = codecs.open(os.path.join(root, name), encoding='windows-1256').read()
				if text:
					yield text

	def _sentences(self):
		for doc in self.docs():

			sentence = []
			for line in doc.split('\r\n'):
				if not line:
					continue

				parts = line.split(' ')
				tags, word = parts[3], '‌'.join(parts[4:])

				if word != '#':
					sentence.append((word, tags))

				if parts[2] == 'PUNC' and word in {'#', '.', '؟', '!'}:
					if len(sentence) > 1:
						yield sentence
					sentence = []

	def sents(self):
		"""
		>>> next(peykare.sents())
		[('دیرزمانی', 'NOUN'), ('از', 'ADP'), ('راه‌اندازی', 'NOUNe'), ('شبکه‌ی', 'NOUNe'), ('خبر', 'NOUNe'), ('الجزیره', 'NOUN'), ('نمی‌گذرد', 'VERB'), ('،', '.'), ('اما', 'CONJ'), ('این', 'DET'), ('شبکه‌ی', 'NOUNe'), ('خبری', 'ADJe'), ('عربی', 'NOUN'), ('بسیار', 'ADV'), ('سریع', 'ADV'), ('توانسته', 'VERB'), ('در', 'ADP'), ('میان', 'NOUNe'), ('شبکه‌های', 'NOUNe'), ('عظیم', 'ADJe'), ('خبری', 'ADJ'), ('و', 'CONJ'), ('بنگاه‌های', 'NOUNe'), ('چندرسانه‌ای', 'ADJe'), ('دنیا', 'NOUN'), ('خودی', 'NOUN'), ('نشان', 'NOUN'), ('دهد', 'VERB'), ('.', '.')]
		"""

		refine = lambda item: (self._normalizer.normalize(item[0]), self._pos_map(item[1].split(',')))

		for sentence in self._sentences():
			if self._joined_verb_parts:
				sentence = join_verb_parts(sentence)

			yield list(map(refine, sentence))
