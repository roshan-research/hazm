
from .WordTokenizer import WordTokenizer
from .SentenceTokenizer import SentenceTokenizer
from .PeykareReader import PeykareReader
from .BijankhanReader import BijankhanReader
from .HamshahriReader import HamshahriReader
from .VerbValencyReader import VerbValencyReader
from .DadeganReader import DadeganReader
from .TreebankReader import TreebankReader
from .Normalizer import Normalizer
from .Stemmer import Stemmer
from .Lemmatizer import Lemmatizer
from .SequenceTagger import SequenceTagger, IOBTagger
from .POSTagger import POSTagger, StanfordPOSTagger
from .Chunker import Chunker, RuleBasedChunker
from .DependencyParser import DependencyParser


def sent_tokenize(text):
	if not hasattr(sent_tokenize, 'tokenizer'):
		sent_tokenize.tokenizer = SentenceTokenizer()
	return sent_tokenize.tokenizer.tokenize(text)


def word_tokenize(sentence):
	if not hasattr(word_tokenize, 'tokenizer'):
		word_tokenize.tokenizer = WordTokenizer()
	return word_tokenize.tokenizer.tokenize(sentence)
