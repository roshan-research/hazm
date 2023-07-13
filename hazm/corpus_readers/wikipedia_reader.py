"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ ویکی‌پدیا است.

[پیکرهٔ ویکی‌پدیا](http://download.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2) پیکرهٔ
عظیمی مشتمل بر تمام مقالات ویکی‌پدیای فارسی است که هر دوماه یکبار بروزرسانی
می‌شود. برای کسب اطلاعات بیشتر دربارهٔ این پیکره می‌توانید به [صفحهٔ اصلی
آن](https://dumps.wikimedia.org/backup-index.html) مراجعه کنید.

"""


import os
import re
import subprocess
from pathlib import Path
from typing import Dict
from typing import Iterator


class WikipediaReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ ویکی‌پدیا است.

    Args:
        fawiki_dump: مسیر فولدر حاوی فایل‌های پیکره.
        n_jobs: تعداد هسته‌های پردازنده برای پردازش موازی.

    """

    def __init__(self: "WikipediaReader", fawiki_dump: str, n_jobs: int = 2) -> None:
        self.fawiki_dump = fawiki_dump
        self.wiki_extractor = Path(__file__).parent / "wiki_extractor.py"
        self.n_jobs = n_jobs

    def docs(self: "WikipediaReader") -> Iterator[Dict[str, str]]:
        """مقالات را برمی‌گرداند.

        هر مقاله، شی‌ای متشکل از چند پارامتر است:

        - شناسه (id)،
        - عنوان (title)،
        - متن (text)،
        - نسخهٔ وب (date)،
        - آدرس صفحه (url).

        Examples:
            >>> wikipedia = WikipediaReader('fawiki-latest-pages-articles.xml.bz2')
            >>> next(wikipedia.docs())['id']

        Yields:
            مقالهٔ بعدی.

        """
        proc = subprocess.Popen(
            [
                "python",
                self.wiki_extractor,
                "--no-templates",
                "--processes",
                str(self.n_jobs),
                "--output",
                "-",
                self.fawiki_dump,
            ],
            stdout=subprocess.PIPE,
        )
        doc_pattern = re.compile(r'<doc id="(\d+)" url="([^\"]+)" title="([^\"]+)">')

        doc = []
        for line in iter(proc.stdout.readline, b""):
            line = line.strip().decode("utf8")
            if line:
                doc.append(line)

            if line == "</doc>":
                del doc[1]
                id, url, title = doc_pattern.match(doc[0]).groups()  # noqa: A001
                html = "\n".join(doc[1:-1])

                yield {"id": id, "url": url, "title": title, "html": html, "text": html}
                doc = []

    def texts(self: "WikipediaReader") -> Iterator[str]:
        """فقط متن مقالات را برمی‌گرداند.

        این تابع صرفاً برای راحتی بیشتر تهیه شده وگرنه با همان تابع
        ‍[docs()][hazm.corpus_readers.wikipedia_reader.WikipediaReader.docs] و دریافت مقدار
        پراپرتی `text` نیز می‌توانید همین کار را انجام دهید.

        Examples:
            >>> wikipedia = WikipediaReader('fawiki-latest-pages-articles.xml.bz2')
            >>> next(wikipedia.texts())[:30]

        Yields:
            متنِ مقالهٔ بعدی.

        """
        for doc in self.docs():
            yield doc["text"]
