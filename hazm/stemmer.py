"""This module includes classes and functions for word stemming.

The difference between [Lemmatizer](./lemmatizer.md) and [Stemmer](./stemmer.md) is that
the Stemmer has no understanding of the word's meaning and merely tries to find
the root by removing some simple suffixes; therefore, it may provide incorrect
results for some words. However, the Lemmatizer performs this task based on a
reference list of words along with their roots, offering more accurate results.
Of course, the cost of this accuracy is lower speed in stemming.
"""

from nltk.stem.api import StemmerI

from hazm.constants import SUFFIXES


class Stemmer(StemmerI):
    """This class includes methods for finding the stem of words."""

    def __init__(self) -> None:
        """Initializes the Stemmer with a sorted list of suffixes."""
        self.ends = sorted(SUFFIXES | {"ٔ", "‌ا", "‌"}, key=len, reverse=True)

    def stem(self, word: str) -> str:
        """Finds the stem of the word.

        Example:
            >>> stemmer = Stemmer()
            >>> stemmer.stem('کتابی')
            'کتاب'
            >>> stemmer.stem('کتاب‌ها')
            'کتاب'
            >>> stemmer.stem('کتاب‌هایی')
            'کتاب'
            >>> stemmer.stem('کتابهایشان')
            'کتاب'
            >>> stemmer.stem('اندیشه‌اش')
            'اندیشه'
            >>> stemmer.stem('خانۀ')
            'خانه'


        Args:
            word: The input word to be stemmed.

        Returns:
            The stemmed version of the word.
        """
        for end in self.ends:
            if word.endswith(end):
                if len(end) == 1 and len(word) - len(end) < 3:
                    continue

                # Avoid stripping a multi-character suffix when doing so would
                # leave an empty or single-character stem (e.g. 'ها' -> '').
                if len(word) - len(end) < 2:
                    continue

                word = word[:-len(end)]
                break

        if word.endswith("ۀ"):
            word = word[:-1] + "ه"

        if word.endswith("\u200c"):
            word = word[:-1]

        return word
