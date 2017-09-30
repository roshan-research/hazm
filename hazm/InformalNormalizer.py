# coding: utf-8

from __future__ import unicode_literals
import codecs
from .utils import informal_verbs, informal_words, NUMBERS
from .Normalizer import Normalizer
from .Lemmatizer import Lemmatizer
from .Stemmer import Stemmer
from .WordTokenizer import *
from .SentenceTokenizer import *


class InformalNormalizer(Normalizer):

	def __init__(self, verb_file=informal_verbs, word_file=informal_words, seperation_flag=False, **kargs):
		self.seperation_flag = seperation_flag
		self.lemmatizer = Lemmatizer()
		self.ilemmatizer = InformalLemmatizer()
		self.stemmer = Stemmer()
		super(InformalNormalizer, self).__init__(**kargs)

		def informal_to_formal_conjucation(i, f, flag):
			iv = self.informal_conjugations(i)
			fv = self.lemmatizer.conjugations(f)
			res = {}
			if flag:
				for i, j in zip(iv, fv[48:]):
					res[i] = j
					if '‌' in i:
						res[i.replace('‌', '')] = j
						res[i.replace('‌', ' ')] = j
					if i.endswith('ین'):
						res[i[:-1] + 'د'] = j
			else:
				for i, j in zip(iv[8:], fv[56:]):
					res[i] = j
					if '‌' in i:
						res[i.replace('‌', '')] = j
						res[i.replace('‌', ' ')] = j
					if i.endswith('ین'):
						res[i[:-1] + 'د'] = j

			return res

		with codecs.open(verb_file, encoding='utf8') as vf:
			self.iverb_map = {}
			for f, i, flag in map(lambda x: x.strip().split(' ', 2), vf):
				self.iverb_map.update(
					informal_to_formal_conjucation(i, f, flag)
				)

		with codecs.open(word_file, encoding='utf8') as wf:
			self.iword_map = dict(
				map(lambda x: x.strip().split(' ', 1), wf)
			)

		self.words = set()
		if self.seperation_flag:
			self.words.update(self.iword_map.keys())
			self.words.update(self.iword_map.values())
			self.words.update(self.iverb_map.keys())
			self.words.update(self.iverb_map.values())
			self.words.update(self.lemmatizer.words)
			self.words.update(self.lemmatizer.verbs.keys())
			self.words.update(self.lemmatizer.verbs.values())

	def split_token_words(self, token):

		def shekan(token):
			res = ['']
			for i in token:
				res[-1] += i
				if i in set(['ا', 'د', 'ذ', 'ر', 'ز', 'ژ', 'و'] + list(NUMBERS)):
					res.append('')
			while '' in res:
				res.remove('')
			return res

		def perm(lst):
			if len(lst) > 1:
				up = perm(lst[1:])
			else:
				return [lst]
			res = []
			for i in up:
				res.append([lst[0]] + i)
				res.append([lst[0] + i[0]] + i[1:])
			res.sort(key=len)
			return res

		token = re.sub(r'(.)\1{2,}', r'\1', token)
		ps = perm(shekan(token))
		for c in ps:
			if set(map(lambda x: self.ilemmatizer.lemmatize(x), c)).issubset(self.words):
				return ' '.join(c)
		return token


	def normalized_word(self, word):
		"""
		>>> normalizer = InformalNormalizer()
		>>> normalizer.normalized_word('می‌رم')
		['می‌روم', 'می‌رم']
		>>> normalizer = InformalNormalizer(seperation_flag=True)
		>>> normalizer.normalized_word('صداوسیماجمهوری')
		['صداوسیما جمهوری', 'صداوسیماجمهوری']
		"""

		options = []
		if word in self.lemmatizer.words or word in self.lemmatizer.verbs:
			pass

		elif word in self.iverb_map:
			options.append(self.iverb_map[word])

		elif word in self.iword_map:
			options.append(self.iword_map[word])

		elif word[:-2] in self.ilemmatizer.verbs and word.endswith('ین'):
			options.append(word[:-1] + 'د')

		elif word.endswith("ن") and word[:-1] in self.ilemmatizer.verbs:
			options.append(word + 'د')

		elif word[:-1] in self.ilemmatizer.verbs and word.endswith('ه') and word[:-1] not in self.lemmatizer.words:
			options.append(self.iword_map.get(word[:-1], word[:-1]) + 'د')

		elif word not in self.ilemmatizer.verbs and word.endswith('ه') and word[:-1] in self.ilemmatizer.words:
			options.append(self.iword_map.get(word[:-1], word[:-1]) + ' است')

		elif word not in self.ilemmatizer.verbs and word.endswith('ون') and self.lemmatizer.lemmatize(word[:-2] + 'ان') in self.ilemmatizer.words:
			options.append(word[:-2] + 'ان')

		elif self.seperation_flag:
			options.append(self.split_token_words(word))

		options.append(word)
		return options

	def normalize(self, text):

		sent_tokenizer = SentenceTokenizer()
		word_tokenizer = WordTokenizer()
		text = super(InformalNormalizer, self).normalize(text)
		sents = [word_tokenizer.tokenize(sentence) for sentence in sent_tokenizer.tokenize(text)]

		return [[self.normalized_word(word) for word in sent] for sent in sents]

	def informal_conjugations(self, verb):
		ends = ['م', 'ی', '', 'یم', 'ین', 'ن']
		present_simples = [verb + end for end in ends]
		if verb.endswith('ا'):
			present_simples[2] = verb + 'د'
		else:
			present_simples[2] = verb + 'ه'
		present_not_simples = ['ن' + item for item in present_simples]
		present_imperfects = ['می‌' + item for item in present_simples]
		present_not_imperfects = ['ن' + item for item in present_imperfects]
		present_subjunctives = [
			item if item.startswith('ب') else 'ب' + item for item in present_simples]
		present_not_subjunctives = ['ن' + item for item in present_simples]
		return present_simples + present_not_simples + \
			present_imperfects + present_not_imperfects + \
			present_subjunctives + present_not_subjunctives


class InformalLemmatizer(Lemmatizer):

	def __init__(self, **kargs):
		super(InformalLemmatizer, self).__init__(**kargs)

		temp = []
		self.words = set(self.words.keys())
		for word in self.words:
			if word.endswith("ً"):
				temp.append(word[:-1])

		self.words.update(temp)

		temp = {}
		for verb in self.verbs:
			if verb.endswith("د"):
				temp[verb[:-1] + 'ن'] = self.verbs[verb]

		self.verbs.update(temp)

		with codecs.open(informal_verbs, encoding='utf8') as vf:
			for f, i, flag in map(lambda x: x.strip().split(' ', 2), vf):
				self.verbs.update(dict(
					map(lambda x: (x, f), self.iconjugations(i))
				))

		with codecs.open(informal_words, encoding='utf8') as wf:
			self.words.update(
				map(lambda x: x.strip().split(' ', 1)[0], wf)
			)

	def iconjugations(self, verb):
		ends = ['م', 'ی', '', 'یم', 'ین', 'ن']
		present_simples = [verb + end for end in ends]
		if verb.endswith('ا'):
			present_simples[2] = verb + 'د'
		else:
			present_simples[2] = verb + 'ه'
		present_not_simples = ['ن' + item for item in present_simples]
		present_imperfects = ['می‌' + item for item in present_simples]
		present_not_imperfects = ['ن' + item for item in present_imperfects]
		present_subjunctives = [
			item if item.startswith('ب') else 'ب' + item for item in present_simples]
		present_not_subjunctives = ['ن' + item for item in present_simples]
		return present_simples + present_not_simples + \
			present_imperfects + present_not_imperfects + \
			present_subjunctives + present_not_subjunctives
