from .BijankhanReader import BijankhanReader
from .Chunker import Chunker, RuleBasedChunker, tree2brackets
from .DadeganReader import DadeganReader
from .DependencyParser import DependencyParser, MaltParser, TurboParser
from .HamshahriReader import HamshahriReader
from .InformalNormalizer import InformalNormalizer, InformalLemmatizer
from .Lemmatizer import Lemmatizer
from .Normalizer import Normalizer
from .POSTagger import POSTagger, StanfordPOSTagger
from .PersicaReader import PersicaReader
from .PeykareReader import PeykareReader
from .QuranCorpusReader import QuranCorpusReader
from .SentenceTokenizer import SentenceTokenizer
from .SentiPersReader import SentiPersReader
from .SequenceTagger import SequenceTagger, IOBTagger
from .Stemmer import Stemmer
from .TNewsReader import TNewsReader
from .TokenSplitter import TokenSplitter
from .TreebankReader import TreebankReader
from .VerbValencyReader import VerbValencyReader
from .WikipediaReader import WikipediaReader
from .WordTokenizer import WordTokenizer
from .utils import words_list, stopwords_list


def sent_tokenize(text):
    if not hasattr(sent_tokenize, 'tokenizer'):
        sent_tokenize.tokenizer = SentenceTokenizer()
    return sent_tokenize.tokenizer.tokenize(text)


def word_tokenize(sentence):
    if not hasattr(word_tokenize, 'tokenizer'):
        word_tokenize.tokenizer = WordTokenizer()
    return word_tokenize.tokenizer.tokenize(sentence)
