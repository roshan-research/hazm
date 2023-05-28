import pytest
from hazm import Normalizer

class TestNormazlier:

    @pytest.fixture(scope="class")
    def normalizer(self):
        return Normalizer()
    
    @pytest.mark.parametrize("input,output", [

        # Multiple spaces between words should be replaced with one space.
        ("سلام    دنیا", "سلام دنیا"),

        # Spaces at the beginning of the string should be removed.
        ("     سلام", "سلام"),

        # Spaces at the end of the string should be removed.
        ("سلام     ", "سلام"),

        # There should be a space after numbers.
        ("مسافت ۹کیلومتر", "مسافت ۹ کیلومتر"),

        # There should be a space before numbers.
        ("مسافت۹ کیلومتر", "مسافت ۹ کیلومتر"),

        # More than one ZWNJ (\u200c) should not be replaced with one ZWNJ.
        ("کاروان‌‌سرا", "کاروان‌سرا"),

        # ZWNJs after spaces should be removed.
        ("سلام ‌‌دنیا", "سلام دنیا"),

        # ZWNJs before spaces should be removed.
        ("سلام‌‌ دنیا", "سلام دنیا"),

        # ZWNJs at the beginning of the string should be removed.
        ("‌‌کاروان‌سرا", "کاروان‌سرا"),

        # ZWNJs at the end of the string should be removed.
        ("کاروان‌سرا‌‌", "کاروان‌سرا"),

        # All kashida (\u0640) should be removed.
        ("ســلام", "سلام"),

        # Add a ZWNJ between ه and ها.
        ("جمعهها مطالعه کنید", "جمعه‌ها مطالعه کنید"),

        # Spaces at the end of a parenthesis should be removed.
        ("(سلام)   ", "(سلام)"),

        # Spaces at the beginning of a parenthesis should be removed.
        ("   (سلام)", "(سلام)"),

        # Spaces at the beginning and end of a parenthesis should be removed.
        ("  (سلام)   ", "(سلام)"),

        # Whitespacess should be removed.
        ("   ", ""),

        # An empty string should return an empty string.
        ("", ""),
    ])

    def test_correct_spacing(self, normalizer, input, output):       
        assert normalizer.correct_spacing(input) == output
