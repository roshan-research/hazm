import pytest

from hazm import MizanReader


@pytest.fixture(scope="module")
def mizan_reader():
    return MizanReader("tests/files/mizan")

def test_english_sentences(mizan_reader):
    first_sentence = next(mizan_reader.english_sentences())
    assert first_sentence == "The story which follows was first written out in Paris during the Peace Conference"

def test_persian_sentences(mizan_reader):
    first_sentence = next(mizan_reader.persian_sentences())
    print(first_sentence)
    assert first_sentence == "داستانی که از نظر شما می‌گذرد، ابتدا ضمن کنفرانس صلح پاریس از روی یادداشت‌هائی که به طور روزانه در حال خدمت در صف برداشته شده بودند"

def test_english_persian_sentences(mizan_reader):
    sentence_pairs = next(mizan_reader.english_persian_sentences())
    assert sentence_pairs == ("The story which follows was first written out in Paris during the Peace Conference", "داستانی که از نظر شما می\u200cگذرد، ابتدا ضمن کنفرانس صلح پاریس از روی یادداشت\u200cهائی که به طور روزانه در حال خدمت در صف برداشته شده بودند")
