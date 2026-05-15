import pytest

from hazm import InformalNormalizer


class TestInformalNormalizer:

    @pytest.mark.parametrize(("token", "expected"), [
        ("تورادوست دارم", "تو را دوست دارم"),
        ("تورادوست‌دارم", "تو را دوست دارم"),
        ("تورا دوست دارم", "تو را دوست دارم"),
    ])
    def test_split_token_words(self: "TestInformalNormalizer", token, expected):
        normalizer = InformalNormalizer()
        assert normalizer.split_token_words(token) == expected

    @pytest.mark.parametrize(("token", "expected"), [
        ("من تورادوست دارم", "من تو را دوست دارم"),
        ("همین‌تورادوست‌دارم", "همین تو را دوست دارم"),
    ])
    def test_split_token_words_in_sentence(self: "TestInformalNormalizer", token, expected):
        normalizer = InformalNormalizer()
        assert normalizer.split_token_words(token) == expected
