# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ ویکی‌پدیا است. 

[پیکرهٔ ویکی‌پدیا](http://download.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2) پیکرهٔ
عظیمی مشتمل بر تمام مقالات ویکی‌پدیای فارسی است که هر دوماه یکبار بروزرسانی
می‌شود. برای کسب اطلاعات بیشتر دربارهٔ این پیکره می‌توانید به [صفحهٔ اصلی
آن](https://dumps.wikimedia.org/backup-index.html) مراجعه کنید.
"""

from __future__ import unicode_literals, print_function
import os, re, subprocess


class WikipediaReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ ویکی‌پدیا است.

    Args:
            fawiki_dump (str): مسیر فولدر حاوی فایل‌های پیکره.
            n_jobs (int, optional): تعداد هسته‌های پردازنده برای پردازش موازی.
    """

    def __init__(self, fawiki_dump, n_jobs=2):
        self.fawiki_dump = fawiki_dump
        self.wiki_extractor = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "WikiExtractor.py"
        )
        self.n_jobs = n_jobs

    def docs(self):
        """مقالات را برمی‌گرداند.

        هر مقاله، شی‌ای متشکل از چند پارامتر است:

        - شناسه (id)،
        - عنوان (title)،
        - متن (text)،
        - نسخهٔ وب (date)،
        - آدرس صفحه (url).

        Examples:
                >>> wikipedia = WikipediaReader('corpora/wikipedia.csv')
                >>> next(wikipedia.docs())['id']

        Yields:
                (Dict): مقالهٔ بعدی.
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
                id, url, title = doc_pattern.match(doc[0]).groups()
                html = "\n".join(doc[1:-1])

                yield {"id": id, "url": url, "title": title, "html": html, "text": html}
                doc = []

    def texts(self):
        """فقط متن مقالات را برمی‌گرداند.

        این تابع صرفاً برای راحتی بیشتر تهیه شده وگرنه با همان تابع
        ‍[docs()][hazm.WikipediaReader.WikipediaReader.docs] و دریافت مقدار
        پراپرتی `text` نیز می‌توانید همین کار را انجام دهید.

        Examples:
                >>> wikipedia = WikipediaReader('corpora/wikipedia.csv')
                >>> next(wikipedia.texts())[:30]

        Yields:
                (str): متنِ مقالهٔ بعدی.
        """
        for doc in self.docs():
            yield doc["text"]
