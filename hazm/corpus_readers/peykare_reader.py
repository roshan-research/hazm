"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ Peykare است.

[peykare پیکرهٔ](https://www.peykaregan.ir/dataset/%D9%BE%DB%8C%DA%A9%D8%B1%D9%
87-%D9%85%D8%AA%D9%86%DB%8C-%D8%B2%D8%A8%D8%A7%D9%86-
%D9%81%D8%A7%D8%B1%D8%B3%DB%8C)
جموعه‌ای از متون نوشتاری و گفتاری رسمی زبان فارسی است که از منابع واقعی همچون
روزنامه‌ها، سایت‌ها و مستنداتِ از قبل تایپ‌شده، جمع‌آوری شده، تصحیح گردیده و
برچسب خورده است. حجم این دادگان حدوداً ۱۰۰ میلیون کلمه است و از منابع مختلف
تهیه
گردیده و دارای تنوع بسیار زیادی است. ۱۰ میلیون کلمه از این پیکره با استفاده از
۸۸۲ برچسب نحوی-معنایی به صورت دستی توسط دانشجویان رشتهٔ زبان‌شناسی برچسب‌دهی
شده‌اند و هر پرونده بر حسب موضوع و منبع آن طبقه‌بندی شده است. این پیکره که توسط
پژوهشکده پردازش هوشمند علائم تهیه شده است، برای استفاده در آموزش مدل زبانی و
سایر پروژه‌های مربوط به پردازش زبان طبیعی مناسب است.

"""


import codecs
import os
from pathlib import Path
from typing import Any
from typing import Iterator
from typing import List
from typing import Tuple

from hazm.normalizer import Normalizer
from hazm.word_tokenizer import WordTokenizer


def coarse_pos_u(tags: List[str], word: str) -> List[str]:
    """برچسب‌های ریز را به برچسب‌های درشت منطبق با استاندارد جهانی (coarse-grained
    universal pos tags) تبدیل می‌کند.

    Examples:
        >>> coarse_pos_u(['N','COM','SING'], 'الجزیره')
        'NOUN'

    Args:
        tags: لیست برچسب‌های ریز.
        word: برچسبی که می‌خواهید به برچسب جهانی تبدیل شود.

    Returns:
        لیست برچسب‌های درشت جهانی.

    """
    map_pos_to_upos = {
        "N": "NOUN",
        "V": "VERB",
        "AJ": "ADJ",
        "ADV": "ADV",
        "PRO": "PRON",
        "DET": "DET",
        "P": "ADP",
        "POSTP": "ADP",
        "NUM": "NUM",
        "CONJ": "CCONJ",
        "PUNC": "PUNCT",
        "CL": "NOUN",
        "INT": "INTJ",
        "RES": "NOUN",
    }
    sconj_list = {
        "که",
        "تا",
        "گرچه",
        "اگرچه",
        "چرا",
        "زیرا",
        "اگر",
        "چون",
        "چراکه",
        "هرچند",
        "وگرنه",
        "چنانچه",
        "والا",
        "هرچه",
        "ولو",
        "مگر",
        "پس",
        "چو",
        "چه",
        "بنابراین",
        "وقتی",
        "والّا",
        "انگاری",
        "هرچندكه",
        "درنتيجه",
        "اگه",
        "ازآنجاكه",
        "گر",
        "وگر",
        "وقتيكه",
        "تااينكه",
        "زمانيكه",
    }
    num_adj_list = {
        "نخست",
        "دوم",
        "اول",
        "پنجم",
        "آخر",
        "يازدهم",
        "نهم",
        "چهارم",
        "ششم",
        "پانزدهم",
        "دوازدهم",
        "هشتم",
        "صدم",
        "هفتم",
        "هفدهم",
        "آخرين",
        "سيزدهم",
        "يكم",
        "بيستم",
        "ويكم",
        "دوسوم",
        "شانزدهم",
        "هجدهم",
        "چهاردهم",
        "ششصدم",
        "ميليونيم",
        "وهفتم",
        "يازدهمين",
        "هيجدهمين",
        "واپسين",
        "چهلم",
        "هزارم",
        "وپنجم",
        "هيجدهم",
        "ميلياردم",
        "ميليونيوم",
        "تريليونيوم",
        "چهارپنجم",
        "دهگانه",
        "ميليونم",
        "اوّل",
        "سوّم",
    }
    try:
        old_pos = list(
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
            },
        )[0]
        if old_pos == "CONJ" and word in sconj_list:
            return "SCONJ"
        if old_pos == "NUM" and word in num_adj_list:
            return "ADJ" + (",EZ" if "EZ" in tags else "")
        return map_pos_to_upos[old_pos] + (",EZ" if "EZ" in tags else "")
    except:
        return "NOUN"


def coarse_pos_e(tags: List[str], word) -> List[str]: # noqa: D417, ARG001
    """برچسب‌های ریز را به برچسب‌های درشت (coarse-grained pos tags) تبدیل می‌کند.

    Examples:
        >>> coarse_pos_e(['N','COM','SING'],'الجزیره')
        'N'

    Args:
        tags: لیست برچسب‌های ریز.

    Returns:
        لیست برچسب‌های درشت.

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
            },
        )[0] + (",EZ" if "EZ" in tags else "")
    except:
        return "N"


def join_verb_parts(sentence: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """جمله را در قالب لیستی از `(توکن، برچسب)‌`ها می‌گیرد و توکن‌های مربوط به
    افعال چندبخشی را با کاراکتر زیرخط (_) به هم می‌چسباند.

    Examples:
        >>> join_verb_parts([('اولین', 'AJ'), ('سیاره', 'Ne'), ('خارج', 'AJ'), ('از', 'P'), ('منظومه', 'Ne'), ('شمسی', 'AJ'), ('دیده', 'AJ'), ('شد', 'V'), ('.', 'PUNC')])
        [('اولین', 'AJ'), ('سیاره', 'Ne'), ('خارج', 'AJ'), ('از', 'P'), ('منظومه', 'Ne'), ('شمسی', 'AJ'), ('دیده_شد', 'V'), ('.', 'PUNC')]

    Args:
        sentence: جمله در قالب لیستی از `(توکن، برچسب)`ها.

    Returns:
        لیستی از `(توکن، برچسب)`ها که در آن افعال چندبخشی در قالب یک توکن با کاراکتر زیرخط به هم چسبانده شده‌اند.

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
        root: آدرس فولدر حاوی فایل‌های پیکره.
        joined_verb_parts: اگر `True‍` باشد افعال چندقسمتی به‌شکل چسبیده‌به‌هم برگردانده_می‌شود.
        pos_map: دیکشنری مبدل برچسب‌های ریز به درشت.

    """

    def __init__(
        self: "PeykareReader",
        root: str,
        joined_verb_parts: bool = True,
        pos_map: str = coarse_pos_e,
        universal_pos: bool = False,
    ) -> None:
        self._root = root
        if pos_map is None:
            self._pos_map = lambda tags: ",".join(tags)
        elif universal_pos:
            self._pos_map = coarse_pos_u
        else:
            self._pos_map = coarse_pos_e
        self._joined_verb_parts = joined_verb_parts
        self._normalizer = Normalizer(correct_spacing=False)

    def docs(self: "PeykareReader") -> Iterator[str]:
        """اسناد را به شکل متن خام برمی‌گرداند.

        Yields:
            متن خام سند بعدی.

        """
        for root, _, files in os.walk(self._root):
            for name in sorted(files):
                with Path.open(
                    Path(root) / name,
                    encoding="windows-1256",
                ) as peykare_file:
                    text = peykare_file.read()
                    # Convert all EOL to CRLF
                    text = text.replace("\r\n", "\n").replace("\n", "\r\n")
                    if text:
                        yield text

    def doc_to_sents(
        self: "PeykareReader", document: str,
    ) -> Iterator[List[Tuple[str, str]]]:
        """سند ورودی را به لیستی از جملات تبدیل می‌کند.

        هر جمله لیستی از `(کلمه, برچسب)`ها است.

        Args:
            document: سندی که باید تبدیل شود.

        Yields:
            `ها جملهٔ بعدی در قالب لیستی از `(کلمه، برچسب).

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

    def sents(self: "PeykareReader") -> Iterator[List[Tuple[str, str]]]:
        """جملات پیکره را در قالب لیستی از `(توکن، برچسب)`ها برمی‌گرداند.

        Examples:
            >>> peykare = PeykareReader(root='peykare')
            >>> next(peykare.sents())
            [('دیرزمانی', 'N'), ('از', 'P'), ('راه\u200cاندازی', 'N,EZ'), ('شبکه\u200cی', 'N,EZ'), ('خبر', 'N,EZ'), ('الجزیره', 'N'), ('نمی\u200cگذرد', 'V'), ('،', 'PUNC'), ('اما', 'CONJ'), ('این', 'DET'), ('شبکه\u200cی', 'N,EZ'), ('خبری', 'AJ,EZ'), ('عربی', 'N'), ('بسیار', 'ADV'), ('سریع', 'ADV'), ('توانسته', 'V'), ('در', 'P'), ('میان', 'N,EZ'), ('شبکه\u200cهای', 'N,EZ'), ('عظیم', 'AJ,EZ'), ('خبری', 'AJ'), ('و', 'CONJ'), ('بنگاه\u200cهای', 'N,EZ'), ('چندرسانه\u200cای', 'AJ,EZ'), ('دنیا', 'N'), ('خودی', 'N'), ('نشان', 'N'), ('دهد', 'V'), ('.', 'PUNC')]

        Yields:
            جملهٔ بعدی در قالب لیستی از `(توکن، برچسب)`ها.

        """

        # >>> peykare = PeykareReader(root='peykare', joined_verb_parts=False, pos_map=None)
        # >>> next(peykare.sents())
        def map_pos(item: str) -> Tuple:
            return (item[0], self._pos_map(item[1].split(","), item[0]))

        for document in self.docs():
            for sentence in self.doc_to_sents(document):
                if self._joined_verb_parts:
                    sentence = join_verb_parts(sentence)

                yield list(map(map_pos, sentence))
