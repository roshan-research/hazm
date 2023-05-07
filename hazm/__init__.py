from .Chunker import Chunker, RuleBasedChunker, tree2brackets
from .CorpusReaders import (BijankhanReader, DadeganReader, DegarbayanReader,
                            HamshahriReader, MirasTextReader, PersicaReader,
                            PeykareReader, QuranCorpusReader, SentiPersReader,
                            TNewsReader, TreebankReader, VerbValencyReader,
                            WikipediaReader)
from .DependencyParser import DependencyParser, MaltParser, TurboParser
from .InformalNormalizer import InformalLemmatizer, InformalNormalizer
from .Lemmatizer import Conjugation, Lemmatizer
from .Normalizer import Normalizer
from .POSTagger import POSTagger, StanfordPOSTagger
from .SentenceTokenizer import SentenceTokenizer
from .SequenceTagger import IOBTagger, SequenceTagger
from .Stemmer import Stemmer
from .TokenSplitter import TokenSplitter
from .utils import stopwords_list, words_list
from .WordTokenizer import WordTokenizer


def sent_tokenize(text: str):
    if not hasattr(sent_tokenize, "tokenizer"):
        sent_tokenize.tokenizer = SentenceTokenizer()
    return sent_tokenize.tokenizer.tokenize(text)


def word_tokenize(sentence):
    if not hasattr(word_tokenize, "tokenizer"):
        word_tokenize.tokenizer = WordTokenizer()
    return word_tokenize.tokenizer.tokenize(sentence)
