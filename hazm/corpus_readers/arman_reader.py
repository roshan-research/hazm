"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ آرمان است.

[پیکرهٔ آرمان](https://github.com/HaniehP/PersianNER) یک پیکره برای موجودیت‌های نامدار است که شامل ۲۵۰,۰۱۵ توکنِ برچسب‌خورده در قالب ۷۶۸۲ جمله است که با فرمت IOB ذخیره شده است.
"""

from pathlib import Path
from typing import Iterator
from typing import List
from typing import Tuple


class ArmanReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ آرمان است.

    Args:
        corpus_folder: مسیر فولدرِ حاوی فایل‌های پیکره.
        subset: نوع دیتاست: `test` یا `train`
    """
    def __init__(self: "ArmanReader", corpus_folder: str, subset: str="train") -> None:
        self._corpus_folder = corpus_folder
        self._file_paths = Path(corpus_folder).glob(f"{subset}*.txt")


    def sents(self: "ArmanReader") -> Iterator[List[Tuple[str,str]]]:
        """جملات را یک‌به‌یک در قالب لیستی از `(توکن، برچسب)`ها برمی‌گرداند.

        Examples:
            >>> arman = ArmanReader("arman")
            >>> next(arman.sents())
            [('همین', 'O'), ('فکر', 'O'), ('،', 'O'), ('این', 'O'), ('احساس', 'O'), ('را', 'O'), ('به', 'O'), ('من', 'O'), ('می‌داد', 'O'), ('که', 'O'), ('آزاد', 'O'), ('هستم', 'O'), ('.', 'O')]

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
                        token, label = line.split(" ")
                        sentence.append((token, label))
                    elif sentence:
                        yield sentence
                        sentence = []
                if sentence:
                    yield sentence
