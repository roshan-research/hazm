"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ ظرفیت نحوی افعال فارسی
است.

پیکرهٔ ظرفیت نحوی افعال فارسی مجموعه‌ای است حاوی اطلاعات مربوط به ظرفیت نحوی
بیش
از ۴۵۰۰ فعل در زبان فارسی. در این فرهنگ، متمم‌های اجباری و اختیاری انواع
فعل‌های
ساده، مرکب، پیشوندی و عبارات فعلی مشخص شده است. فراوانی فعل‌های مرکب در زبان
فارسی، نیاز به فرهنگ ظرفیت فعل را در این زبان دوچندان می‌نماید. چرا که شناخت
فعل‌های مرکب چه از لحاظ انسانی و چه از لحاظ پردازشی کاری دشوار‌تر از شناخت
فعل‌های ساده است و به همین خاطر فراهم آوردن فهرستی از فعل‌های زبان (که شامل
فعل‌های مرکب نیز می‌شود) به همراه ساخت‌های ظرفیتی افعال، کمکی شایان برای کارهای
پردازشی است. از سوی دیگر، بر اساس نظریه وابستگی، ساخت بنیادین جمله را می‌توان
از
روی ساخت ظرفیتی فعل جمله به دست آورد و به همین دلیل بر اهمیت دانستن ساخت‌های
ظرفیتی فعل در متن‌های زبانی افزوده می‌شود.

"""


from collections import namedtuple
from pathlib import Path
from typing import Iterator

Verb = namedtuple(
    "Verb",
    (
        "past_light_verb",
        "present_light_verb",
        "prefix",
        "nonverbal_element",
        "preposition",
        "valency",
    ),
)


class VerbValencyReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ ظرفیت نحوی افعال فارسی است.

    Args:
        valency_file: مسیر فایلِ پیکره.

    """

    def __init__(
        self: "VerbValencyReader", valency_file: str = "valency.txt",
    ) -> None:
        self._valency_file = valency_file

    def verbs(self: "VerbValencyReader") -> Iterator[Verb]:
        """افعال پیکره را برمی‌گرداند.

        Yields:
            فعل بعدی.

        """
        with Path.open(self._valency_file, encoding="utf-8") as valency_file:
            for line in valency_file:
                if "بن ماضی" in line:
                    continue

                line = line.strip().replace("-\t", "\t")
                parts = line.split("\t")
                if len(parts) == 6:
                    yield Verb(*parts)
