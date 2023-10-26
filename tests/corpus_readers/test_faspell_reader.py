from hazm import FaSpellReader


def test_main_entries():
    faspell = FaSpellReader(corpus_folder="tests/files/faspell")
    actual = next(faspell.main_entries())
    expected = ("آاهي", "آگاهي", 1)
    assert actual == expected

def test_ocr_entries():
    faspell = FaSpellReader(corpus_folder="tests/files/faspell")
    actual = next(faspell.ocr_entries())
    expected = ("آ!دبم", "آمدیم")
    assert actual == expected
