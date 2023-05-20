"""این ماژول شامل کلاس‌ها و توابع کمکی است."""

import re
from os import path
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

data_path = Path(__file__).parent / "data"

default_words = Path(data_path) / "words.dat"
default_stopwords = Path(data_path) / "stopwords.dat"
default_verbs = Path(data_path) / "verbs.dat"
informal_words = Path(data_path) / "iwords.dat"
informal_verbs = Path(data_path) / "iverbs.dat"

NUMBERS = "۰۱۲۳۴۵۶۷۸۹"


def maketrans(a: str, b: str) -> Dict[int, Any]:
    """هر یک از حروف رشتهٔ a را به یک حرف در رشتهٔ b مپ می‌کند."""
    return {ord(a): b for a, b in zip(a, b)}


def words_list(
    words_file: str = default_words,
) -> List[Tuple[str, int, Tuple[str]]]:
    """لیست کلمات را برمی‌گرداند.

    Examples:
        >>> from hazm.utils import words_list
        >>> words_list()[1]
        ('آب', 549005877, ('N', 'AJ'))

    Args:
        words_file: مسیر فایل حاوی کلمات.

    Returns:
        فهرست کلمات.

    """
    with Path.open(words_file, encoding="utf-8") as words_file:
        items = [line.strip().split("\t") for line in words_file]
        return [
            (item[0], int(item[1]), tuple(item[2].split(",")))
            for item in items
            if len(item) == 3
        ]


def stopwords_list(stopwords_file: str = default_stopwords) -> List[str]:
    """لیست ایست‌واژه‌ها را برمی‌گرداند.

    Examples:
        >>> from hazm.utils import stopwords_list
        >>> stopwords_list()[:4]
        ['آخرین', 'آقای', 'آمد', 'آمده']

    Args:
        stopwords_file: مسیر فایل حاوی ایست‌واژه‌ها.

    Returns:
        فهرست ایست‌واژه‌ها.

    """
    with Path.open(stopwords_file, encoding="utf8") as stopwords_file:
        return sorted({w.strip() for w in stopwords_file})


def verbs_list() -> List[str]:
    """لیست افعال را برمی‌گرداند."""
    with Path.open(default_verbs, encoding="utf8") as verbs_file:
        lst = []
        for line in verbs_file:
            lst.append(line.strip())
        return lst


def past_roots() -> str:
    """لیست بن‌های گذشته را برمی‌گرداند."""
    roots = ""
    for verb in verbs_list():
        split = verb.split("#")
        roots += split[0] + "|"

    return roots[:-1]


def present_roots() -> str:
    """لیست بن‌های مضارع را برمی‌گرداند."""
    roots = ""
    for verb in verbs_list():
        split = verb.split("#")
        roots += split[1] + "|"

    return roots[:-1]


def regex_replace(patterns: str, text: str) -> str:
    """الگوی ریجکس را یافته و با متن داده شده جایگزین می‌کند."""
    for pattern, repl in patterns:
        text = re.sub(pattern, repl, text)
    return text

