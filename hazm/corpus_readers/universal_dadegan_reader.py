"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ [PerUDT](https://github.com/phsfr/UD_Persian-PerDT) است.
PerUDT حاوی تعداد قابل‌توجهی جملۀ برچسب‌خورده با اطلاعات نحوی و ساخت‌واژی است.
"""
import sys
from pathlib import Path
from typing import Iterator

from hazm.corpus_readers import DadeganReader


def conllu2conll(conllu_path: str) -> str :
    """یک فایل conllu را می‌گیرد و بعد از تبدیل به فرمت قدیمی conll آن را به صورت یک رشتهٔ متنی برمی‌گرداند."""
    reader1 = Path(conllu_path).open(encoding="utf8")

    delex = False
    if len(sys.argv) > 3 and sys.argv[3] == "delex":
        delex = True

    line1 = reader1.readline()

    lines = []
    while line1:
        if len(line1.strip()) == 0:
            lines.append(line1)
        else:
            spl = line1.strip().split("\t")
            if len(spl) > 2 and "." not in spl[0] and spl[0].isdigit():
                if ":" in spl[7]:
                    spl[7] = spl[7][:spl[7].rfind(":")]
                if spl[6] == "_" or spl[6] == "-":
                    spl[6] = "-1"
                if delex:
                    spl[1] = "_"
                    spl[2] = "_"
                lines.append("\t".join(spl) + "\n")

        line1 = reader1.readline()
    return "".join(lines)

class UniversalDadeganReader(DadeganReader):
    """این کلاس شامل توابعی برای خواندن پیکرهٔ PerUDT است.

    Args:
        conllu_file: مسیر فایلِ پیکره.

    """
    def __init__(self: DadeganReader, conllu_file: str) -> None:
        self._conll_file = conllu_file
        self._pos_map = lambda tags, _: ",".join(tags)

    def _sentences(self: DadeganReader) -> Iterator[str]:
        """جملات پیکره را به شکل متن خام برمی‌گرداند.

        Yields:
            جملهٔ بعدی.
        """
        text = conllu2conll(self._conll_file)

        # refine text
        text = text.replace("‌‌", "‌").replace("\t‌", "\t").replace("‌\t", "\t").replace("\t ", "\t").replace(" \t", "\t").replace(
            "\r", "").replace("\u2029", "‌")

        for item in text.replace(" ", "_").split("\n\n"):
            if item.strip():
                yield item

