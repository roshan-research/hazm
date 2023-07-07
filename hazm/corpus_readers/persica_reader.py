"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ پرسیکا است.

[پیکرهٔ پرسیکا](https://www.peykaregan.ir/dataset/%D9%BE%D8%B1%D8%B3%DB%8C%DA%A
9%D8%A7-%D9%BE%DB%8C%DA%A9%D8%B1%D9%87-%D9%85%D8%AA%D9%88%D9%86-
%D8%AE%D8%A8%D8%B1%DB%8C) حاوی
خبرهای برگرفته از خبرگزاری ایسنا در یازده دستهٔ ورزشی، اقتصادی، فرهنگی، مذهبی،
تاریخی، سیاسی، علمی، اجتماعی، آموزشی، حقوق قضایی و بهداشت است. روی این داده‌ها
پیش‌پردازش‌هایی صورت شده و آمادهٔ استفاده در کاربردهای مختلف پردازش زبان طبیعی
و
داده‌کاوی است.

"""
from pathlib import Path
from typing import Dict
from typing import Iterator


class PersicaReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ پرسیکا است.

    Args:
        csv_file: مسیر فایلِ پیکره با پسوند csv.

    """

    def __init__(self: "PersicaReader", csv_file: str) -> None:
        self._csv_file = csv_file

    def docs(self: "PersicaReader") -> Iterator[Dict[str, str]]:
        """خبرها را برمی‌گرداند.

        هر خبر، شی‌ای متشکل از این پارامتر است:

        - شناسه (`id`)
        - عنوان (`title`)
        - متن (`text`)
        - تاریخ (`date`)
        - زمان (`time`)
        - دستهٔ اصلی (`category`)
        - دستهٔ فرعی (`category2`)

        Examples:
            >>> persica = PersicaReader('persica.csv')
            >>> next(persica.docs())['id']
            843656

        Yields:
            خبر بعدی.

        """
        lines = []
        for current_line in Path(self._csv_file).open(encoding="utf-8-sig"):
            current_line = current_line.strip()
            if current_line:
                if current_line.endswith(","):
                    lines.append(current_line[:-1])
                else:
                    lines.append(current_line)
                    yield {
                        "id": int(lines[0]),
                        "title": lines[1],
                        "text": lines[2],
                        "date": lines[3],
                        "time": lines[4],
                        "category": lines[5],
                        "category2": lines[6],
                    }
                    lines = []

    def texts(self: "PersicaReader") -> Iterator[str]:
        """فقط متن خبرها را برمی‌گرداند.

        این تابع صرفاً برای راحتی بیشتر تهیه شده وگرنه با همان تابع
        ‍[docs()][hazm.corpus_readers.persica_reader.PersicaReader.docs] و دریافت مقدار پراپرتی
        `text` نیز می‌توانید همین کار را انجام دهید.

        Examples:
            >>> persica = PersicaReader('persica.csv')
            >>> next(persica.texts()).startswith('وزير علوم در جمع استادان نمونه كشور گفت')
            True

        Yields:
            متنِ خبر بعدی.

        """
        for doc in self.docs():
            yield doc["text"]
