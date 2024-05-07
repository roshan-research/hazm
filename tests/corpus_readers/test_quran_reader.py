import pytest

from hazm import QuranReader


@pytest.fixture(scope="module")
def quran_reader():
    return QuranReader(quran_file="tests/files/quranic_corpus_morphology.txt")

def test_parts(quran_reader):
    parts = quran_reader.parts()
    assert next(parts)=={"loc": (1, 1, 1, 1), "text": "بِ", "tag": "P"}
    assert next(parts)=={"loc": (1, 1, 1, 2), "text": "سْمِ", "tag": "N", "lem": "ٱسْم", "root": "سمو"}
    assert next(parts)=={"loc": (1, 1, 2, 1), "text": "ٱللَّهِ", "tag": "PN", "lem": "ٱللَّه", "root": "اله"}

def test_words(quran_reader):
    assert next(quran_reader.words())== ("1.1.1", "بِسْمِ", "ٱسْم", "سمو", "P-N", [{"text": "بِ", "tag": "P"}, {"text": "سْمِ", "tag": "N", "lem": "ٱسْم", "root": "سمو"}])
