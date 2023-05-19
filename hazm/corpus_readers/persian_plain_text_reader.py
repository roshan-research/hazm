"""این ماژول، پیکره‌های متنی خام را می‌خواند."""
from typing import Any, Callable, List

from nltk.corpus import PlaintextCorpusReader
from nltk.corpus.reader import StreamBackedCorpusView, read_blankline_block

from hazm import sent_tokenize, word_tokenize


class PersianPlainTextReader(PlaintextCorpusReader):
    """Reader for corpora that consist of plaintext documents.  Paragraphs
    are assumed to be split using blank lines.  Sentences and words can
    be tokenized using the default tokenizers, or by custom tokenizers
    specificed as parameters to the constructor.

    """

    CorpusView = StreamBackedCorpusView

    def __init__(
        self: "PersianPlainTextReader",
        root: str,
        fileids: List,
        word_tokenizer: Callable = word_tokenize,
        sent_tokenizer: Callable = sent_tokenize,
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
