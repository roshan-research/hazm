import pytest


class TestNormazlier:

    @pytest.mark.parametrize(("text", "expected"), [

        ("اِعلاممممم کَرد : « زمین لرزه ای به بُزرگیِ 6 دهم ریشتر ...»", "اعلام کرد: «زمین‌لرزه‌ای به بزرگی ۶ دهم ریشتر …»"),
        ("  ", ""),
        ("", ""),
    ])

    def test_normalize(self: "TestNormazlier", normalizer, text, expected):
        assert normalizer.normalize(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [

        ("سلام    دنیا", "سلام دنیا"),
        ("     سلام", "سلام"),
        ("سلام     ", "سلام"),
        ("مسافت ۹کیلومتر", "مسافت ۹ کیلومتر"),
        ("مسافت۹ کیلومتر", "مسافت ۹ کیلومتر"),
        ("کاروان‌‌سرا", "کاروان‌سرا"), # Replaces more than one ZWNJ (\u200c) with one ZWNJ.
        ("سلام ‌‌دنیا", "سلام دنیا"), # Removes ZWNJs after spaces.
        ("سلام‌‌ دنیا", "سلام دنیا"), # Removes ZWNJs before spaces.
        ("‌‌کاروان‌سرا", "کاروان‌سرا"), # Removes ZWNJs at the beginning of the string.
        ("کاروان‌سرا‌‌", "کاروان‌سرا"), # Removes ZWNJs at the end of the string.
        ("ســلام", "سلام"),
        ("جمعهها مطالعه کنید", "جمعه‌ها مطالعه کنید"),
        ("لحظه هایی سخت", "لحظه‌هایی سخت"),
        ("   (سلام)", "(سلام)"),
        ("(سلام)   ", "(سلام)"),
        ("  (سلام)   ", "(سلام)"),
        ("   ", ""),
        ("", ""),
    ])

    def test_correct_spacing(self: "TestNormazlier", normalizer, text, expected):
        assert normalizer.correct_spacing(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [
        ("حَذفِ اِعراب", "حذف اعراب"),
        ("آمدند", "آمدند"),
        ("متن بدون اعراب", "متن بدون اعراب"),
        ("  ", "  "),
        ("", ""),

    ])

    def test_remove_diacritics(self: "TestNormazlier", normalizer, text, expected):
        assert normalizer.remove_diacritics(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [
        ("پیامبر اکرم ﷺ", "پیامبر اکرم "),
        ("سلام", "سلام"),
        ("", ""),

    ])

    def test_remove_specials_chars(self: "TestNormazlier", normalizer, text, expected):
        assert normalizer.remove_specials_chars(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [

        ("سلاممم دوستان", "سلام دوستان"), # Replaces 3+ repeated chars with one.
        ("سلامم را برسان", "سلامم را برسان"),  # Does not replace 3- repeated chars because they may have meaning.

        pytest.param("سلاممم را برسان", "سلامم را برسان", marks=pytest.mark.xfail(reason="some bug")),
        pytest.param("سلامم دوستان", "سلام دوستان", marks=pytest.mark.xfail(reason="some bug")),

    ])

    def test_decrease_repeated_chars(self: "TestNormazlier", normalizer, text, expected):
        assert normalizer.decrease_repeated_chars(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [

        ('"نقل‌قول"', "«نقل‌قول»"),
        ("و...", "و …"),
        ("10.450", "10٫450"),
        ("سلام", "سلام"),
        ("  ", "  "),
        ("", ""),

    ])

    def test_persian_style(self: "TestNormazlier", normalizer, text, expected):
        assert normalizer.persian_style(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [

        ("ساعت 18", "ساعت ۱۸"),
        ("ساعت ۱۸", "ساعت ۱۸"),
        ("  ", "  "),
        ("", ""),
    ])

    def test_persian_number(self: "TestNormazlier", normalizer, text, expected):
        assert normalizer.persian_number(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [

        ("﷽", "بسم الله الرحمن الرحیم"),
        ("  ", "  "),
        ("", ""),
    ])

    def test_unicodes_replacement(self: "TestNormazlier", normalizer, text, expected):
        assert normalizer.unicodes_replacement(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [

        ("نمیدانم چه میگفت", "نمی‌دانم چه می‌گفت"),
        ("میز", "میز"),
        ("میانه", "میانه"),
        ("ماهان", "ماهان"),
        ("  ", "  "),
        ("", ""),
    ])

    def test_seperate_mi(self:"TestNormazlier", normalizer, text, expected):
        assert normalizer.seperate_mi(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [

        (["کتاب", "ها"], ["کتاب‌ها"]),
        (["کتاب", "های"], ["کتاب‌های"]),
        (["کتاب", "هایی"], ["کتاب‌هایی"]),
        (["او", "می", "رود"], ["او", "می‌رود"]),
        (["ماه", "می", "سال", "جدید"], ["ماه", "می", "سال", "جدید"]),
        (["اخلال", "گر"], ["اخلال‌گر"]),
        (["زمین", "لرزه", "ای"], ["زمین‌لرزه‌ای"]),
        ([],[]),

    ])

    def test_token_spacing(self: "TestNormazlier", normalizer, text, expected):
        assert normalizer.token_spacing(text) == expected
