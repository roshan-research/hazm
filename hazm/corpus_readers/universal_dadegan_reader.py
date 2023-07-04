
from typing import Iterator
from hazm import DadeganReader

class UniversalDadeganReader(DadeganReader):
    """این کلاس شامل توابعی برای خواندن پیکرهٔ PerDT است.

    Args:
        conllu_file: مسیر فایلِ پیکره.

    """
    def __init__(self: DadeganReader, conllu_file: str) -> None:
        self._conll_file = conllu_file
        self._pos_map = lambda tags: ','.join(tags)
    
    def _sentences(self: DadeganReader) -> Iterator[str]:
        """جملات پیکره را به شکل متن خام برمی‌گرداند.

        Yields:
            (str): جملهٔ بعدی.
        """