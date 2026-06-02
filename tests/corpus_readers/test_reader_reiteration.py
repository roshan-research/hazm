"""Regression tests: corpus readers must be iterable more than once.

Several readers stored ``Path(...).glob(...)`` (a one-shot iterator) on the
instance, so a second call to ``sents()`` / ``docs()`` silently yielded nothing.
They now materialize the file list, so repeated iteration returns the same data.
The Degarbayan reader additionally used to raise ``NameError`` (undefined ``e``)
instead of ``FileNotFoundError`` when the corpus file was missing.
"""

import pytest

from hazm import ArmanReader
from hazm import DegarbayanReader
from hazm import NaabReader
from hazm import NerReader
from hazm import PnSummaryReader


def test_arman_reader_is_reiterable():
    arman = ArmanReader(corpus_folder="tests/files/arman", subset="test")
    first = list(arman.sents())
    second = list(arman.sents())
    assert first
    assert first == second


def test_naab_reader_is_reiterable():
    naab = NaabReader("tests/files/naab", "test")
    first = list(naab.sents())
    second = list(naab.sents())
    assert first
    assert first == second


def test_ner_reader_is_reiterable():
    ner = NerReader("tests/files/ner")
    first = list(ner.sents())
    second = list(ner.sents())
    assert first
    assert first == second


def test_pn_summary_reader_is_reiterable():
    pn_summary = PnSummaryReader("tests/files/pn-summary", "test")
    first = list(pn_summary.docs())
    second = list(pn_summary.docs())
    assert first
    assert first == second


def test_degarbayan_missing_file_raises_filenotfound():
    reader = DegarbayanReader(
        root="tests/files/degarbayan",
        corpus_file="this_file_does_not_exist.xml",
    )
    with pytest.raises(FileNotFoundError):
        next(reader.docs())
