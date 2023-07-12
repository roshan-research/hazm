"""این ماژول، پیکره‌های متنی خام را می‌خواند."""
from typing import Any
from typing import Callable
from typing import List

from nltk.corpus import PlaintextCorpusReader
from nltk.corpus.reader import StreamBackedCorpusView
from nltk.corpus.reader import read_blankline_block

from hazm import SentenceTokenizer
from hazm import WordTokenizer


class PersianPlainTextReader(PlaintextCorpusReader):

    CorpusView = StreamBackedCorpusView

    def __init__(
        self: "PersianPlainTextReader",
        root: str,
        fileids: List,
        word_tokenizer: Callable = WordTokenizer.tokenize,
        sent_tokenizer: Callable = SentenceTokenizer.tokenize,
        para_block_reader: Callable = read_blankline_block,
        encoding: str = "utf8",
    ) -> None:
        super().__init__(
            root,
            fileids,
            word_tokenizer,
            sent_tokenizer,
            para_block_reader,
            encoding,
        )
