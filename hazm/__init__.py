"""entry point for the package."""

from typing import List

from .chunker import Chunker
from .chunker import RuleBasedChunker
from .chunker import tree2brackets
from .corpus_readers import BijankhanReader
from .corpus_readers import DadeganReader
from .corpus_readers import DegarbayanReader
from .corpus_readers import HamshahriReader
from .corpus_readers import MirasTextReader
from .corpus_readers import PersicaReader
from .corpus_readers import PeykareReader
from .corpus_readers import QuranReader
from .corpus_readers import SentiPersReader
from .corpus_readers import TNewsReader
from .corpus_readers import TreebankReader
from .corpus_readers import VerbValencyReader
from .corpus_readers import WikipediaReader
from .dependency_parser import DependencyParser
from .dependency_parser import MaltParser
from .dependency_parser import TurboParser
from .informal_normalizer import InformalLemmatizer
from .informal_normalizer import InformalNormalizer
from .lemmatizer import Conjugation
from .lemmatizer import Lemmatizer
from .normalizer import Normalizer
from .pos_tagger import POSTagger
from .pos_tagger import StanfordPOSTagger
from .sentence_tokenizer import SentenceTokenizer
from .sequence_tagger import IOBTagger
from .sequence_tagger import SequenceTagger
from .stemmer import Stemmer
from .token_splitter import TokenSplitter
from .utils import default_verbs
from .utils import default_words
from .utils import stopwords_list
from .utils import words_list
from .word_tokenizer import WordTokenizer


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
