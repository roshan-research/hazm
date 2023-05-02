from .CorpusReaders import BijankhanReader
from .Chunker import Chunker
from .Chunker import RuleBasedChunker
from .Chunker import tree2brackets
from .CorpusReaders import DadeganReader
from .CorpusReaders import DegarbayanReader
from .DependencyParser import DependencyParser
from .DependencyParser import MaltParser
from .DependencyParser import TurboParser
from .CorpusReaders import HamshahriReader
from .InformalNormalizer import InformalLemmatizer
from .InformalNormalizer import InformalNormalizer
from .Lemmatizer import Conjugation
from .Lemmatizer import Lemmatizer
from .CorpusReaders import MirasTextReader
from .Normalizer import Normalizer
from .CorpusReaders import PersicaReader
from .CorpusReaders import PeykareReader
from .POSTagger import POSTagger
from .POSTagger import StanfordPOSTagger
from .CorpusReaders import QuranCorpusReader
from .SentenceTokenizer import SentenceTokenizer
from .CorpusReaders import SentiPersReader
from .SequenceTagger import IOBTagger
from .SequenceTagger import SequenceTagger
from .Stemmer import Stemmer
from .CorpusReaders import TNewsReader
from .TokenSplitter import TokenSplitter
from .CorpusReaders import TreebankReader
from .utils import stopwords_list
from .utils import words_list
from .CorpusReaders import VerbValencyReader
from .CorpusReaders import WikipediaReader
from .WordTokenizer import WordTokenizer


def sent_tokenize(text: str):
    if not hasattr(sent_tokenize, "tokenizer"):
        sent_tokenize.tokenizer = SentenceTokenizer()
    return sent_tokenize.tokenizer.tokenize(text)


def word_tokenize(sentence):
    if not hasattr(word_tokenize, "tokenizer"):
        word_tokenize.tokenizer = WordTokenizer()
    return word_tokenize.tokenizer.tokenize(sentence)
