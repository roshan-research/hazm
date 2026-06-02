"""This module includes classes and functions for reading the Named Entity Recognition (NER) corpus.

The [Named Entity Recognition corpus](https://github.com/Text-Mining/Persian-NER/)
contains 25 million tagged tokens from Persian Wikipedia in the form of about
one million sentences.
"""

from collections.abc import Iterator
from pathlib import Path


class NerReader:
    """This class includes functions for reading the Named Entity Recognition (NER) corpus.

    Args:
        corpus_folder: Path to the folder containing the corpus files.
    """
    def __init__(self: "NerReader", corpus_folder: str) -> None:
        """Initializes the NER reader.

        Args:
            corpus_folder: Path to the folder containing the corpus files.
        """
        self._corpus_folder = corpus_folder
        # Materialize the glob into a list so sents() can be iterated more than
        # once (a bare glob() is a one-shot iterator).
        self._file_paths = sorted(Path(corpus_folder).glob("*.txt"))


    def sents(self: "NerReader") -> Iterator[list[tuple[str,str]]]:
        """Yields sentences one by one as a list of `(token, tag)` tuples.

        Examples:
            >>> ner = NerReader("ner")
            >>> next(ner.sents())
            [('ویکی‌پدیای', 'O'), ('انگلیسی', 'O'), ('در', 'B-DAT'), ('تاریخ', 'I-DAT'), ('۱۵', 'I-DAT'), ('ژانویه', 'I-DAT'), ('۲۰۰۱', 'I-DAT'), ('(', 'O'), ('میلادی', 'B-DAT'), (')', 'O'), ('۲۶', 'B-DAT'), ('دی', 'I-DAT'), ('۱۳۷۹', 'I-DAT'), (')', 'O'), ('به', 'O'), ('صورت', 'O'), ('مکملی', 'O'), ('برای', 'O'), ('دانشنامه', 'O'), ('تخصصی', 'O'), ('نوپدیا', 'O'), ('نوشته', 'O'), ('شد', 'O'), ('.', 'O')]

        Yields:
            The next sentence in the form of a list of `(token, tag)` tuples.
        """
        for file_path in self._file_paths:
            with Path(file_path).open("r", encoding="utf-8") as file:
                lines = file.readlines()
                sentence = []
                for line in lines:
                    line = line.strip()
                    if line:
                        token, label = line.split("\t")
                        sentence.append((token, label))
                    elif sentence:
                        yield sentence
                        sentence = []
                if sentence:
                    yield sentence
