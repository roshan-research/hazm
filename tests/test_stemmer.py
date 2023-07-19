import pytest


class TestStemmer:

    @pytest.mark.parametrize(("word", "expected"), [

        ("کتابی", "کتاب"),
        ("کتاب‌ها", "کتاب"),
        ("کتاب‌هایی", "کتاب"),
        ("کتابهایشان", "کتاب"),
        ("اندیشه‌اش", "اندیشه"),
        ("خانهٔ", "خانه"),        
        ("  ", "  "),
        ("", ""),
    ])

    def test_stem(self: "TestStemmer", stemmer, word, expected):
        assert stemmer.stem(word) == expected
