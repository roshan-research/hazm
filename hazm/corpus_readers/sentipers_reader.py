"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ سِنتی‌پِرِس است.

سِنتی‌پرس شامل مجموعه‌ای از متون فارسی با برچسب‌های معنایی است.

"""


import itertools
import os
import sys
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterator
from xml.dom import minidom


class SentiPersReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ سِنتی‌پِرِس است.

    Args:
        root: مسیر فولدر حاوی فایل‌های پیکره

    """

    def __init__(self: "SentiPersReader", root: str) -> None:
        self._root = root

    def docs(self: "SentiPersReader") -> Iterator[Dict[str, Any]]:
        """متن‌های فارسی را در قالب یک برمی‌گرداند.

        هر متن شامل این فیلدهاست:

        - عنوان (Title)
        - نوع (Type)
        - نظرات (comments)

        فیلد `comments `خودش شامل این فیلدهاست:

        - شناسه (id)
        - نوع (type)
        - نویسنده (author)
        - ارزش (value)
        - جملات (sentences)

        Yields:
            متن بعدی.

        """

        def element_sentences(element: str) -> Iterator[Dict]:
            for sentence in element.getElementsByTagName("Sentence"):
                yield {
                    "text": sentence.childNodes[0].data,
                    "id": sentence.getAttribute("ID"),
                    "value": (
                        int(sentence.getAttribute("Value"))
                        if comment.getAttribute("Value")
                        else None
                    ),
                }

        for root, _dirs, files in os.walk(self._root):
            for filename in sorted(files):
                try:
                    elements = minidom.parse(os.path.join(root, filename)) # noqa: PTH118

                    product = elements.getElementsByTagName("Product")[0]
                    doc = {
                        "Title": product.getAttribute("Title"),
                        "Type": product.getAttribute("Type"),
                        "comments": [],
                    }

                    for child in product.childNodes:
                        if child.nodeName in {
                            "Voters",
                            "Performance",
                            "Capability",
                            "Production_Quality",
                            "Ergonomics",
                            "Purchase_Value",
                        }:
                            value = child.getAttribute("Value")
                            doc[child.nodeName] = (
                                float(value) if "." in value else int(value)
                            )

                    for comment in itertools.chain(
                        elements.getElementsByTagName("Opinion"),
                        elements.getElementsByTagName("Criticism"),
                    ):
                        doc["comments"].append(
                            {
                                "id": comment.getAttribute("ID"),
                                "type": comment.nodeName,
                                "author": comment.getAttribute("Holder").strip(),
                                "value": (
                                    int(comment.getAttribute("Value"))
                                    if comment.getAttribute("Value")
                                    else None
                                ),
                                "sentences": list(element_sentences(comment)),
                            },
                        )

                    # todo: Accessories, Features, Review, Advantages, Tags, Keywords, Index

                    yield doc

                except Exception as e:
                    print("error in reading", filename, e, file=sys.stderr)

    def comments(self: "SentiPersReader") -> Iterator[str]:
        """نظرات مربوط به متن را برمی‌گرداند.

        Examples:
            >>> sentipers = SentiPersReader(root='sentipers')
            >>> next(sentipers.comments())[0][1]
            'بيشتر مناسب است براي کساني که به دنبال تنوع هستند و در همه چيز نو گرايي دارند .'

        Yields:
            نظر بعدی.

        """
        for doc in self.docs():
            yield [
                [sentence["text"] for sentence in text]
                for text in [comment["sentences"] for comment in doc["comments"]]
            ]
