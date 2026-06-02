import importlib.resources
import re
import sys
from pathlib import Path
from typing import Any


def get_data_path(filename: str) -> Path:
    """Returns the data file path in a zip-safe manner.

    Args:
        filename: The name of the data file.

    Returns:
        The path to the specified data file.
    """
    return importlib.resources.files("hazm") / "data" / filename

default_words = get_data_path("words.dat")
default_stopwords = get_data_path("stopwords.dat")
default_verbs = get_data_path("verbs.dat")
informal_words = get_data_path("iwords.dat")
informal_verbs = get_data_path("iverbs.dat")
abbreviations = get_data_path("abbreviations.dat")

NUMBERS = "۰۱۲۳۴۵۶۷۸۹"

def maketrans(a: str, b: str) -> dict[int, Any]:
    """Maps each character in string `a` to the corresponding character in string `b`.

    Examples:
        >>> table = maketrans('012', '۰۱۲')
        >>> '012'.translate(table)
        '۰۱۲'

    Args:
        a: A string of characters to be replaced.
        b: A string of characters to replace with.

    Returns:
        A dictionary mapping character ordinals to their replacements.
    """
    return {ord(a): b for a, b in zip(a, b, strict=False)}

def words_list(words_file: str | Path = default_words) -> list[tuple[str, int, tuple[str, ...]]]:
    """Returns a list of words from the specified file.

    Examples:
        >>> from hazm.utils import words_list
        >>> words_list()[1]
        ('آب', 549005877, ('N', 'AJ'))

    Args:
        words_file: Path to the words file. Defaults to `default_words`.

    Returns:
        A list of tuples, each containing (word, count, categories).
    """
    file_path = Path(words_file) if isinstance(words_file, str) else words_file

    with file_path.open(encoding="utf-8") as file:
        items = [line.strip().split("\t") for line in file]
        return [
            (item[0], int(item[1]), tuple(item[2].split(",")))
            for item in items
            if len(item) == 3
        ]

def stopwords_list(stopwords_file: str | Path = default_stopwords) -> list[str]:
    """Returns a sorted list of stopwords.

    Examples:
        >>> from hazm.utils import stopwords_list
        >>> stopwords_list()[:4]
        ['آخرین', 'آقای', 'آمد', 'آمده']

    Args:
        stopwords_file: Path to the stopwords file. Defaults to `default_stopwords`.

    Returns:
        A sorted list of unique stopwords.
    """
    file_path = Path(stopwords_file) if isinstance(stopwords_file, str) else stopwords_file

    with file_path.open(encoding="utf-8") as file:
        return sorted({w.strip() for w in file})

def verbs_list() -> list[str]:
    """Returns a list of verbs from the default verbs file.

    Examples:
        >>> from hazm.utils import verbs_list
        >>> verbs_list()[:2]
        ['آباد#آباد', 'آزمای#آزمود']

    Returns:
        A list of verbs.
    """
    with default_verbs.open(encoding="utf-8") as verbs_file:
        return [line.strip() for line in verbs_file]

def past_roots() -> str:
    """Returns a string of past roots joined by a pipe character.

    Examples:
        >>> from hazm.utils import past_roots
        >>> past_roots()[:20]
        'آباد|آزمود|آسود|آشفت'

    Returns:
        A string containing all past roots, suitable for use in regex.
    """
    roots = []
    for verb in verbs_list():
        split = verb.split("#")
        if split and split[0]:
            roots.append(split[0])
    return "|".join(roots)

def present_roots() -> str:
    """Returns a string of present roots joined by a pipe character.

    Examples:
        >>> from hazm.utils import present_roots
        >>> present_roots()[:20]
        'آباد|آزمای|آسای|آشوب'

    Returns:
        A string containing all present roots, suitable for use in regex.
    """
    roots = []
    for verb in verbs_list():
        split = verb.split("#")
        if len(split) >= 2:
            roots.append(split[1])
    return "|".join(roots)

def regex_replace(patterns: list[tuple[str, str]], text: str) -> str:
    """Finds regex patterns and replaces them with the given text.

    Examples:
        >>> from hazm.utils import regex_replace
        >>> patterns = [(r'apples', 'oranges'), (r'red', 'blue')]
        >>> regex_replace(patterns, 'red apples')
        'blue oranges'

    Args:
        patterns: A list of tuples, each containing (pattern, replacement).
        text: The input text to be processed.

    Returns:
        The modified text after all replacements.
    """
    for pattern, repl in patterns:
        if isinstance(pattern, str):
            text = re.sub(pattern, repl, text)
        else:
            text = pattern.sub(repl, text)
    return text
