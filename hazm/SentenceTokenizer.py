# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای استخراج جملاتِ متن است. 

برای استخراج کلمات از تابع [WordTokenizer()][hazm.WordTokenizer] استفاده کنید.
"""

from __future__ import unicode_literals
import re
from nltk.tokenize.api import TokenizerI


class SentenceTokenizer(TokenizerI):
    """این کلاس شامل توابعی برای استخراج جملاتِ متن است."""

    def __init__(self):
        self.pattern = re.compile(r"([!\.\?⸮؟]+)[ \n]+")

    def tokenize(self, text):
        """متن ورودی را به جملات سازندهٔ آن می‌شِکند.

        Examples:
                >>> tokenizer = SentenceTokenizer()
                >>> tokenizer.tokenize('جدا کردن ساده است. تقریبا البته!')
                ['جدا کردن ساده است.', 'تقریبا البته!']

        Args:
                text (str): متنی که باید جملات آن استخراج شود.

        Returns:
                (List[str]): فهرست جملات استخراج‌شده.
        """
        text = self.pattern.sub(r"\1\n\n", text)
        return [
            sentence.replace("\n", " ").strip()
            for sentence in text.split("\n\n")
            if sentence.strip()
        ]
