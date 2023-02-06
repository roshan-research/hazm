# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ پرسیکا است.

[پیکرهٔ پرسیکا](https://www.peykaregan.ir/dataset/%D9%BE%D8%B1%D8%B3%DB%8C%DA%A9%D8%A7-%D9%BE%DB%8C%DA%A9%D8%B1%D9%87-%D9%85%D8%AA%D9%88%D9%86-%D8%AE%D8%A8%D8%B1%DB%8C) حاوی
خبرهای برگرفته از خبرگزاری ایسنا در یازده دستهٔ ورزشی، اقتصادی، فرهنگی، مذهبی،
تاریخی، سیاسی، علمی، اجتماعی، آموزشی، حقوق قضایی و بهداشت است. روی این داده‌ها
پیش‌پردازش‌هایی صورت شده و آمادهٔ استفاده در کاربردهای مختلف پردازش زبان طبیعی و
داده‌کاوی است.
"""

from __future__ import print_function
import codecs


class PersicaReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ پرسیکا است.

    Args:
            csv_file (str): مسیر فایلِ پیکره با پسوند csv.
    """

    def __init__(self, csv_file):
        self._csv_file = csv_file

    def docs(self):
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
                >>> persica = PersicaReader('corpora/persica.csv')
                >>> next(persica.docs())['id']
                843656

        Yields:
                (Dict): خبر بعدی.
        """
        lines = []
        for line in codecs.open(self._csv_file, encoding="utf-8-sig"):
            line = line.strip()
            if line:
                if line.endswith(","):
                    lines.append(line[:-1])
                else:
                    lines.append(line)
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

    def texts(self):
        """فقط متن خبرها را برمی‌گرداند.

        این تابع صرفاً برای راحتی بیشتر تهیه شده وگرنه با همان تابع
        ‍[docs()][hazm.PersicaReader.PersicaReader.docs] و دریافت مقدار پراپرتی
        `text` نیز می‌توانید همین کار را انجام دهید.

        Examples:
                >>> persica = PersicaReader('corpora/persica.csv')
                >>> next(persica.texts())
                ''

        Yields:
                (str): متنِ خبر بعدی.
        """
        for doc in self.docs():
            yield doc["text"]
