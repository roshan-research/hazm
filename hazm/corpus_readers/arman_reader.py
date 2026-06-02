"""This module includes classes and functions for reading the Arman corpus.

The [Arman corpus](https://github.com/HaniehP/PersianNER) is a Named Entity
Recognition (NER) corpus containing 250,015 tagged tokens in 7,682 sentences,
stored in IOB format.
"""

from collections.abc import Iterator
from pathlib import Path


class ArmanReader:
    """This class includes methods for reading the Arman corpus.

    Args:
        corpus_folder: Path to the folder containing the corpus files.
        subset: The dataset subset: 'test' or 'train'.
    """
    def __init__(self: "ArmanReader", corpus_folder: str, subset: str="train") -> None:
        """Initializes the ArmanReader with the corpus folder and subset.

        Args:
            corpus_folder: Path to the folder containing the corpus files.
            subset: The dataset subset: 'test' or 'train'. Defaults to 'train'.
        """
        self._corpus_folder = corpus_folder
        # Materialize the glob into a list so sents() can be called more than
        # once; a bare glob() returns a one-shot iterator that yields nothing on
        # the second pass.
        self._file_paths = sorted(Path(corpus_folder).glob(f"{subset}*.txt"))


    def sents(self: "ArmanReader") -> Iterator[list[tuple[str,str]]]:
        """Yields sentences one by one as a list of (token, tag) tuples.

        Examples:
            >>> arman = ArmanReader("arman")
            >>> next(arman.sents())
            [('همین', 'O'), ('فکر', 'O'), ('،', 'O'), ('این', 'O'), ('احساس', 'O'), ('را', 'O'), ('به', 'O'), ('من', 'O'), ('می‌داد', 'O'), ('که', 'O'), ('آزاد', 'O'), ('هستم', 'O'), ('.', 'O')]

        Yields:
            The next sentence as a list of (token, tag) tuples.
        """
        for file_path in self._file_paths:
            with Path(file_path).open("r", encoding="utf-8") as file:
                lines = file.readlines()
                sentence = []
                for line in lines:
                    line = line.strip()
                    if line:
                        token, label = line.split()
                        sentence.append((token, label))
                    elif sentence:
                        yield sentence
                        sentence = []
                if sentence:
                    yield sentence
