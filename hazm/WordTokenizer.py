# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای استخراج کلماتِ متن است. 

برای استخراج جملات، از تابع [SentenceTokenizer()][hazm.SentenceTokenizer] استفاده کنید.
"""

from __future__ import unicode_literals
import re
import codecs
from .utils import words_list, default_words, default_verbs
from nltk.tokenize.api import TokenizerI


class WordTokenizer(TokenizerI):
    """این کلاس شامل توابعی برای استخراج کلماتِ متن است.

    Args:
            words_file (str, optional): مسیر فایل حاوی لیست کلمات.
                    هضم به صورت پیش‌فرض فایلی برای این منظور در نظر گرفته است؛ با
                    این حال شما می‌توانید فایل موردنظر خود را معرفی کنید. برای آگاهی از
                    ساختار این فایل به فایل پیش‌فرض مراجعه کنید.

            verbs_file (str, optional): مسیر فایل حاوی افعال.
                    هضم به صورت پیش‌فرض فایلی برای این منظور در نظر گرفته است؛ با
                    این حال شما می‌توانید فایل موردنظر خود را معرفی کنید. برای آگاهی از
                    ساختار این فایل به فایل پیش‌فرض مراجعه کنید.

            join_verb_parts (bool, optional): اگر `True` باشد افعال چندبخشی را با خط زیر به هم می‌چسباند؛ مثلاً «گفته شده است» را به صورت «گفته_شده_است» برمی‌گرداند.
            separate_emoji (bool, optional): اگر `True` باشد اموجی‌ها را با یک فاصله از هم جدا می‌کند.
            replace_links (bool, optional): اگر `True` باشد لینک‌ها را با کلمهٔ `LINK` جایگزین می‌کند.
            replace_IDs (bool, optional): اگر `True` باشد شناسه‌ها را با کلمهٔ `ID` جایگزین می‌کند.
            replace_emails (bool, optional): اگر `True` باشد آدرس‌های ایمیل را با کلمهٔ `EMAIL‍` جایگزین می‌کند.
            replace_numbers (bool, optional): اگر `True` باشد اعداد اعشاری را با`NUMF` و اعداد صحیح را با` NUM` جایگزین می‌کند. در اعداد غیراعشاری، تعداد ارقام نیز جلوی `NUM` می‌آید.
            replace_hashtags (bool, optional): اگر `True` باشد علامت `#` را با `TAG` جایگزین می‌کند.
    """

    def __init__(
        self,
        words_file=default_words,
        verbs_file=default_verbs,
        join_verb_parts=False,
        separate_emoji=False,
        replace_links=False,
        replace_IDs=False,
        replace_emails=False,
        replace_numbers=False,
        replace_hashtags=False,
    ):
        self._join_verb_parts = join_verb_parts
        self.separate_emoji = separate_emoji
        self.replace_links = replace_links
        self.replace_IDs = replace_IDs
        self.replace_emails = replace_emails
        self.replace_numbers = replace_numbers
        self.replace_hashtags = replace_hashtags

        self.pattern = re.compile(
            r'([؟!\?]+|\d[\d\.:\/\\]+\d|[:\.،؛»\]\)\}"«\[\(\{])'
        )  # TODO \d
        self.emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F4CC\U0001F4CD"  # other emojis
            "]",
            flags=re.UNICODE,
        )
        self.emoji_repl = r"\g<0> "
        self.id_pattern = re.compile(r"(?<![\w\._])(@[\w_]+)")
        self.id_repl = r" ID "
        self.link_pattern = re.compile(
            r"((https?|ftp):\/\/)?(?<!@)(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})[-\w@:%_\.\+\/~#?=&]*"
        )
        self.link_repl = r" LINK "
        self.email_pattern = re.compile(
            r"[a-zA-Z0-9\._\+-]+@([a-zA-Z0-9-]+\.)+[A-Za-z]{2,}"
        )
        self.email_repl = r" EMAIL "

        # '٫' is the decimal separator and '٬' is the thousands separator
        self.number_int_pattern = re.compile(
            r"\b(?<![\d۰-۹][\.٫٬,])([\d۰-۹]+)(?![\.٫٬,][\d۰-۹])\b"
        )
        self.number_int_repl = lambda m: " NUM" + str(len(m.group(1))) + " "
        self.number_float_pattern = re.compile(
            r"\b(?<!\.)([\d۰-۹,٬]+[\.٫٬]{1}[\d۰-۹]+)\b(?!\.)"
        )
        self.number_float_repl = r" NUMF "

        self.hashtag_pattern = re.compile(r"\#([\S]+)")
        # NOTE: python2.7 does not support unicodes with \w

        self.hashtag_repl = lambda m: "TAG " + m.group(1).replace("_", " ")

        self.words = {item[0]: (item[1], item[2]) for item in words_list(words_file)}

        if join_verb_parts:
            self.after_verbs = set(
                [
                    "ام",
                    "ای",
                    "است",
                    "ایم",
                    "اید",
                    "اند",
                    "بودم",
                    "بودی",
                    "بود",
                    "بودیم",
                    "بودید",
                    "بودند",
                    "باشم",
                    "باشی",
                    "باشد",
                    "باشیم",
                    "باشید",
                    "باشند",
                    "شده_ام",
                    "شده_ای",
                    "شده_است",
                    "شده_ایم",
                    "شده_اید",
                    "شده_اند",
                    "شده_بودم",
                    "شده_بودی",
                    "شده_بود",
                    "شده_بودیم",
                    "شده_بودید",
                    "شده_بودند",
                    "شده_باشم",
                    "شده_باشی",
                    "شده_باشد",
                    "شده_باشیم",
                    "شده_باشید",
                    "شده_باشند",
                    "نشده_ام",
                    "نشده_ای",
                    "نشده_است",
                    "نشده_ایم",
                    "نشده_اید",
                    "نشده_اند",
                    "نشده_بودم",
                    "نشده_بودی",
                    "نشده_بود",
                    "نشده_بودیم",
                    "نشده_بودید",
                    "نشده_بودند",
                    "نشده_باشم",
                    "نشده_باشی",
                    "نشده_باشد",
                    "نشده_باشیم",
                    "نشده_باشید",
                    "نشده_باشند",
                    "شوم",
                    "شوی",
                    "شود",
                    "شویم",
                    "شوید",
                    "شوند",
                    "شدم",
                    "شدی",
                    "شد",
                    "شدیم",
                    "شدید",
                    "شدند",
                    "نشوم",
                    "نشوی",
                    "نشود",
                    "نشویم",
                    "نشوید",
                    "نشوند",
                    "نشدم",
                    "نشدی",
                    "نشد",
                    "نشدیم",
                    "نشدید",
                    "نشدند",
                    "می‌شوم",
                    "می‌شوی",
                    "می‌شود",
                    "می‌شویم",
                    "می‌شوید",
                    "می‌شوند",
                    "می‌شدم",
                    "می‌شدی",
                    "می‌شد",
                    "می‌شدیم",
                    "می‌شدید",
                    "می‌شدند",
                    "نمی‌شوم",
                    "نمی‌شوی",
                    "نمی‌شود",
                    "نمی‌شویم",
                    "نمی‌شوید",
                    "نمی‌شوند",
                    "نمی‌شدم",
                    "نمی‌شدی",
                    "نمی‌شد",
                    "نمی‌شدیم",
                    "نمی‌شدید",
                    "نمی‌شدند",
                    "خواهم_شد",
                    "خواهی_شد",
                    "خواهد_شد",
                    "خواهیم_شد",
                    "خواهید_شد",
                    "خواهند_شد",
                    "نخواهم_شد",
                    "نخواهی_شد",
                    "نخواهد_شد",
                    "نخواهیم_شد",
                    "نخواهید_شد",
                    "نخواهند_شد",
                ]
            )

            self.before_verbs = set(
                [
                    "خواهم",
                    "خواهی",
                    "خواهد",
                    "خواهیم",
                    "خواهید",
                    "خواهند",
                    "نخواهم",
                    "نخواهی",
                    "نخواهد",
                    "نخواهیم",
                    "نخواهید",
                    "نخواهند",
                ]
            )

            with codecs.open(verbs_file, encoding="utf8") as verbs_file:
                self.verbs = list(
                    reversed([verb.strip() for verb in verbs_file if verb])
                )
                self.bons = set([verb.split("#")[0] for verb in self.verbs])
                self.verbe = set(
                    [bon + "ه" for bon in self.bons]
                    + ["ن" + bon + "ه" for bon in self.bons]
                )

    def tokenize(self, text):
        """توکن‌های متن را استخراج می‌کند.

        Examples:
                >>> tokenizer = WordTokenizer()
                >>> tokenizer.tokenize('این جمله (خیلی) پیچیده نیست!!!')
                ['این', 'جمله', '(', 'خیلی', ')', 'پیچیده', 'نیست', '!!!']

                >>> tokenizer.tokenize('نسخه 0.5 در ساعت 22:00 تهران،1396.')
                ['نسخه', '0.5', 'در', 'ساعت', '22:00', 'تهران', '،', '1396', '.']

                >>> tokenizer = WordTokenizer(join_verb_parts=False)
                >>> print(' '.join(tokenizer.tokenize('سلام.')))
                سلام .

                >>> tokenizer = WordTokenizer(join_verb_parts=False, replace_links=True)
                >>> print(' '.join(tokenizer.tokenize('در قطر هک شد https://t.co/tZOurPSXzi https://t.co/vtJtwsRebP')))
                در قطر هک شد LINK LINK

                >>> tokenizer = WordTokenizer(join_verb_parts=False, replace_IDs=True, replace_numbers=True)
                >>> print(' '.join(tokenizer.tokenize('زلزله ۴.۸ ریشتری در هجدک کرمان @bourse24ir')))
                زلزله NUMF ریشتری در هجدک کرمان ID

                >>> tokenizer = WordTokenizer(join_verb_parts=False, replace_hashtags=True, replace_numbers=True, separate_emoji=True)
                >>> print(' '.join(tokenizer.tokenize('📍عرضه بلوک 17 درصدی #های_وب به قیمت')))
                📍 عرضه بلوک NUM2 درصدی TAG های وب به قیمت

                >>> tokenizer = WordTokenizer(join_verb_parts=False, separate_emoji=True)
                >>> print(' '.join(tokenizer.tokenize('دیگه میخوام ترک تحصیل کنم 😂😂😂')))
                دیگه میخوام ترک تحصیل کنم 😂 😂 😂

        Args:
                text (str): متنی که باید توکن‌های آن استخراج شود.

        Returns:
                (List[str]): لیست توکن‌های استخراج‌شده.
        """

        if self.separate_emoji:
            text = self.emoji_pattern.sub(self.emoji_repl, text)
        if self.replace_emails:
            text = self.email_pattern.sub(self.email_repl, text)
        if self.replace_links:
            text = self.link_pattern.sub(self.link_repl, text)
        if self.replace_IDs:
            text = self.id_pattern.sub(self.id_repl, text)
        if self.replace_hashtags:
            text = self.hashtag_pattern.sub(self.hashtag_repl, text)
        if self.replace_numbers:
            text = self.number_int_pattern.sub(self.number_int_repl, text)
            text = self.number_float_pattern.sub(self.number_float_repl, text)

        text = self.pattern.sub(r" \1 ", text.replace("\n", " ").replace("\t", " "))

        tokens = [word for word in text.split(" ") if word]
        if self._join_verb_parts:
            tokens = self.join_verb_parts(tokens)
        return tokens

    def join_verb_parts(self, tokens):
        """افعال چندبخشی را به هم می‌چسباند.

        Examples:
            >>> tokenizer = WordTokenizer()
            >>> tokenizer.join_verb_parts(['خواهد', 'رفت'])
            ['خواهد_رفت']
            >>> tokenizer.join_verb_parts(['رفته', 'است'])
            ['رفته_است']
            >>> tokenizer.join_verb_parts(['گفته', 'شده', 'است'])
            ['گفته_شده_است']
            >>> tokenizer.join_verb_parts(['گفته', 'خواهد', 'شد'])
            ['گفته_خواهد_شد']
            >>> tokenizer.join_verb_parts(['خسته', 'شدید'])
            ['خسته', 'شدید']
        Args:
            tokens (List[str]): لیست کلمات یک فعل چندبخشی.
        Returns:
            (List[str]): لیست از افعال چندبخشی که در صورت لزوم بخش‌های آن با کاراکتر خط زیر به هم چسبانده_شده_است.
        """

        result = [""]
        for token in reversed(tokens):
            if token in self.before_verbs or (
                result[-1] in self.after_verbs and token in self.verbe
            ):
                result[-1] = token + "_" + result[-1]
            else:
                result.append(token)
        return list(reversed(result[1:]))
