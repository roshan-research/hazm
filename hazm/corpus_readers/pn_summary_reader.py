"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ pn-summary است.

پیکرهٔ [pn-summary](https://github.com/hooshvare/pn-summary) با هدف کمک به سیستم‌های یادگیری عمیق و ساخت مدل‌های بهتر برای خلاصه‌سازی دقیق‌تر متن‌های فارسی تهیه شده است. این پیکره شامل ۹۳,۲۰۷ متن خبری تمیزشده است که از ۶ خبرگزاری فارسی و از میان حدوداً ۲۰۰ هزار خبر استخراج شده است.
"""
import csv
from pathlib import Path
from typing import Iterator
from typing import List
from typing import Tuple


class PnSummaryReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ pn-summary است.

    Args:
        corpus_folder: مسیر فولدر حاوی فایل‌های پیکره.
        subset: نوع دیتاست: `test` یا `train` یا `dev`
    """

    def __init__(self: "PnSummaryReader", corpus_folder: str, subset: str="train") -> None:
        self._file_paths=Path(corpus_folder).glob(f"{subset}*.csv")

    def docs(self: "PnSummaryReader") -> Iterator[Tuple[str, str, str, str, str, List[str], str, str]]:
        """خبرها را یک‌به‌یک برمی‌گرداند.

        Examples:
            >>> pn_summary = PnSummaryReader("pn-summary", "test")
            >>> next(pn_summary.docs())
            (
                'ff49386698b87be4fc3943bd3cf88987157e1d47',
                'کاهش ۵۸ درصدی مصرف نفت کوره منطقه سبزوار',
                'مدیر شرکت ملی پخش فرآورده‌های نفتی منطقه سبزوار به خبرنگار شانا، گفت...,
                'مصرف نفت کوره منطقه سبزوار در بهار امسال، نسبت به مدت مشابه پارسال، ۵۸ درصد کاهش یافت.',
                'Oil-Energy',
                ['پالایش و پخش'],
                'Shana',
                'https://www.shana.ir/news/243726/%DA%A9%D8%A7%D9%87%D8...'
            )

        Yields:
           خبر بعدی در قالب `(شناسه, عنوان, متن خبر ,خلاصهٔ خبر, موضوع خبر به انگلیسی, [موضوع ۱ به فارسی، موضوع ۲ به فارسی، ...], منبع, لینک)`
        """
        for file_path in self._file_paths:
                with Path(file_path).open("r", encoding="utf-8") as file:
                    reader = csv.reader(file, delimiter="\t")
                    next(reader)  # Skip the header row

                    for row in reader:
                        _id, title, article, summary, category, categories, network, link = (field.strip() for field in row)
                        categories = categories.split("+")
                        yield (_id, title, article, summary, category, categories, network, link)
