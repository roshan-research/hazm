"""این ماژول شامل کلاس‌ها و توابعی برای استخراج جملاتِ متن است.

برای استخراج کلمات از تابع [WordTokenizer()][hazm.WordTokenizer] استفاده کنید.

"""


import re
from typing import List

from nltk.tokenize.api import TokenizerI


class SentenceTokenizer(TokenizerI):
    """این کلاس شامل توابعی برای استخراج جملاتِ متن است."""

    def __init__(self: "SentenceTokenizer") -> None:
        self.pattern = re.compile(r"([!.?⸮؟]+)[ \n]+")

    def tokenize(self: "SentenceTokenizer", text: str) -> List[str]:
        """متن ورودی را به جملات سازندهٔ آن می‌شِکند.

        Examples:
            >>> tokenizer = SentenceTokenizer()
            >>> tokenizer.tokenize('جدا کردن ساده است. تقریبا البته!')
            ['جدا کردن ساده است.', 'تقریبا البته!']

        Args:
            text: متنی که باید جملات آن استخراج شود.

        Returns:
            فهرست جملات استخراج‌شده.

        """
        text = self.pattern.sub(r"\1\n\n", text)
        return [
            sentence.replace("\n", " ").strip()
            for sentence in text.split("\n\n")
            if sentence.strip()
        ]
