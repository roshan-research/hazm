"""این ماژول شامل کلاس‌ها و توابع کمکی است.

"""

import re
import sys
from os import path
from typing import Any

PY2 = sys.version_info[0] == 2

data_path = path.join(path.dirname(__file__), "data")
default_words = path.join(data_path, "words.dat")
default_stopwords = path.join(data_path, "stopwords.dat")
default_verbs = path.join(data_path, "verbs.dat")
informal_words = path.join(data_path, "iwords.dat")
informal_verbs = path.join(data_path, "iverbs.dat")

NUMBERS = "۰۱۲۳۴۵۶۷۸۹"


def maketrans(A: str, B: str) -> Dict[int, Any]:
    return {ord(a): b for a, b in zip(A, B)}


def words_list(
    words_file: str = default_words,
) -> list[tuple[str, int, tuple[str]]]:
    """لیست کلمات را برمی‌گرداند.

    Examples:
        >>> from hazm.utils import words_list
        >>> words_list()[1]
        ('آب', 549005877, ('N', 'AJ')) #(id, word, (tag1, tag2, ...))

    Args:
        words_file: مسیر فایل حاوی کلمات.

    Returns:
        فهرست کلمات.

    """
    with open(words_file, encoding="utf-8") as words_file:
        items = [line.strip().split("\t") for line in words_file]
        return [
            (item[0], int(item[1]), tuple(item[2].split(",")))
            for item in items
            if len(item) == 3
        ]


def stopwords_list(stopwords_file: str = default_stopwords) -> list[str]:
    """لیست ایست‌واژه‌ها را برمی‌گرداند.

    Examples:
        >>> from hazm.utils import stopwords_list
        >>> stopwords_list()[:4]
        ['محسوب', 'اول', 'بسیار', 'طول']

    Args:
        stopwords_file: مسیر فایل حاوی ایست‌واژه‌ها.

    Returns:
        فهرست ایست‌واژه‌ها.

    """
    with open(stopwords_file, encoding="utf8") as stopwords_file:
        return list({w.strip() for w in stopwords_file})


def verbs_list() -> list[str]:
    with open(default_verbs, encoding="utf8") as verbs_file:
        lst = []
        for line in verbs_file:
            lst.append(line.strip())
        return lst


def past_roots() -> str:
    roots = ""
    for verb in verbs_list():
        split = verb.split("#")
        roots += split[0] + "|"

    return roots[:-1]


def present_roots() -> str:
    roots = ""
    for verb in verbs_list():
        split = verb.split("#")
        roots += split[1] + "|"

    return roots[:-1]


def regex_replace(patterns: str, text: str) -> str:
    for pattern, repl in patterns:
        text = re.sub(pattern, repl, text)
    return text
