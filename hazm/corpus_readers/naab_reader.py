"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ ناب است.

[پیکرهٔ ناب](https://huggingface.co/datasets/SLPL/naab/) متشکل از ۱۳۰ گیگابایت متن تمیزشدهٔ فارسی متشکل از ۲۵۰ میلیون پاراگراف و ۱۵ میلیارد کلمه است.

"""
from pathlib import Path
from typing import Iterator


class NaabReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ ناب است.

    Args:
        corpus_folder: مسیر فولدر حاوی فایل‌های پیکره.
        subset: نوع دیتاست: `test` یا `train`
    """

    def __init__(self: "NaabReader", corpus_folder: str, subset: str="train") -> None:
        self._file_paths=Path(corpus_folder).glob(f"{subset}*.txt")

    def sents(self: "NaabReader") -> Iterator[str]:
        """جملات پیکره را یک‌به‌یک برمی‌گرداند.

        Examples:
            >>> naab = NaabReader("naab", "test")
            >>> next(naab.sents())
            این وبلاگ زیر نظر وب‌های زیر به کار خود ادامه می‌دهد

        Yields:
           جملهٔ بعدی.
        """
        for file_path in self._file_paths:
                with Path(file_path).open("r", encoding="utf-8") as file:
                    yield from (line.strip() for line in file)
