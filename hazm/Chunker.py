# coding: utf8

from __future__ import unicode_literals
from nltk.chunk import ChunkParserI, RegexpParser, tree2conlltags, conlltags2tree
from .SequenceTagger import IOBTagger


def tree2brackets(tree):
	str, tag = '', ''
	for item in tree2conlltags(tree):
		if item[2][0] in {'B', 'O'} and tag:
			str += tag +'] '
			tag = ''

		if item[2][0] == 'B':
			tag = item[2].split('-')[1]
			str += '['
		str += item[0] +' '

	if tag:
		str += tag +'] '

	return str.strip()


class Chunker(IOBTagger, ChunkParserI):
	"""
	>>> # from hazm import POSTagger
	>>> # chunker = Chunker(tagger=POSTagger(), model='resources/chunker.model')
	>>> # tree2brackets(chunker.parse([('نامه', 'Ne'), ('۱۰', 'NUM'), ('فوریه', 'Ne'), ('شما', 'PRO'), ('را', 'POSTP'), ('دریافت', 'N'), ('داشتم', 'V'), ('.', 'PUNC')]))
	'[نامه ۱۰ فوریه شما NP] [را POSTP] [دریافت داشتم VP] .'
	"""

	def __init__(self, tagger, **kwargs):
		self.tagger = tagger

	def train(self, trees):
		super(Chunker, self).train(map(tree2conlltags, trees))

	def parse(self, sentence):
		return self.parse_sents([sentence])[0]

	def parse_sents(self, sentences):
		tagged_sentences = self.tagger.tag_sents(sentences)
		return self.tagged_parse_sents(tagged_sentences)

	def tagged_parse_sents(self, sentences):
		return conlltags2tree(super(Chunker, self).tag_sents(sentences))


class RuleBasedChunker(RegexpParser):
	"""
	>>> chunker = RuleBasedChunker()
	>>> tree2brackets(chunker.parse([('نامه', 'Ne'), ('۱۰', 'NUM'), ('فوریه', 'Ne'), ('شما', 'PRO'), ('را', 'POSTP'), ('دریافت', 'N'), ('داشتم', 'V'), ('.', 'PUNC')]))
	'[نامه ۱۰ فوریه شما NP] [را POSTP] [دریافت داشتم VP] .'
	"""

	def __init__(self):
		grammar = r"""

			NP:
				<P>{<N>}<V>

			VP:
				<.*[^e]>{<N>?<V>}
				{<V>}

			ADVP:
				{<ADVe?><AJ>?}

			ADJP:
				<.*[^e]>{<AJe?>}

			NP:
				{<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?|AJe?|PRO|CL|RESe?>*}
				<N>}{<.*e?>

			ADJP:
				{<AJe?>}

			POSTP:
				{<POSTP>}

			PP:
				{<Pe?>+}

		"""

		super(Chunker, self).__init__(grammar=grammar)
