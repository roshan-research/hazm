"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ FAspell است.

پیکرهٔ [FAspell](https://lindat.mff.cuni.cz/repository/xmlui/handle/11372/LRT-1547) حاوی ۵۰۶۳ غلط املایی فارسی است.
این پیکره همچنین ۸۰۱ تشخیص اشتباه سیستم‌های OCR را نیز در بر دارد.

"""
from pathlib import Path
from typing import Iterator
from typing import Tuple


class FaSpellReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ FAspell است.


    Args:
        corpus_folder: مسییر فولدر حاوی فایل‌های پیکره.

    """

    def __init__(self: "FaSpellReader", corpus_folder: str) -> None:
        self._corpus_folder = Path(corpus_folder)
        self._main_file_path = self._corpus_folder / "faspell_main.txt"
        self._ocr_file_path = self._corpus_folder / "faspell_ocr.txt"



    def main_entries(self: "FaSpellReader") -> Iterator[Tuple[str, str, int]]:
        """کلمات اشتباه و معادل درست آن‌ها را به همراه دسته‌بندی غلط در قالب یک تاپل `(شکل غلط کلمه، شکل صحیح کلمه، دسته‌بندی غلط)`، یک به یک برمی‌گرداند.

        Examples:
            >>> faspell = FaSpellReader(corpus_folder='faspell')
            >>> next(faspell.main_entries())
            ("آاهي","آگاهی",1)


        Yields:
            مدخل بعدی.

        """
        with Path(self._main_file_path).open("r", encoding="utf-8") as file:
            next(file) # skip the first line (header line)
            for line in file:
                parts = line.strip().split("\t")
                misspelt, corrected, error_category = parts
                yield (misspelt, corrected, int(error_category))

    def ocr_entries(self: "FaSpellReader") -> Iterator[Tuple[str, str]]:
        """کلمات اشتباه ocr شده و معادل درست آن‌ها را در قالب یک تاپل `(شکل غلط کلمه، شکل صحیح کلمه)`، یک به یک برمی‌گرداند.


        Examples:
            >>> faspell = FaSpellReader(corpus_folder='faspell')
            >>> next(faspell.ocr_entries())
            ("آمدیم","آ!دبم")


        Yields:
            مدخل بعدی.

        """
        with Path(self._ocr_file_path).open("r", encoding="utf-8") as file:
            next(file) # skip the first line (header line)
            for line in file:
                parts = line.strip().split("\t")
                misspelt, corrected = parts
                yield (misspelt, corrected)
