"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ موجودیت‌های نامدار است.

[پیکرهٔ موجودیت‌های نامدار](https://github.com/Text-Mining/Persian-NER/) حاوی ۲۵ میلیون توکنِ برچسب‌خورده از ویکی‌پدیای فارسی در قالب حدود یک میلیون جمله است.
"""

from pathlib import Path
from typing import Iterator
from typing import List
from typing import Tuple


class NerReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ موجودیت‌های نامدار است.

    Args:
        corpus_folder: مسیر فولدرِ حاوی فایل‌های پیکره.
    """
    def __init__(self: "NerReader", corpus_folder: str) -> None:
        self._corpus_folder = corpus_folder
        self._file_paths = Path(corpus_folder).glob("*.txt")


    def sents(self: "NerReader") -> Iterator[List[Tuple[str,str]]]:
        """جملات را یک‌به‌یک در قالب لیستی از `(توکن، برچسب)`ها برمی‌گرداند.

        Examples:
            >>> ner = NerReader("ner")
            >>> next(ner.sents())
            [('ویکی‌پدیای', 'O'), ('انگلیسی', 'O'), ('در', 'B-DAT'), ('تاریخ', 'I-DAT'), ('۱۵', 'I-DAT'), ('ژانویه', 'I-DAT'), ('۲۰۰۱', 'I-DAT'), ('(', 'O'), ('میلادی', 'B-DAT'), (')', 'O'), ('۲۶', 'B-DAT'), ('دی', 'I-DAT'), ('۱۳۷۹', 'I-DAT'), (')', 'O'), ('به', 'O'), ('صورت', 'O'), ('مکملی', 'O'), ('برای', 'O'), ('دانشنامه', 'O'), ('تخصصی', 'O'), ('نوپدیا', 'O'), ('نوشته', 'O'), ('شد', 'O'), ('.', 'O')]

        Yields:
            جملهٔ بعدی در قالب لیستی از `(توکن، برچسب)`ها

        """
        for file_path in self._file_paths:
            with Path(file_path).open("r", encoding="utf-8") as file:
                lines = file.readlines()
                sentence = []
                for line in lines:
                    line = line.strip()
                    if line:
                        token, label = line.split("\t")
                        sentence.append((token, label))
                    elif sentence:
                        yield sentence
                        sentence = []
                if sentence:
                    yield sentence
