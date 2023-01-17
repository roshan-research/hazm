# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای تجزیه توکن به دو توکن کوچکتر است.
"""

from __future__ import unicode_literals
from .Lemmatizer import Lemmatizer


class TokenSplitter:
    """این کلاس شامل توابعی برای تجزیه توکن به دو توکن کوچکتر است."""

    def __init__(self):
        self.lemmatizer = Lemmatizer()
        self.lemmatize = self.lemmatizer.lemmatize
        self.words = self.lemmatizer.words

    def split_token_words(self, token):
        """توکنِ ورودی را به دو توکن کوچکتر تجزیه می‌کند.

        اگر توکن به بیش از یک روش قابل تجزیه باشد همهٔ حالت‌های ممکن را
        برمی‌گرداند؛ مثلاً «داستان‌سرا» هم می‌توان به `['داستان', 'سرا']` تجزیه
        شود و هم می‌تواند به `['داستان‌سرا',]` شکسته شود؛ پس هر دو را
        برمی‌گرداند: `[('داستان', 'سرا'), ('داستان‌سرا',)]`.

        Examples:
                >>> splitter = TokenSplitter()
                >>> splitter.split_token_words('صداوسیماجمهوری')
                [('صداوسیما', 'جمهوری')]
                >>> splitter.split_token_words('صداو')
                [('صد', 'او'), ('صدا', 'و')]
                >>> splitter.split_token_words('شهرموشها')
                [('شهر', 'موشها')]
                >>> splitter.split_token_words('داستان‌سرا')
                [('داستان', 'سرا'), ('داستان‌سرا',)]
                >>> splitter.split_token_words('دستان‌سرا')
                [('دستان', 'سرا')]

        Args:
                token (str): توکنی که باید پردازش شود.

        Returns:
                ([List[Tuple[str,str]]]): <dir-rtl>لیستی از `[(توکن, توکن), (توکن, توکن), …]`ها.</dir-rtl>
        """

        candidates = []
        if "‌" in token:
            candidates.append(tuple(token.split("‌")))

        splits = [
            (token[:s], token[s:])
            for s in range(1, len(token))
            if token[s - 1] != "‌" and token[s] != "‌"
        ] + [(token,)]
        candidates.extend(
            list(
                filter(
                    lambda tokens: set(map(self.lemmatize, tokens)).issubset(
                        self.words
                    ),
                    splits,
                )
            )
        )

        return candidates
