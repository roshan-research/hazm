from typing import Any
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus.reader import StreamBackedCorpusView
from nltk.corpus.reader import read_blankline_block

from hazm import sent_tokenize
from hazm import word_tokenize


class PersianPlainTextReader(PlaintextCorpusReader):
    """
    Reader for corpora that consist of plaintext documents.  Paragraphs
    are assumed to be split using blank lines.  Sentences and words can
    be tokenized using the default tokenizers, or by custom tokenizers
    specificed as parameters to the constructor.

    """

    CorpusView = StreamBackedCorpusView

    def __init__(
        self,
        root: Any,
        fileids: Any,
        word_tokenizer:Any= word_tokenize,
        sent_tokenizer: Any= sent_tokenize,
        para_block_reader: Any= read_blankline_block,
        encoding="utf8",
    ) -> None:
        super().__init__(
            root, fileids, word_tokenizer, sent_tokenizer, para_block_reader, encoding
        )
