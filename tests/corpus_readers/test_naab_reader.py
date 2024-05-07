from hazm import NaabReader


def test_sents():
    ner = NaabReader("tests/files/naab","test")
    sentence = next(ner.sents())
    assert sentence == "این وبلاگ زیر نظر وب‌های زیر به کار خود ادامه می‌دهد"
