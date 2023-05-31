from hazm import BijankhanReader


def test_sents():
    bijankhan = BijankhanReader(bijankhan_file="corpora/bijankhan.txt")
    actual = next(bijankhan.sents())
    expected = [("اولین", "ADJ"), ("سیاره", "N"), ("خارج", "ADJ"), ("از", "PREP"), ("منظومه", "N"), ("شمسی", "ADJ"), ("دیده_شد", "V"), (".", "PUNC")]
    assert actual == expected
