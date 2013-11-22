
import re
from .utils import u
from nltk.tokenize.api import TokenizerI


class WordTokenizer(TokenizerI):
	def __init__(self):
		self.pattern = re.compile(u(r'([!:\.،؛؟»\]\)\}«\[\(\{\?]+)'))

	def tokenize(self, text):
		"""
		>>> tokenizer.tokenize('این جمله معمولی است.')
		['این', 'جمله', 'معمولی', 'است', '.']
		"""

		text = self.pattern.sub(r' \1', text)
		return [word for word in text.split(' ') if word]


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'tokenizer': WordTokenizer()})
