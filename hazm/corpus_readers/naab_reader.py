"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ ناب است.

[پیکرهٔ ناب](https://huggingface.co/datasets/SLPL/naab/) متشکل از ۱۳۰ گیگابایت متن تمیزشدهٔ فارسی متشکل از ۲۵۰ میلیون پاراگراف و ۱۵ میلیارد کلمه است.

"""
import os
from pathlib import Path
from typing import Iterator


class NaabReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ ناب است.

    Args:
        corpus_folder: مسیر فولدر حاوی فایل‌های پیکره.
    """

    def __init__(self: "NaabReader", corpus_folder: str) -> None:
        self.folder_path = corpus_folder

    def sents(self: "NaabReader") -> Iterator[str]:
        """جملات پیکره را یک‌به‌یک برمی‌گرداند.

        Examples:
            >>> naab = NaabReader("naab")
            >>> next(naab.sents())
            این وبلاگ زیر نظر وب‌های زیر به کار خود ادامه می‌دهد


        Yields:
           جملهٔ بعدی.
        """
        for root, _, files in os.walk(self.folder_path):
            for file_name in files:
                if file_name.endswith(".txt"):
                    file_path = Path(root) / file_name
                    with Path(file_path).open("r", encoding="utf-8") as file:
                        yield from (line.strip() for line in file)
