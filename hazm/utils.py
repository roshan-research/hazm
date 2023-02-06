# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابع کمکی است.
"""

import re
import sys, codecs
from os import path

PY2 = sys.version_info[0] == 2

data_path = path.join(path.dirname(__file__), "data")
default_words = path.join(data_path, "words.dat")
default_stopwords = path.join(data_path, "stopwords.dat")
default_verbs = path.join(data_path, "verbs.dat")
informal_words = path.join(data_path, "iwords.dat")
informal_verbs = path.join(data_path, "iverbs.dat")

NUMBERS = "۰۱۲۳۴۵۶۷۸۹"

maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))


def words_list(words_file=default_words):
    """لیست کلمات را برمی‌گرداند.

    Examples:
            >>> from hazm.utils import words_list
            >>> words_list()[1]
            ('آب', 549005877, ('N', 'AJ')) #(id, word, (tag1, tag2, ...))

    Args:
            words_file (str, optional): مسیر فایل حاوی کلمات.

    Returns:
            (Tuple[str,str,Tuple[str,str]]): فهرست کلمات.
    """
    with codecs.open(words_file, encoding="utf-8") as words_file:
        items = [line.strip().split("\t") for line in words_file]
        return [
            (item[0], int(item[1]), tuple(item[2].split(",")))
            for item in items
            if len(item) == 3
        ]


def stopwords_list(stopwords_file=default_stopwords):
    """لیست ایست‌واژه‌ها را برمی‌گرداند.

    Examples:
            >>> from hazm.utils import stopwords_list
            >>> stopwords_list()[:4]
            ['محسوب', 'اول', 'بسیار', 'طول']

    Args:
            stopwords_file (str, optional): مسیر فایل حاوی ایست‌واژه‌ها.

    Returns:
            (List[str]): فهرست ایست‌واژه‌ها.
    """
    with codecs.open(stopwords_file, encoding="utf8") as stopwords_file:
        return list(set(map(lambda w: w.strip(), stopwords_file)))


def verbs_list():
    with codecs.open(default_verbs, encoding="utf8") as verbs_file:
        list = []
        for line in verbs_file:
            list.append(line.strip())
        return list


def past_roots():
    roots = ""
    for verb in verbs_list():
        split = verb.split("#")
        roots += split[0] + "|"

    return roots[:-1]


def present_roots():
    roots = ""
    for verb in verbs_list():
        split = verb.split("#")
        roots += split[1] + "|"

    return roots[:-1]


def regex_replace(patterns, text):
    for pattern, repl in patterns:
        text = re.sub(pattern, repl, text)
    return text


"""
def generate_all_verb_forms(ri, rii):
    list = []
    return [
        ri+"م",
        ri + "ی",
        ri,
        ri + "یم",
        ri + "ید",
        ri + "ند",

        ri + "ه‌ام",
        ri + "ه‌ای",
        ri + "ه است",
        ri + "ه‌ایم",
        ri + "ه‌اید",
        ri + "ه‌اند",

        "می‌"+ri+"م",
        "می‌"+ri + "ی",
        "می‌"+ri,
        "می‌"+ri + "یم",
        "می‌"+ri + "ید",
        "می‌"+ri + "ند",

        "می‌"+ri+"ه‌ام",
        "می‌"+ri+"ه‌ای",
        "می‌"+ri+"ه است",
        "می‌"+ri+"ه‌ایم",
        "می‌"+ri+"ه‌اید",
        "می‌"+ri+"ه‌اند",

        ri+"ه بودم",
        ri+"ه بودی",
        ri+"ه بود",
        ri+"ه بودیم",
        ri+"ه بودید",
        ri+"ه بودند",

        ri+"ه بوده‌ام",
        ri+"ه بوده‌ای",
        ri+"ه بوده است",
        ri+"ه بوده‌ایم",
        ri+"ه بوده‌اید",
        ri+"ه بوده‌اند",

        ri+"ه باشم",
        ri+"ه باشی",
        ri+"ه باشد",
        ri+"ه باشیم",
        ri+"ه باشید",
        ri+"ه باشند",

        "داشتم "+"می‌"+ri+"م",
        "داشتی "+"می‌"+ri+"ی",
        "داشت "+"می‌"+ri,
        "داشتیم "+"می‌"+ri+"یم",
        "داشتید "+"می‌"+ri+"ید",
        "داشتند "+"می‌"+ri+"ند",

        "داشته‌ام "+"می‌"+ri+"ه‌ام",
        "داشته‌ای "+"می‌"+ri+"ه‌ای",
        "داشته است "+"می‌"+ri+"ه است",
        "داشته‌ایم "+"می‌"+ri+"ه ایم",
        "داشته‌اید "+"می‌"+ri+"ه‌اید",
        "داشته‌اند "+"می‌"+ri+"ه‌اند",

        "می‌"+rii+"م",
        "می‌"+rii+"ی",
        "می‌"+rii+"د",
        "می‌"+rii+"یم",
        "می‌"+rii+"ید",
        "می‌"+rii+"ند",

        "ب"+rii+"م",
        "ب"+rii+"ی",
        "ب"+rii+"د",
        "ب"+rii+"یم",
        "ب"+rii+"ید",
        "ب"+rii+"ند",

        "دارم می‌"+rii+"م",
        "داری می‌"+rii+"ی",
        "دارد می‌"+rii+"د",
        "داریم می‌"+rii+"یم",
        "دارید می‌"+rii+"ید",
        "دارند می‌"+rii+"ند",

        "خواهم "+ri,
        "خواهی "+ri,
        "خواهد "+ri,
        "خواهیم "+ri,
        "خواهید "+ri,
        "خواهند "+ri,
    ]
"""
