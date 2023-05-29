import pytest
from hazm import Normalizer

class TestNormazlier:

    @pytest.fixture(scope="class")
    def normalizer(self):
        return Normalizer()
    
    @pytest.mark.parametrize("text,expected", [

        # Replaces multiple spaces between words with one space.
        ("سلام    دنیا", "سلام دنیا"),

        # Removes spaces at the beginning of the string.
        ("     سلام", "سلام"),

        # Removes spaces at the end of the string.
        ("سلام     ", "سلام"),

        # Adds a space after numbers.
        ("مسافت ۹کیلومتر", "مسافت ۹ کیلومتر"),

        # Adds a space before numbers.
        ("مسافت۹ کیلومتر", "مسافت ۹ کیلومتر"),

        # Replaces more than one ZWNJ (\u200c) with one ZWNJ.
        ("کاروان‌‌سرا", "کاروان‌سرا"),

        # Removes ZWNJs after spaces.
        ("سلام ‌‌دنیا", "سلام دنیا"),

        # Removes ZWNJs before spaces.
        ("سلام‌‌ دنیا", "سلام دنیا"),

        # Removes ZWNJs at the beginning of the string.
        ("‌‌کاروان‌سرا", "کاروان‌سرا"),

        # Removes ZWNJs at the end of the string.
        ("کاروان‌سرا‌‌", "کاروان‌سرا"),

        # Removes all kashida (\u0640).
        ("ســلام", "سلام"),

        # Adds a ZWNJ between ه and ها.
        ("جمعهها مطالعه کنید", "جمعه‌ها مطالعه کنید"),

        # Removes spaces at the beginning of a punctuation.
        ("   (سلام)", "(سلام)"),
        
        # Removes spaces at the end of a punctuation.
        ("(سلام)   ", "(سلام)"),

        # Removes spaces at the beginning and end of a punctuation.
        ("  (سلام)   ", "(سلام)"),

        # Returns an empty string if the input consists only of whitespace characters.
        ("   ", ""),

        # Returns an empty string if the input is empty.
        ("", ""),
    ])

    def test_correct_spacing(self, normalizer, text, expected):       
        assert normalizer.correct_spacing(text) == expected

    @pytest.mark.parametrize("text,expected", [
        
        # Removes any diacritical.
        ("حَذفِ اِعراب", "حذف اعراب"),

        # Does not remove آ.
        ("آمدند", "آمدند"),

        # Returns original string if no diacritics.
        ("متن بدون اعراب", "متن بدون اعراب"),
        ("  ", "  "),
        ("", ""),

    ])

    def test_remove_diacritics(self, normalizer, text, expected):       
        assert normalizer.remove_diacritics(text) == expected

    @pytest.mark.parametrize("text,expected", [
        
        # Removes any specials characters.
        ("پیامبر اکرم ﷺ", "پیامبر اکرم "),

        # Returns original string if no specials characters.
        ("سلام", "سلام"),
        ("", ""),

    ])

    def test_remove_specials_chars(self, normalizer, text, expected):       
        assert normalizer.remove_specials_chars(text) == expected

    @pytest.mark.parametrize("text,expected", [
        
        # Replaces 3+ repeated chars with one.
        ("سلاممم دوستان", "سلام دوستان"),

        # Keeps 3- repeated chars because they may have meaning.
        ("سلامم را برسان", "سلامم را برسان"),

        pytest.param("سلاممم را برسان", "سلامم را برسان", marks=pytest.mark.xfail(reason='some bug')),
        pytest.param("سلامم دوستان", "سلام دوستان", marks=pytest.mark.xfail(reason='some bug')),        

    ])

    def test_decrease_repeated_chars(self, normalizer, text, expected):       
        assert normalizer.decrease_repeated_chars(text) == expected
