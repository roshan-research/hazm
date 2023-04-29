from .BijankhanReader import BijankhanReader
from .Chunker import Chunker
from .Chunker import RuleBasedChunker
from .Chunker import tree2brackets
from .DadeganReader import DadeganReader
from .DegarbayanReader import DegarbayanReader
from .DependencyParser import DependencyParser
from .DependencyParser import MaltParser
from .DependencyParser import TurboParser
from .HamshahriReader import HamshahriReader
from .InformalNormalizer import InformalLemmatizer
from .InformalNormalizer import InformalNormalizer
from .Lemmatizer import Lemmatizer
from .Lemmatizer import Conjugation
from .MirasTextReader import MirasTextReader
from .Normalizer import Normalizer
from .PersicaReader import PersicaReader
from .PeykareReader import PeykareReader
from .POSTagger import POSTagger
from .POSTagger import StanfordPOSTagger
from .QuranCorpusReader import QuranCorpusReader
from .SentenceTokenizer import SentenceTokenizer
from .SentiPersReader import SentiPersReader
from .SequenceTagger import IOBTagger
from .SequenceTagger import SequenceTagger
from .Stemmer import Stemmer
from .TNewsReader import TNewsReader
from .TokenSplitter import TokenSplitter
from .TreebankReader import TreebankReader
from .utils import stopwords_list
from .utils import words_list
from .VerbValencyReader import VerbValencyReader
from .WikipediaReader import WikipediaReader
from .WordTokenizer import WordTokenizer


def sent_tokenize(text):
    if not hasattr(sent_tokenize, "tokenizer"):
        sent_tokenize.tokenizer = SentenceTokenizer()
    return sent_tokenize.tokenizer.tokenize(text)


def word_tokenize(sentence):
    if not hasattr(word_tokenize, "tokenizer"):
        word_tokenize.tokenizer = WordTokenizer()
    return word_tokenize.tokenizer.tokenize(sentence)
