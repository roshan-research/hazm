"""Regression tests covering recently fixed edge-case bugs.

Each test in this module pins the corrected behaviour of a specific fix so that
an accidental regression turns the suite red. The fixes covered here are:

* Stemmer no longer collapses suffix-only words to an empty/1-char stem.
* WordTokenizer.join_verb_parts no longer drops a trailing "before verb".
* Lemmatizer no longer maps '' / single characters to a verb lemma.
* Normalizer reuses cached translation tables and its decimal-separator rule
  only fires between digits.
* POSTagger.features tolerates empty-string tokens instead of raising.
"""

import re

import pytest

from hazm import Normalizer
from hazm import WordTokenizer
from hazm.utils import maketrans
from hazm.utils import regex_replace


class TestStemmerEdgeCases:
    """A multi-character suffix must never leave an empty/1-char stem."""

    @pytest.mark.parametrize(("word", "expected"), [
        ("ها", "ها"),
        ("رها", "رها"),
        ("های", "های"),
        ("تر", "تر"),
        ("ان", "ان"),
    ])
    def test_suffix_only_word_is_preserved(self, stemmer, word, expected):
        assert stemmer.stem(word) == expected

    def test_known_suffix_still_stripped(self, stemmer):
        assert stemmer.stem("کتاب‌ها") == "کتاب"
        assert stemmer.stem("کتابی") == "کتاب"


class TestJoinVerbParts:
    """A "before verb" at the end of the token list must be preserved."""

    def test_trailing_before_verb_is_not_dropped(self, word_tokenizer):
        assert word_tokenizer.join_verb_parts(["کتاب", "خواهد"]) == ["کتاب", "خواهد"]

    def test_single_token_passthrough(self, word_tokenizer):
        assert word_tokenizer.join_verb_parts(["رفت"]) == ["رفت"]

    def test_regular_join_still_works(self, word_tokenizer):
        assert word_tokenizer.join_verb_parts(["خواهد", "رفت"]) == ["خواهد_رفت"]
        assert word_tokenizer.join_verb_parts(["رفته", "است"]) == ["رفته_است"]


class TestWordTokenizerEmptyInput:
    def test_empty_and_whitespace_only(self, word_tokenizer):
        assert word_tokenizer.tokenize("") == []
        assert word_tokenizer.tokenize("   ") == []
        assert word_tokenizer.tokenize("\n\t") == []


class TestWordTokenizerReplacements:
    def test_replace_emails(self):
        tokenizer = WordTokenizer(join_verb_parts=False, replace_emails=True)
        assert "EMAIL" in tokenizer.tokenize("تماس a.b@example.com بگیرید")

    def test_replace_hashtags(self):
        tokenizer = WordTokenizer(join_verb_parts=False, replace_hashtags=True)
        assert tokenizer.tokenize("موضوع #علم_داده") == ["موضوع", "TAG", "علم", "داده"]


class TestLemmatizer:
    def test_empty_string_returns_empty(self, lemmatizer):
        assert lemmatizer.lemmatize("") == ""

    def test_single_char_not_mapped_to_verb(self, lemmatizer):
        # Previously the empty past-root entry '#هست' injected keys like 'م'
        # that made these resolve to a verb lemma.
        assert lemmatizer.lemmatize("م") == "م"
        assert lemmatizer.lemmatize("ی") == "ی"

    def test_verb_still_lemmatized(self, lemmatizer):
        assert lemmatizer.lemmatize("می‌روم") == "رفت#رو"

    def test_pos_branches(self, lemmatizer):
        assert lemmatizer.lemmatize("او", pos="PRON") == "او"
        assert lemmatizer.lemmatize("اجتماعی", pos="ADJ") == "اجتماعی"


class TestNormalizer:
    def test_module_translation_tables_match_maketrans(self):
        from hazm.constants import NUMBERS_DST
        from hazm.constants import NUMBERS_SRC
        from hazm.constants import TRANSLATION_DST
        from hazm.constants import TRANSLATION_SRC
        from hazm.normalizer import _NUMBERS_TABLE
        from hazm.normalizer import _TRANSLATION_TABLE

        assert maketrans(TRANSLATION_SRC, TRANSLATION_DST) == _TRANSLATION_TABLE
        assert maketrans(NUMBERS_SRC, NUMBERS_DST) == _NUMBERS_TABLE

    def test_persian_numbers_flag_disables_conversion(self):
        normalizer = Normalizer(persian_numbers=False)
        assert normalizer.normalize("ساعت 18") == "ساعت 18"

    def test_unicodes_replacement_examples(self, normalizer):
        assert normalizer.unicodes_replacement("ﷲ") == "الله"
        assert normalizer.unicodes_replacement("﷽") == "بسم الله الرحمن الرحیم"

    def test_decimal_separator_only_between_digits(self, normalizer):
        assert normalizer.persian_style("10.450") == "10٫450"
        # A lone '+.' must no longer be treated as a number boundary.
        assert normalizer.persian_style("a+.+b") == "a+.+b"


class TestPosTaggerFeatures:
    def test_empty_token_does_not_raise(self, pos_tagger):
        features = pos_tagger.features(["", "خانه"], 0)
        assert features["word"] == ""
        assert features["prefix-1"] == ""
        assert features["suffix-1"] == ""

    def test_normal_token_features(self, pos_tagger):
        features = pos_tagger.features(["خانه"], 0)
        assert features["prefix-1"] == "خ"
        assert features["suffix-1"] == "ه"


class TestUtils:
    def test_maketrans(self):
        table = maketrans("012", "۰۱۲")
        assert "012".translate(table) == "۰۱۲"

    def test_regex_replace_with_string_pattern(self):
        assert regex_replace([(r"red", "blue")], "red apples") == "blue apples"

    def test_regex_replace_with_compiled_pattern(self):
        patterns = [(re.compile(r"red"), "blue")]
        assert regex_replace(patterns, "red apples") == "blue apples"


class TestSentenceTokenizer:
    def test_empty_input(self, sentence_tokenizer):
        assert sentence_tokenizer.tokenize("") == []

    def test_multiple_terminators(self, sentence_tokenizer):
        assert sentence_tokenizer.tokenize("واقعا؟! بله.") == ["واقعا؟!", "بله."]
