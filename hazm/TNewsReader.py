# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ تی‌نیوز است.
"""

from __future__ import print_function
import os
import sys
import re
from xml.dom import minidom


class TNewsReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ تی‌نیوز است.

    Args:
        root (str): مسیر فولدر حاوی فایل‌های پیکره.
    """

    def __init__(self, root):
        self._root = root
        self.cleaner = re.compile(r"<[^<>]+>")

    def docs(self):
        """خبرها را در قالب یک `iterator` برمی‌گرداند.

        هر خبر، شی‌ای متشکل از چند پارامتر است:

        - شناسه (id)،
        - عنوان (title)،
        - پیش از عنوان (pre-title)،
        - پس از عنوان (post-title)،
        - متن (text)،
        - خلاصه (brief)،
        - آدرس (url)،
        - موضوع (category)،
        - تاریخ و زمان انتشار (datetime).

        Examples:
                        >>> tnews = TNewsReader(root='corpora/tnews')
                        >>> next(tnews.docs())['id']
                        '14092303482300013653'

        Yields:
            (Dict): خبر بعدی.
        """

        def get_text(element):
            raw_html = element.childNodes[0].data if element.childNodes else ""
            cleaned_text = re.sub(self.cleaner, "", raw_html)
            return cleaned_text

        for root, dirs, files in os.walk(self._root):
            for name in sorted(files):
                try:
                    content = open(os.path.join(root, name)).read()

                    # fix xml formating issue
                    content = (
                        re.sub(r"[]", "", content).replace(
                            "</TNews>", ""
                        )
                        + "</TNews>"
                    )

                    elements = minidom.parseString(content)
                    for element in elements.getElementsByTagName("NEWS"):
                        doc = {}
                        doc["id"] = get_text(element.getElementsByTagName("NEWSID")[0])
                        doc["url"] = get_text(element.getElementsByTagName("URL")[0])
                        doc["datetime"] = get_text(
                            element.getElementsByTagName("UTCDATE")[0]
                        )
                        doc["category"] = get_text(
                            element.getElementsByTagName("CATEGORY")[0]
                        )
                        doc["pre-title"] = get_text(
                            element.getElementsByTagName("PRETITLE")[0]
                        )
                        doc["title"] = get_text(
                            element.getElementsByTagName("TITLE")[0]
                        )
                        doc["post-title"] = get_text(
                            element.getElementsByTagName("POSTTITLE")[0]
                        )
                        doc["brief"] = get_text(
                            element.getElementsByTagName("BRIEF")[0]
                        )
                        doc["text"] = get_text(
                            element.getElementsByTagName("DESCRIPTION")[0]
                        )
                        yield doc

                except Exception as e:
                    print("error in reading", name, e, file=sys.stderr)

    def texts(self):
        """فقط متن خبرها را برمی‌گرداند.

        این تابع صرفاً برای راحتی بیشتر تهیه شده وگرنه با همان تابع
        ‍[docs()][hazm.TNewsReader.TNewsReader.docs] و دریافت مقدار پراپرتی
        `text` نیز می‌توانید همین کار را انجام دهید.

        Examples:
            >>> tnews = TNewsReader(root='corpora/tnews')
            >>> next(tnews.texts())
            ''

        Yields:
            (str): متن خبر بعدی.
        """
        for doc in self.docs():
            yield doc["text"]
