# ruff: noqa
"""entry point for the package."""

from typing import List

from hazm.utils import default_verbs
from hazm.utils import default_words
from hazm.utils import stopwords_list
from hazm.utils import words_list
from hazm.utils import maketrans
from hazm.utils import regex_replace
from hazm.utils import words_list
from hazm.utils import NUMBERS
from hazm.utils import informal_verbs
from hazm.utils import informal_words

from hazm.sequence_tagger import IOBTagger
from hazm.sequence_tagger import SequenceTagger

from hazm.pos_tagger import POSTagger
from hazm.pos_tagger import StanfordPOSTagger

from hazm.stemmer import Stemmer
from hazm.word_tokenizer import WordTokenizer

from hazm.lemmatizer import Conjugation
from hazm.lemmatizer import Lemmatizer

from hazm.normalizer import Normalizer

from hazm.chunker import Chunker
from hazm.chunker import RuleBasedChunker
from hazm.chunker import tree2brackets

from hazm.sentence_tokenizer import SentenceTokenizer

def sent_tokenize(text: str) -> List[str]:
    """Sentence Tokenizer."""
    if not hasattr(sent_tokenize, "tokenizer"):
        sent_tokenize.tokenizer = SentenceTokenizer()
    return sent_tokenize.tokenizer.tokenize(text)


def word_tokenize(sentence: str) -> List[str]:
    """Word Tokenizer."""
    if not hasattr(word_tokenize, "tokenizer"):
        word_tokenize.tokenizer = WordTokenizer()
    return word_tokenize.tokenizer.tokenize(sentence)

from hazm.corpus_readers import PeykareReader
from hazm.corpus_readers import BijankhanReader
from hazm.corpus_readers import DadeganReader
from hazm.corpus_readers import UniversalDadeganReader
from hazm.corpus_readers import DegarbayanReader
from hazm.corpus_readers import HamshahriReader
from hazm.corpus_readers import MirasTextReader
from hazm.corpus_readers import PersicaReader
from hazm.corpus_readers import QuranReader
from hazm.corpus_readers import SentiPersReader
from hazm.corpus_readers import TNewsReader
from hazm.corpus_readers import TreebankReader
from hazm.corpus_readers import VerbValencyReader
from hazm.corpus_readers import PersianPlainTextReader
from hazm.corpus_readers import WikipediaReader

from hazm.dependency_parser import DependencyParser
from hazm.dependency_parser import MaltParser
from hazm.dependency_parser import TurboParser

from hazm.embedding import SentEmbedding
from hazm.embedding import WordEmbedding

from hazm.informal_normalizer import InformalLemmatizer
from hazm.informal_normalizer import InformalNormalizer

from hazm.token_splitter import TokenSplitter


