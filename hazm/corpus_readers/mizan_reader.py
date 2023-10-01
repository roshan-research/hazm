"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ میزان است.

[پیکرهٔ میزان](https://github.com/omidkashefi/Mizan/) حاوی بیش از ۱ میلیون جمله از متون انگلیسی (اغلب در حوزهٔ ادبیات کلاسیک) و ترجمهٔ این جملات به فارسی که توسط دبیرخانهٔ شورای عالی اطلاع‌رسانی تهیه شده است..

"""
from pathlib import Path
from typing import Iterator
from typing import Tuple


class MizanReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ میزان است.

    Args:
        corpus_folder: مسیر فولدر حاوی فایل‌های پیکرهٔ میزان.
    """
    def __init__(self: "MizanReader", corpus_folder: str) -> None:
        self._corpus_folder = Path(corpus_folder)
        self._en_file_path = self._corpus_folder / "mizan_en.txt"
        self._fa_file_path = self._corpus_folder / "mizan_fa.txt"


    def english_sentences(self: "MizanReader") -> Iterator[str]:
        """جملات انگلیسی را یک‌به‌یک برمی‌گرداند.

        Examples:
            >>> mizan = MizanReader("mizan")
            >>> next(mizan.english_sentences())
            The story which follows was first written out in Paris during the Peace Conference

        Yields:
            جملهٔ انگلیسی بعدی.
        """
        with Path(self._en_file_path).open("r", encoding="utf-8") as file:
            for line in file:
                    yield line.strip()


    def persian_sentences(self: "MizanReader") -> Iterator[str]:
        """جملات فارسی را یک‌به‌یک برمی‌گرداند.

        Examples:
            >>> mizan = MizanReader("mizan")
            >>> next(mizan.persian_sentences())
            داستانی که از نظر شما می‌گذرد، ابتدا ضمن کنفرانس صلح پاریس از روی یادداشت‌هائی که به طور روزانه در حال خدمت در صف برداشته شده بودند

        Yields:
            جملهٔ فارسی بعدی.
        """
        with Path(self._fa_file_path).open("r", encoding="utf-8") as file:
            for line in file:
                    yield line.strip()

    def english_persian_sentences(self: "MizanReader") -> Iterator[Tuple[str, str]]:
        """جملات انگلیسی و فارسی را کنار هم در قالب یک زوج `(جملهٔ انگلیسی، جملهٔ فارسی)` یک‌به‌یک برمی‌گرداند.

        Examples:
            >>> mizan = MizanReader("mizan")
            >>> next(mizan.english_persian_sentences())
            ("The story which follows was first written out in Paris during the Peace Conference", "داستانی که از نظر شما می\u200cگذرد، ابتدا ضمن کنفرانس صلح پاریس از روی یادداشت\u200cهائی که به طور روزانه در حال خدمت در صف برداشته شده بودند")

        Yields:
            جملهٔ بعدی در قالب یک زوج `(جملهٔ انگلیسی، جملهٔ فارسی)`.
        """
        yield from zip(self.english_sentences(), self.persian_sentences())
