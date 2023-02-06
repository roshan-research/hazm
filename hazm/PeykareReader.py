# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ Peykare است. 

[peykare پیکرهٔ](https://www.peykaregan.ir/dataset/%D9%BE%DB%8C%DA%A9%D8%B1%D9%87-%D9%85%D8%AA%D9%86%DB%8C-%D8%B2%D8%A8%D8%A7%D9%86-%D9%81%D8%A7%D8%B1%D8%B3%DB%8C)
جموعه‌ای از متون نوشتاری و گفتاری رسمی زبان فارسی است که از منابع واقعی همچون
روزنامه‌ها، سایت‌ها و مستنداتِ از قبل تایپ‌شده، جمع‌آوری شده، تصحیح گردیده و
برچسب خورده است. حجم این دادگان حدوداً ۱۰۰ میلیون کلمه است و از منابع مختلف تهیه
گردیده و دارای تنوع بسیار زیادی است. ۱۰ میلیون کلمه از این پیکره با استفاده از
۸۸۲ برچسب نحوی-معنایی به صورت دستی توسط دانشجویان رشتهٔ زبان‌شناسی برچسب‌دهی
شده‌اند و هر پرونده بر حسب موضوع و منبع آن طبقه‌بندی شده است. این پیکره که توسط
پژوهشکده پردازش هوشمند علائم تهیه شده است، برای استفاده در آموزش مدل زبانی و
سایر پروژه‌های مربوط به پردازش زبان طبیعی مناسب است.
"""

from __future__ import unicode_literals
import os, codecs
from .Normalizer import Normalizer
from .WordTokenizer import WordTokenizer


def coarse_pos_e(tags):
    """برچسب‌های ریز را به برچسب‌های درشت (coarse-grained pos tags) تبدیل می‌کند.

    Examples:
            >>> coarse_pos_e(['N','COM','SING'])
            'N'

    Args:
            tags (List[str]): لیست برچسب‌های ریز.

    Returns:
            (List[str]): لیست برچسب‌های درشت.
    """

    try:
        return list(
            set(tags)
            & {
                "N",
                "V",
                "AJ",
                "ADV",
                "PRO",
                "DET",
                "P",
                "POSTP",
                "NUM",
                "CONJ",
                "PUNC",
                "CL",
                "INT",
                "RES",
            }
        )[0] + ("e" if "EZ" in tags else "")
    except:
        return "N"


def join_verb_parts(sentence):
    """جمله را در قالب لیستی از `(توکن، برچسب)‌`ها می‌گیرد و توکن‌های مربوط به افعال چندبخشی را با کاراکتر زیرخط (_) به هم می‌چسباند.

    Examples:
            >>> join_verb_parts([('اولین', 'AJ'), ('سیاره', 'Ne'), ('خارج', 'AJ'), ('از', 'P'), ('منظومه', 'Ne'), ('شمسی', 'AJ'), ('دیده', 'AJ'), ('شد', 'V'), ('.', 'PUNC')])
            [('اولین', 'AJ'), ('سیاره', 'Ne'), ('خارج', 'AJ'), ('از', 'P'), ('منظومه', 'Ne'), ('شمسی', 'AJ'), ('دیده_شد', 'V'), ('.', 'PUNC')]

    Args:
            sentence(List[Tuple[str,str]]): جمله در قالب لیستی از `(توکن، برچسب)`ها.

    Returns:
            (List[Tuple[str, str]): لیستی از `(توکن، برچسب)`ها که در آن افعال چندبخشی در قالب یک توکن با کاراکتر زیرخط به هم چسبانده شده‌اند.
    """

    if not hasattr(join_verb_parts, "tokenizer"):
        join_verb_parts.tokenizer = WordTokenizer()
    before_verbs, after_verbs, verbe = (
        join_verb_parts.tokenizer.before_verbs,
        join_verb_parts.tokenizer.after_verbs,
        join_verb_parts.tokenizer.verbe,
    )

    result = [("", "")]
    for word in reversed(sentence):
        if word[0] in before_verbs or (
            result[-1][0] in after_verbs and word[0] in verbe
        ):
            result[-1] = (word[0] + "_" + result[-1][0], result[-1][1])
        else:
            result.append(word)
    return list(reversed(result[1:]))


class PeykareReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ Peykare است.

    Args:
            root (str): آدرس فولدر حاوی فایل‌های پیکره.
            join_verb_parts (bool, optional): اگر `True‍` باشد افعال چندقسمتی به‌شکل چسبیده‌به‌هم برگردانده_می‌شود.
            pos_map (str): دیکشنری مبدل برچسب‌های ریز به درشت.
    """

    def __init__(self, root, joined_verb_parts=True, pos_map=coarse_pos_e):
        self._root = root
        self._pos_map = pos_map if pos_map else lambda tags: ",".join(tags)
        self._joined_verb_parts = joined_verb_parts
        self._normalizer = Normalizer(punctuation_spacing=False, affix_spacing=False)

    def docs(self):
        """اسناد را به شکل متن خام برمی‌گرداند.

        Yields:
                (str): متن خام سند بعدی.
        """

        for root, dirs, files in os.walk(self._root):
            for name in sorted(files):
                with codecs.open(
                    os.path.join(root, name), encoding="windows-1256"
                ) as peykare_file:
                    text = peykare_file.read()
                    if text:
                        yield text

    def doc_to_sents(self, document):
        """سند ورودی را به لیستی از جملات تبدیل می‌کند.

        هر جمله لیستی از `(کلمه, برچسب)`ها است.

        Args:
                document (str): سندی که باید تبدیل شود.

        Yields:
                (List[(str,str)]): `ها جملهٔ بعدی در قالب لیستی از `(کلمه، برچسب).
        """

        sentence = []
        for line in document.split("\r\n"):
            if not line:
                continue

            parts = line.split(" ")
            tags, word = parts[3], self._normalizer.normalize("‌".join(parts[4:]))

            if word and word != "#":
                sentence.append((word, tags))

            if parts[2] == "PUNC" and word in {"#", ".", "؟", "!"}:
                if len(sentence) > 1:
                    yield sentence
                sentence = []

    def sents(self):
        """جملات پیکره را در قالب لیستی از `(توکن، برچسب)`ها برمی‌گرداند.

        Examples:
                >>> peykare = PeykareReader(root='corpora/peykare')
                >>> next(peykare.sents())
                [('دیرزمانی', 'N'), ('از', 'P'), ('راه‌اندازی', 'Ne'), ('شبکه‌ی', 'Ne'), ('خبر', 'Ne'), ('الجزیره', 'N'), ('نمی‌گذرد', 'V'), ('،', 'PUNC'), ('اما', 'CONJ'), ('این', 'DET'), ('شبکه‌ی', 'Ne'), ('خبری', 'AJe'), ('عربی', 'N'), ('بسیار', 'ADV'), ('سریع', 'ADV'), ('توانسته', 'V'), ('در', 'P'), ('میان', 'Ne'), ('شبکه‌های', 'Ne'), ('عظیم', 'AJe'), ('خبری', 'AJ'), ('و', 'CONJ'), ('بنگاه‌های', 'Ne'), ('چندرسانه‌ای', 'AJe'), ('دنیا', 'N'), ('خودی', 'N'), ('نشان', 'N'), ('دهد', 'V'), ('.', 'PUNC')]

                >>> peykare = PeykareReader(root='corpora/peykare', joined_verb_parts=False, pos_map=None)
                >>> next(peykare.sents())
                [('دیرزمانی', 'N,COM,SING,TIME,YA'), ('از', 'P'), ('راه‌اندازی', 'N,COM,SING,EZ'), ('شبکه‌ی', 'N,COM,SING,EZ'), ('خبر', 'N,COM,SING,EZ'), ('الجزیره', 'N,PR,SING'), ('نمی‌گذرد', 'V,PRES,NEG,3'), ('،', 'PUNC'), ('اما', 'CONJ'), ('این', 'DET,DEMO'), ('شبکه‌ی', 'N,COM,SING,EZ'), ('خبری', 'AJ,SIM,EZ'), ('عربی', 'N,PR,SING'), ('بسیار', 'ADV,INTSF,SIM'), ('سریع', 'ADV,GENR,SIM'), ('توانسته', 'V,PASTP'), ('در', 'P'), ('میان', 'N,COM,SING,EZ'), ('شبکه‌های', 'N,COM,PL,EZ'), ('عظیم', 'AJ,SIM,EZ'), ('خبری', 'AJ,SIM'), ('و', 'CONJ'), ('بنگاه‌های', 'N,COM,PL,EZ'), ('چندرسانه‌ای', 'AJ,SIM,EZ'), ('دنیا', 'N,COM,SING'), ('خودی', 'N,COM,SING,YA'), ('نشان', 'N,COM,SING'), ('دهد', 'V,SUB,POS,3'), ('.', 'PUNC')]

        Yields:
                (List[Tuple[str,str]]): جملهٔ بعدی در قالب لیستی از `(توکن، برچسب)`ها.
        """
        map_pos = lambda item: (item[0], self._pos_map(item[1].split(",")))

        for document in self.docs():
            for sentence in self.doc_to_sents(document):
                if self._joined_verb_parts:
                    sentence = join_verb_parts(sentence)

                yield list(map(map_pos, sentence))
