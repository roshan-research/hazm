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

            separate_emoji (bool, optional): اگر `True` باشد اموجی‌ها را با یک فاصله از هم جدا می‌کند.
            replace_links (bool, optional): اگر `True` باشد لینک‌ها را با کلمهٔ `LINK` جایگزین می‌کند.
            replace_IDs (bool, optional): اگر `True` باشد شناسه‌ها را با کلمهٔ `ID` جایگزین می‌کند.
            replace_emails (bool, optional): اگر `True` باشد آدرس‌های ایمیل را با کلمهٔ `EMAIL‍` جایگزین می‌کند.
            replace_numbers (bool, optional): اگر `True` باشد اعداد اعشاری را با`NUMF` و اعداد صحیح را با` NUM` جایگزین می‌کند. در اعداد غیراعشاری، تعداد ارقام نیز جلوی `NUM` می‌آید.
            replace_hashtags (bool, optional): اگر `True` باشد علامت `#` را با `TAG` جایگزین می‌کند.
    """

    def __init__(self, words_file=default_words, verbs_file=default_verbs, separate_emoji=False, replace_links=False, replace_IDs=False, replace_emails=False, replace_numbers=False, replace_hashtags=False):
        self.separate_emoji = separate_emoji
        self.replace_links = replace_links
        self.replace_IDs = replace_IDs
        self.replace_emails = replace_emails
        self.replace_numbers = replace_numbers
        self.replace_hashtags = replace_hashtags

        self.pattern = re.compile(
            r'([؟!\?]+|\d[\d\.:\/\\]+\d|[:\.،؛»\]\)\}"«\[\(\{])')  # TODO \d
        self.emoji_pattern = re.compile(u"["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F4CC\U0001F4CD"  # other emojis
                                        "]", flags=re.UNICODE)
        self.emoji_repl = r'\g<0> '
        self.id_pattern = re.compile(r'(?<![\w\._])(@[\w_]+)')
        self.id_repl = r' ID '
        self.link_pattern = re.compile(
            r'((https?|ftp):\/\/)?(?<!@)(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})[-\w@:%_\.\+\/~#?=&]*')
        self.link_repl = r' LINK '
        self.email_pattern = re.compile(
            r'[a-zA-Z0-9\._\+-]+@([a-zA-Z0-9-]+\.)+[A-Za-z]{2,}')
        self.email_repl = r' EMAIL '

        # '٫' is the decimal separator and '٬' is the thousands separator
        self.number_int_pattern = re.compile(
            r'\b(?<![\d۰-۹][\.٫٬,])([\d۰-۹]+)(?![\.٫٬,][\d۰-۹])\b')
        self.number_int_repl = lambda m: ' NUM' + str(len(m.group(1))) + ' '
        self.number_float_pattern = re.compile(
            r'\b(?<!\.)([\d۰-۹,٬]+[\.٫٬]{1}[\d۰-۹]+)\b(?!\.)')
        self.number_float_repl = r' NUMF '

        self.hashtag_pattern = re.compile(r'\#([\S]+)')
        # NOTE: python2.7 does not support unicodes with \w

        self.hashtag_repl = lambda m: 'TAG ' + m.group(1).replace('_', ' ')

        self.words = {item[0]: (item[1], item[2])
                      for item in words_list(words_file)}

        with codecs.open(verbs_file, encoding='utf8') as verbs_file:
            self.verbs = list(reversed([verb.strip()
                              for verb in verbs_file if verb]))
            self.bons = set([verb.split('#')[0] for verb in self.verbs])
            self.verbe = set([bon + 'ه' for bon in self.bons] +
                             ['ن' + bon + 'ه' for bon in self.bons])

    def tokenize(self, text):
        """توکن‌های متن را استخراج می‌کند.

        Examples:
                >>> tokenizer = WordTokenizer()
                >>> tokenizer.tokenize('این جمله (خیلی) پیچیده نیست!!!')
                ['این', 'جمله', '(', 'خیلی', ')', 'پیچیده', 'نیست', '!!!']

                >>> tokenizer.tokenize('نسخه 0.5 در ساعت 22:00 تهران،1396.')
                ['نسخه', '0.5', 'در', 'ساعت', '22:00', 'تهران', '،', '1396', '.']

                >>> tokenizer = WordTokenizer()
                >>> print(' '.join(tokenizer.tokenize('سلام.')))
                سلام .

                >>> tokenizer = WordTokenizer(replace_links=True)
                >>> print(' '.join(tokenizer.tokenize('در قطر هک شد https://t.co/tZOurPSXzi https://t.co/vtJtwsRebP')))
                در قطر هک شد LINK LINK

                >>> tokenizer = WordTokenizer(replace_IDs=True, replace_numbers=True)
                >>> print(' '.join(tokenizer.tokenize('زلزله ۴.۸ ریشتری در هجدک کرمان @bourse24ir')))
                زلزله NUMF ریشتری در هجدک کرمان ID

                >>> tokenizer = WordTokenizer(replace_hashtags=True, replace_numbers=True, separate_emoji=True)
                >>> print(' '.join(tokenizer.tokenize('📍عرضه بلوک 17 درصدی #های_وب به قیمت')))
                📍 عرضه بلوک NUM2 درصدی TAG های وب به قیمت

                >>> tokenizer = WordTokenizer(separate_emoji=True)
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

        text = self.pattern.sub(
            r' \1 ', text.replace('\n', ' ').replace('\t', ' '))

        tokens = [word for word in text.split(' ') if word]
        return tokens
