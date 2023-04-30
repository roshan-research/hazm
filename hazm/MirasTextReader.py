"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ میراث است.

[پیکرهٔ میراث](https://github.com/miras-tech/MirasText) حاوی ۲,۸۳۵,۴۱۴ خبر از
۲۵۰ خبرگزاری فارسی است.

"""
from typing import Iterator
from typing import Dict


class MirasTextReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ میراث است.

    Args:
        filename: مسیر فایلِ پیکره.

    """

    def __init__(self, filename: str):
        self._filename = filename

    def docs(self) -> Iterator[Dict[str, str]]:
        """خبرها را برمی‌گرداند.

        Yields:
            خبر بعدی.

        """

        for line in open(self._filename, encoding="utf-8"):
            parts = line.split("***")
            # todo: extract link, tags, ...
            yield {"text": parts[0].strip()}

    def texts(self) -> Iterator[str]:
        """فقط متن خبرها را برمی‌گرداند.

        این تابع صرفاً برای راحتی بیشتر تهیه شده وگرنه با تابع
        ‍[docs()][hazm.MirasTextReader.MirasTextReader.docs] و دریافت مقدار
        پراپرتی `text` نیز می‌توانید همین کار را انجام دهید.

        Examples:
            >>> miras_text = MirasTextReader(filename='corpora/MirasText.txt')
            >>> next(miras_text.texts())[:42]  # first 42 characters of fitst text
            'ایرانی‌ها چقدر از اینترنت استفاده می‌کنند؟'

        Yields:
            : متنِ خبر بعدی.

        """
        for doc in self.docs():
            yield doc["text"]
