"""This module contains classes and functions for text normalization."""

import re

from hazm.api import NormalizerProtocol
from hazm.constants import AFFIX_SPACING_PATTERNS
from hazm.constants import DIACRITICS_PATTERNS
from hazm.constants import EXTRA_SPACE_PATTERNS
from hazm.constants import NUMBERS_DST
from hazm.constants import NUMBERS_SRC
from hazm.constants import PERSIAN_STYLE_PATTERNS
from hazm.constants import PUNCTUATION_SPACING_PATTERNS
from hazm.constants import SPECIAL_CHARS_PATTERNS
from hazm.constants import SUFFIXES
from hazm.constants import TRANSLATION_DST
from hazm.constants import TRANSLATION_SRC
from hazm.constants import UNICODE_REPLACEMENTS
from hazm.lemmatizer import Lemmatizer
from hazm.utils import maketrans
from hazm.utils import regex_replace
from hazm.word_tokenizer import WordTokenizer


class Normalizer(NormalizerProtocol):
    """This class includes functions for text normalization."""

    def __init__(
        self,
        correct_spacing: bool = True,
        remove_diacritics: bool = True,
        remove_specials_chars: bool = True,
        decrease_repeated_chars: bool = True,
        persian_style: bool = True,
        persian_numbers: bool = True,
        unicodes_replacement: bool = True,
        seperate_mi: bool = True,
    ) -> None:
        """Constructor.

        Args:
            correct_spacing: If True, corrects spacing in text, punctuation, prefixes, and suffixes.
            remove_diacritics: If True, removes diacritics from characters.
            remove_specials_chars: If True, removes special characters not useful for text processing.
            decrease_repeated_chars: If True, reduces character repetitions greater than 2 to 2.
            persian_style: If True, applies Persian-specific style corrections (e.g., replacing quotes with guillemets).
            persian_numbers: If True, replaces English numbers with Persian numbers.
            unicodes_replacement: If True, replaces certain Unicode characters with their normalized equivalents.
            seperate_mi: If True, separates the 'mi' prefix in verbs.
        """
        self._correct_spacing = correct_spacing
        self._remove_diacritics = remove_diacritics
        self._remove_specials_chars = remove_specials_chars
        self._decrease_repeated_chars = decrease_repeated_chars
        self._persian_style = persian_style
        self._persian_number = persian_numbers
        self._unicodes_replacement = unicodes_replacement
        self._seperate_mi = seperate_mi

        # Lazy loading
        self._tokenizer: WordTokenizer | None = None
        self._words: dict[str, tuple[int, tuple[str, ...]]] | None = None
        self._verbs: set[str] | None = None

        if self._correct_spacing or self._decrease_repeated_chars:
            self._tokenizer = WordTokenizer(join_verb_parts=False)
            self._words = self._tokenizer.words

        if self._seperate_mi:
            self._verbs = set(Lemmatizer(joined_verb_parts=False).verbs.keys())

        if self._decrease_repeated_chars:
            self.more_than_two_repeat_pattern = re.compile(
                r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])\1{2,}",
            )
            self.repeated_chars_pattern = re.compile(
                r"[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]*"
                 r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])\1{2,}"
                 r"[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]*",
            )

    def normalize(self, text: str) -> str:
        """Normalizes the text.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.normalize('اِعلاممممم کَرد : « زمین لرزه ای به بُزرگیِ 6 دهم ریشتر ...»')
            'اعلام کرد: «زمین‌لرزه‌ای به بزرگی ۶ دهم ریشتر …»'
            >>> normalizer.normalize('')
            ''

        Args:
            text: The text to be normalized.

        Returns:
            The normalized text.
        """
        translations = maketrans(TRANSLATION_SRC, TRANSLATION_DST)
        text = text.translate(translations)

        if self._persian_style:
            text = self.persian_style(text)

        if self._persian_number:
            text = self.persian_number(text)

        if self._remove_diacritics:
            text = self.remove_diacritics(text)

        if self._correct_spacing:
            text = self.correct_spacing(text)

        if self._unicodes_replacement:
            text = self.unicodes_replacement(text)

        if self._remove_specials_chars:
            text = self.remove_specials_chars(text)

        if self._decrease_repeated_chars:
            text = self.decrease_repeated_chars(text)

        if self._seperate_mi:
            text = self.seperate_mi(text)

        return text

    def correct_spacing(self, text: str) -> str:
        """Corrects spacing in text.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.correct_spacing("سلام   دنیا")
            'سلام دنیا'
            >>> normalizer.correct_spacing("به طول ۹متر و عرض۶")
            'به طول ۹ متر و عرض ۶'
            >>> normalizer.correct_spacing("کاروان‌‌سرا")
            'کاروان‌سرا'
            >>> normalizer.correct_spacing("‌سلام‌ به ‌همه‌")
            'سلام به همه'
            >>> normalizer.correct_spacing("سلام دنیـــا")
            'سلام دنیا'
            >>> normalizer.correct_spacing("جمعهها که کار نمی کنم مطالعه می کنم")
            'جمعه‌ها که کار نمی‌کنم مطالعه می‌کنم'
            >>> normalizer.correct_spacing(' "سلام به همه"   ')
            '"سلام به همه"'
            >>> normalizer.correct_spacing('')
            ''

        Args:
            text: The text to correct spacing for.

        Returns:
            The text with corrected spacing.
        """
        text = regex_replace(EXTRA_SPACE_PATTERNS, text)

        lines = text.split("\n")
        result = []
        for line in lines:
            if not line.strip():
                result.append(line)
                continue

            if self._tokenizer:
                tokens = self._tokenizer.tokenize(line)
                spaced_tokens = self.token_spacing(tokens)
                line = " ".join(spaced_tokens)

            result.append(line)

        text = "\n".join(result)
        text = regex_replace(AFFIX_SPACING_PATTERNS, text)
        return regex_replace(PUNCTUATION_SPACING_PATTERNS, text)

    def remove_diacritics(self, text: str) -> str:
        """Removes diacritics from the text.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.remove_diacritics('حَذفِ اِعراب')
            'حذف اعراب'
            >>> normalizer.remove_diacritics('آمدند')
            'آمدند'
            >>> normalizer.remove_diacritics('متن بدون اعراب')
            'متن بدون اعراب'
            >>> normalizer.remove_diacritics('')
            ''

        Args:
            text: The text to remove diacritics from.

        Returns:
            The text without diacritics.
        """
        return regex_replace(DIACRITICS_PATTERNS, text)

    def remove_specials_chars(self, text: str) -> str:
        """Removes special characters from the text.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.remove_specials_chars('پیامبر اکرم ﷺ')
            'پیامبر اکرم '

        Args:
            text: The text to remove special characters from.

        Returns:
            The text without special characters.
        """
        return regex_replace(SPECIAL_CHARS_PATTERNS, text)

    def decrease_repeated_chars(self, text: str) -> str:
        """Reduces character repetitions greater than 2 to 2.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.decrease_repeated_chars('سلامممم به همه')
            'سلام به همه'
            >>> normalizer.decrease_repeated_chars('سلامم به همه')
            'سلامم به همه'
            >>> normalizer.decrease_repeated_chars('سلامم را برسان')
            'سلامم را برسان'
            >>> normalizer.decrease_repeated_chars('سلاممم را برسان')
            'سلام را برسان'
            >>> normalizer.decrease_repeated_chars('')
            ''

        Args:
            text: The text to reduce repeated characters in.

        Returns:
            The text with reduced character repetitions.
        """
        matches = list(self.repeated_chars_pattern.finditer(text))
        for m in reversed(matches):
            word = m.group()
            if self._words and word not in self._words:
                no_repeat = self.more_than_two_repeat_pattern.sub(r"\1", word)
                two_repeat = self.more_than_two_repeat_pattern.sub(r"\1\1", word)

                if (no_repeat in self._words) != (two_repeat in self._words):
                    r = no_repeat if no_repeat in self._words else two_repeat
                    text = text[:m.start()] + text[m.start():m.end()].replace(word, r) + text[m.end():]
                else:
                    text = text[:m.start()] + text[m.start():m.end()].replace(word, two_repeat) + text[m.end():]
        return text

    def persian_style(self, text: str) -> str:
        """Applies Persian style corrections to the text.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.persian_style('"نرمال‌سازی"')
            '«نرمال‌سازی»'
            >>> normalizer.persian_style('و ...')
            'و …'
            >>> normalizer.persian_style('10.450')
            '10٫450'
            >>> normalizer.persian_style('')
            ''

        Args:
            text: The text to apply Persian style corrections to.

        Returns:
            The text with Persian style corrections.
        """
        return regex_replace(PERSIAN_STYLE_PATTERNS, text)

    def persian_number(self, text: str) -> str:
        """Replaces English numbers with Persian numbers.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.persian_number('5 درصد')
            '۵ درصد'
            >>> normalizer.persian_number('۵ درصد')
            '۵ درصد'
            >>> normalizer.persian_number('')
            ''

        Args:
            text: The text to replace English numbers in.

        Returns:
            The text with Persian numbers.
        """
        translations = maketrans(NUMBERS_SRC, NUMBERS_DST)
        return text.translate(translations)

    def unicodes_replacement(self, text: str) -> str:
        """Replaces certain Unicode characters with normalized equivalents.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.unicodes_replacement('ﷲ')
            'الله'
            >>> normalizer.unicodes_replacement('﷼')
            'ریال'
            >>> normalizer.unicodes_replacement('')
            ''

        Args:
            text: The text to replace Unicode characters in.

        Returns:
            The text with normalized Unicode characters.
        """
        for old, new in UNICODE_REPLACEMENTS:
            text = text.replace(old, new)
        return text

    def seperate_mi(self, text: str) -> str:
        """Separates the 'mi' prefix in verbs.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.seperate_mi('نمیدانم چه میگفت')
            'نمی‌دانم چه می‌گفت'
            >>> normalizer.seperate_mi('میز')
            'میز'
            >>> normalizer.seperate_mi('')
            ''

        Args:
            text: The text to separate 'mi' in.

        Returns:
            The text with 'mi' separated.
        """
        def replace_match(match):
            m = match.group(0)
            r = re.sub(r"^(ن?می)", r"\1‌", m)
            if self._verbs and r in self._verbs:
                return r
            return m

        return re.sub(r"\bن?می[آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+", replace_match, text)

    def token_spacing(self, tokens: list[str]) -> list[str]:
        """Merges tokens that should be joined.

        Examples:
            >>> normalizer = Normalizer()
            >>> normalizer.token_spacing(['کتاب', 'ها'])
            ['کتاب‌ها']
            >>> normalizer.token_spacing(['او', 'می', 'رود'])
            ['او', 'می‌رود']
            >>> normalizer.token_spacing(['ماه', 'می', 'سال', 'جدید'])
            ['ماه', 'می', 'سال', 'جدید']
            >>> normalizer.token_spacing(['اخلال', 'گر'])
            ['اخلال‌گر']
            >>> normalizer.token_spacing(['زمین', 'لرزه', 'ای'])
            ['زمین‌لرزه‌ای']
            >>> normalizer.token_spacing([])
            []

        Args:
            tokens: The tokens to process.

        Returns:
            A list of processed tokens.
        """
        result: list[str] = []
        for t, token in enumerate(tokens):
            joined = False

            if result:
                token_pair = result[-1] + "‌" + token
                if self._words and (
                    (self._verbs and token_pair in self._verbs)
                    or (token_pair in self._words and self._words[token_pair][0] > 0)
                ):
                    joined = True

                    if (
                        t < len(tokens) - 1
                        and self._verbs
                        and token + "_" + tokens[t + 1] in self._verbs
                    ):
                        joined = False

                elif self._words and token in SUFFIXES and result[-1] in self._words:
                    joined = True

            if joined:
                result[-1] = token_pair
            else:
                result.append(token)

        return result
