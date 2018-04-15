
from .WordTokenizer import WordTokenizer
from .SentenceTokenizer import SentenceTokenizer
from .TokenSplitter import TokenSplitter
from .HamshahriReader import HamshahriReader
from .PersicaReader import PersicaReader
from .BijankhanReader import BijankhanReader
from .PeykareReader import PeykareReader
from .VerbValencyReader import VerbValencyReader
from .DadeganReader import DadeganReader
from .TreebankReader import TreebankReader
from .WikipediaReader import WikipediaReader
from .SentiPersReader import SentiPersReader
from .QuranCorpusReader import QuranCorpusReader
from .TNewsReader import TNewsReader
from .Normalizer import Normalizer
from .InformalNormalizer import InformalNormalizer, InformalLemmatizer
from .Stemmer import Stemmer
from .Lemmatizer import Lemmatizer
from .SequenceTagger import SequenceTagger, IOBTagger
from .POSTagger import POSTagger, StanfordPOSTagger
from .Chunker import Chunker, RuleBasedChunker, tree2brackets
from .DependencyParser import DependencyParser, MaltParser, TurboParser


from .utils import words_list, stopwords_list


def sent_tokenize(text):
	if not hasattr(sent_tokenize, 'tokenizer'):
		sent_tokenize.tokenizer = SentenceTokenizer()
	return sent_tokenize.tokenizer.tokenize(text)


def word_tokenize(sentence):
	if not hasattr(word_tokenize, 'tokenizer'):
		word_tokenize.tokenizer = WordTokenizer()
	return word_tokenize.tokenizer.tokenize(sentence)
