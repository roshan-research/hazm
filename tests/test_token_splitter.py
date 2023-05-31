import pytest


class TestTokenSplitter:

    @pytest.mark.parametrize(("token", "expected"), [

        ("صداوسیماجمهوری", [("صداوسیما", "جمهوری")]),
        ("صداو", [("صد", "او"), ("صدا", "و")]),
        ("داستان‌سرا", [("داستان", "سرا"), ("داستان‌سرا",)]),
        ("دستان‌سرا", [("دستان", "سرا")]),
        ("", []),
    ])

    def test_split_token_words(self: "TestTokenSplitter", token_splitter, token, expected):
        assert token_splitter.split_token_words(token) == expected
