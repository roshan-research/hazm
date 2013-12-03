#coding=utf8

import re, codecs
from .Normalizer import *
from .WordTokenizer import *

dadegan_map = {
	'CON'	:	'CONJ',
	'DELM'	: 	'PUNC',
	'P'		:	'PREP',
	'PRO'	:	'PR',
	'DET'	:	'PREP',
}

class BijankhanReader():

	def __init__(self, bijankhan_corpus='resources/bijankhan.txt', joined_verb_parts=True, pos_map=dadegan_map):
		"""
			downnload bijankhan corpus from ...
		"""
		self._separator = '/'
		self._bijankhan_corpus = bijankhan_corpus
		self.joined_verb_parts = joined_verb_parts
		self._pos_map = dadegan_map
		self._normalizer = Normalizer(punctuation_spacing=False)
		self._tokenizer = WordTokenizer()
		self._pattern_pos_removal = re.compile(r'/[a-zA-z]+')

	def sents(self, add_pos=False, use_cpos=False):
		def word_pos(token, use_cpos=False):
			# 11/26/2013/POS => [11/26/2013, POS]
			word = self._pattern_pos_removal.sub(r'', token)
			parts = token.split(self._separator) 
			pos = parts[len(parts)-1]
			if (use_cpos == True):
				pos = mapper(pos.split('_')[0])
			else:
				pos = mapper(pos)
			return (word,pos)

		def normalized(sent):
			sentence = ' '.join(sent)

			if (add_pos==False):
				return self._normalizer.normalize(sentence)
			else:
				new_sent = []

				pos_text = self._normalizer.normalize(sentence)
				pos_tokens = pos_text.split(' ')

				raw_text = self._pattern_pos_removal.sub(r'', sentence)
				raw_text = self._normalizer.normalize(raw_text)
				raw_tokens = self._tokenizer.tokenize(raw_text)

				j = 0
				for i, t in enumerate(raw_tokens):
					w,p = word_pos(pos_tokens[j], use_cpos)
					if (w != t and t.startswith(w)):
						for k in range(j+1, len(pos_tokens)):
							w1,p1 = word_pos(pos_tokens[k], use_cpos)
							if (t.endswith(w1)):
								p = mapper('V')
								j = k+1
								break
					else:
						j=j+1
					new_sent.append(t.replace(' ', '_') + self._separator + p)
				return ' '.join(new_sent)

		def mapper(pos):
			if (self._pos_map != None and pos in self._pos_map):
				pos = self._pos_map[pos]
			return pos

		texts = codecs.open(self._bijankhan_corpus, encoding='utf-8').read()
		lines = [word.strip() for word in texts.split('\n')]
		sentence = []
		for line in lines:
			parts = re.split("[ \t]+", line)
			word = '‌'.join(parts[0:len(parts)-1])
			pos = parts[len(parts)-1]
			if (word == '#'):
				yield normalized(sentence)
				sentence = []
			else:
				if (add_pos == True):
					new_pos = mapper(pos)
					if ('؛' in word):
						word = word.replace('؛', '')
						sentence.append(word + self._separator + new_pos)
						sentence.append('؛' + self._separator + mapper('DELM'))
					else:
						sentence.append(word + self._separator + new_pos)
				else:
					if ('؛' in word):
						word = word.replace('؛', '')
						sentence.append(word)
						sentence.append('؛')
					else:
						sentence.append(word)
					
				if (word == '.' and pos == 'DELM'):
					yield normalized(sentence)
					sentence = []