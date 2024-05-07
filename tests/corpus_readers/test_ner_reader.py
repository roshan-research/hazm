from hazm import NerReader


def test_sents():
    ner = NerReader("tests/files/ner")
    sentence = next(ner.sents())
    assert sentence == [("ویکی‌پدیای", "O"), ("انگلیسی", "O"), ("در", "B-DAT"), ("تاریخ", "I-DAT"), ("۱۵", "I-DAT"), ("ژانویه", "I-DAT"), ("۲۰۰۱", "I-DAT"), ("(", "O"), ("میلادی", "B-DAT"), (")", "O"), ("۲۶", "B-DAT"), ("دی", "I-DAT"), ("۱۳۷۹", "I-DAT"), (")", "O"), ("به", "O"), ("صورت", "O"), ("مکملی", "O"), ("برای", "O"), ("دانشنامه", "O"), ("تخصصی", "O"), ("نوپدیا", "O"), ("نوشته", "O"), ("شد", "O"), (".", "O")]
