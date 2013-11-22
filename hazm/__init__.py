
from .Normalizer import Normalizer
from .SentenceTokenizer import SentenceTokenizer
from .WordTokenizer import WordTokenizer

sentence_tokenizer = SentenceTokenizer()
sent_tokenize = lambda text: sentence_tokenizer.tokenize(text)
word_tokenizer = WordTokenizer()
word_tokenize = lambda text: word_tokenizer.tokenize(text)
