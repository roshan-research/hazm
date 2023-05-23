"""این ماژول شامل کلاس‌ها و توابعی برای ریشه‌یابی کلمات است.

فرق بین [Lemmatizer](./lemmatizer.md) و [Stemmer](./stemmer.md) این است که
اِستمر درکی از معنای کلمه ندارد و صرفاً براساس حذف برخی از پسوندهای ساده تلاش
می‌کند ریشهٔ کلمه را بیابد؛ بنابراین ممکن است در ریشه‌یابیِ برخی از کلمات نتایج
نادرستی ارائه دهد؛ اما لماتایزر براساس لیستی از کلمات مرجع به همراه ریشهٔ آن
این
کار را انجام می‌دهد و نتایج دقیق‌تری ارائه می‌دهد. البته هزینهٔ این دقت، سرعتِ
کمتر در ریشه‌یابی است.

"""


from nltk.stem.api import StemmerI


class Stemmer(StemmerI):      
    """این کلاس شامل توابعی برای ریشه‌یابی کلمات است."""

    def __init__(self: "Stemmer") -> None:
        self.ends = [
            "ات",
            "ان",
            "ترین",
            "تر",
            "م",
            "ت",
            "ش",
            "یی",
            "ی",
            "ها",
            "ٔ",
            "‌ا",
            "‌",
        ]

    def stem(self: "Stemmer", word: str) -> str:
        """ریشهٔ کلمه را پیدا می‌کند.

        Examples:
            >>> stemmer = Stemmer()
            >>> stemmer.stem('کتابی')
            'کتاب'
            >>> stemmer.stem('کتاب‌ها')
            'کتاب'
            >>> stemmer.stem('کتاب‌هایی')
            'کتاب'
            >>> stemmer.stem('کتابهایشان')
            'کتاب'
            >>> stemmer.stem('اندیشه‌اش')
            'اندیشه'
            >>> stemmer.stem('خانۀ')
            'خانه'
            >>> stemmer.stem('محبوب‌ترین‌ها')
            'محبوب'

        Args:
            word: کلمه‌ای که باید ریشهٔ آن پیدا شود.

        Returns:
            ریشهٔ کلمه.

        """
        if word.endswith("ۀ"):
            word = word[:-1] + "ه"

        else:
            iteration = len(self.ends)
            while iteration:
                for end in self.ends:
                    if word.endswith(end):
                        word = word[: -len(end)]
                iteration -= 1

        return word
