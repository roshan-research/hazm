from hazm import MirasTextReader


def test_sents():
    mirastext = MirasTextReader(filename="tests/files/mirastext.txt")
    actual = next(mirastext.texts())[:42]
    expected = "ایرانی‌ها چقدر از اینترنت استفاده می‌کنند؟"
    assert actual == expected
