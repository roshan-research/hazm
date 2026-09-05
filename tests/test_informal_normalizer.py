import pytest
from hazm import InformalNormalizer


class TestInformalNormalizer:
    @pytest.fixture(scope="class")
    @classmethod
    def normalizer(cls):
        return InformalNormalizer(seperation_flag=True)

    @pytest.fixture(scope="class")
    @classmethod
    def default_normalizer(cls):
        return InformalNormalizer()

    @pytest.mark.parametrize(
        ("token", "expected"),
        [
            ("تورادوست‌دارم", "تو را دوست دارم"),
            ("تورا دوست دارم", "تو را دوست دارم"),
            ("صداوسیماجمهوری", "صدا و سیما جمهوری"),
            ("کتاب", "کتاب"),
            ("دانشگاه", "دانشگاه"),
        ],
    )
    def test_split_token_words(self, normalizer, token, expected):
        assert normalizer.split_token_words(token) == expected

    def test_split_token_words_with_default_instance(self, default_normalizer):
        # Default instance has seperation_flag=False by default,
        # but split_token_words should automatically initialize words on demand
        assert default_normalizer.split_token_words("تورادوست‌دارم") == "تو را دوست دارم"
        assert default_normalizer.split_token_words("تورا دوست دارم") == "تو را دوست دارم"
