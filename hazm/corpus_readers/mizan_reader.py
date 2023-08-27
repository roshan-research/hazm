"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ میزان است.

[پیکرهٔ میزان](https://github.com/omidkashefi/Mizan/) حاوی بیش از ۱ میلیون جمله از متون انگلیسی (اغلب در حوزهٔ ادبیات کلاسیک) و ترجمهٔ این جملات به فارسی که توسط دبیرخانهٔ شورای عالی اطلاع‌رسانی تهیه شده است..

"""
from pathlib import Path
from typing import Iterator
from typing import Tuple

from hazm import get_lines


class MizanReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ میزان است.

    Args:
        corpus_folder: مسیر فولدر حاوی فایل‌های پیکرهٔ میزان.
    """
    def __init__(self: "MizanReader", corpus_folder: str) -> None:
        self.corpus_folder = Path(corpus_folder)
        self.en_file_path = self.corpus_folder / "mizan_en.txt"
        self.fa_file_path = self.corpus_folder / "mizan_fa.txt"


    def english_sentences(self: "MizanReader") -> Iterator[str]:
        """جملات انگلیسی را یک‌به‌یک برمی‌گرداند.

        Yields:
            جملهٔ انگلیسی بعدی.
        """
        return get_lines(self.en_file_path, True)

    def persian_sentences(self: "MizanReader") -> Iterator[str]:
        """جملات فارسی را یک‌به‌یک برمی‌گرداند.

        Yields:
            جملهٔ فارسی بعدی.
        """
        return get_lines(self.fa_file_path, True)

    def english_persian_sentences(self: "MizanReader") -> Iterator[Tuple[str, str]]:
        """جملات انگلیسی و فارسی را کنار هم در قالب یک زوج `(جملهٔ انگلیسی، جملهٔ فارسی)` یک‌به‌یک برمی‌گرداند..

        Yields:
            زوج جملهٔ انگلیسی-فارسی بعدی.
        """
        yield from zip(self.english_sentences(), self.persian_sentences())
