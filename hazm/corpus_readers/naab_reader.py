"""This module includes classes and functions for reading the Naab corpus.

The [Naab corpus](https://huggingface.co/datasets/SLPL/naab/) consists of 130 GB
of cleaned Persian text comprising 250 million paragraphs and 15 billion words.
"""
from collections.abc import Iterator
from pathlib import Path


class NaabReader:
    """This class includes functions for reading the Naab corpus.

    Args:
        corpus_folder: Path to the folder containing the corpus files.
        subset: The dataset subset: `test` or `train`.
    """

    def __init__(self: "NaabReader", corpus_folder: str, subset: str="train") -> None:
        """Initializes the Naab reader.

        Args:
            corpus_folder: Path to the folder containing the corpus files.
            subset: The dataset subset: `test` or `train`.
        """
        # Materialize the glob into a list so sents() can be iterated more than
        # once (a bare glob() is a one-shot iterator).
        self._file_paths = sorted(Path(corpus_folder).glob(f"{subset}*.txt"))

    def sents(self: "NaabReader") -> Iterator[str]:
        """Yields sentences from the corpus one by one.

        Examples:
            >>> naab = NaabReader("naab", "test")
            >>> next(naab.sents())
            این وبلاگ زیر نظر وب‌های زیر به کار خود ادامه می‌دهد

        Yields:
            The next sentence in the corpus.
        """
        for file_path in self._file_paths:
                with Path(file_path).open("r", encoding="utf-8") as file:
                    yield from (line.strip() for line in file)
