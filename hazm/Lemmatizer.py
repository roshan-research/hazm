# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای ریشه‌یابی کلمات است. 

فرق بین [Lemmatizer](./Lemmatizer.md) و [Stemmer](./Stemmer.md) این است که
اِستمر درکی از معنای کلمه ندارد و صرفاً براساس حذف برخی از پسوندهای ساده تلاش
می‌کند ریشهٔ کلمه را بیابد؛ بنابراین ممکن است در ریشه‌یابیِ برخی از کلمات نتایج
نادرستی ارائه دهد؛ اما لماتایزر براساس لیستی از کلمات مرجع به همراه ریشهٔ آن این
کار را انجام می‌دهد و نتایج دقیق‌تری ارائه می‌دهد. البته هزینهٔ این دقت، سرعتِ
کمتر در ریشه‌یابی است.
"""

from __future__ import unicode_literals
from .utils import default_words, default_verbs
from .Stemmer import Stemmer
from .WordTokenizer import WordTokenizer


class Lemmatizer(object):
    """این کلاس شامل توابعی برای ریشه‌یابی کلمات است.

    Args:
            words_file (str, optional): ریشه‌یابی کلمات از روی این فایل صورت
                    می‌گیرد. هضم به صورت پیش‌فرض فایلی برای این منظور در نظر گرفته است؛ با
                    این حال شما می‌توانید فایل موردنظر خود را معرفی کنید. برای آگاهی از
                    ساختار این فایل به فایل پیش‌فرض مراجعه کنید.
            verbs_file (str, optional): اشکال صرفی فعل از روی این فایل ساخته
                    می‌شود. هضم به صورت پیش‌فرض فایلی برای این منظور در نظر گرفته است؛ با
                    این حال شما می‌توانید فایل موردنظر خود را معرفی کنید. برای آگاهی از
                    ساختار این فایل به فایل پیش‌فرض مراجعه کنید.
            joined_verb_parts (bool, optional): اگر `True` باشد افعال چندبخشی را با کاراکتر زیرخط به هم می‌چسباند.
    """

    def __init__(
        self, words_file=default_words, verbs_file=default_verbs, joined_verb_parts=True
    ):
        self.verbs = {}
        self.stemmer = Stemmer()

        tokenizer = WordTokenizer(words_file=default_words, verbs_file=verbs_file)
        self.words = tokenizer.words

        if verbs_file:
            self.verbs["است"] = "#است"
            for verb in tokenizer.verbs:
                for tense in self.conjugations(verb):
                    self.verbs[tense] = verb
            if joined_verb_parts:
                for verb in tokenizer.verbs:
                    bon = verb.split("#")[0]
                    for after_verb in tokenizer.after_verbs:
                        self.verbs[bon + "ه_" + after_verb] = verb
                        self.verbs["ن" + bon + "ه_" + after_verb] = verb
                    for before_verb in tokenizer.before_verbs:
                        self.verbs[before_verb + "_" + bon] = verb

    def lemmatize(self, word, pos=""):
        """ریشهٔ کلمه را پیدا می‌کند.

        پارامتر `pos` نوع کلمه است: (اسم، فعل، صفت و ...) و به این خاطر لازم
        است که می‌تواند روی ریشه‌یابی کلمات اثر بگذارد؛ مثلاً واژهٔ «اجتماعی» در
        جایگاه صفت (او یک فرد اجتماعی است)، ریشه‌اش همان «اجتماعی» می‌شود ولی
        همین واژه در جایگاه اسم (اجتماعی از مردم)، ریشه‌اش می‌شود «اجتماع».

        Examples:
                >>> lemmatizer = Lemmatizer()
                >>> lemmatizer.lemmatize('کتاب‌ها')
                'کتاب'
                >>> lemmatizer.lemmatize('آتشفشان')
                'آتشفشان'
                >>> lemmatizer.lemmatize('می‌روم')
                'رفت#رو'
                >>> lemmatizer.lemmatize('گفته_شده_است')
                'گفت#گو'
                >>> lemmatizer.lemmatize('نچشیده_است')
                'چشید#چش'
                >>> lemmatizer.lemmatize('مردم', pos='N')
                'مردم'
                >>> lemmatizer.lemmatize('اجتماعی', pos='AJ')
                'اجتماعی'

        Args:
                word (str): کلمه‌ای که باید پردازش شود.
                pos (str, optional): نوع کلمه. این پارامتر سه مقدار `V` (فعل) و `AJ` (صفت) و `PRO` (ضمیر) را می‌پذیرد.

        Returns:
                (str): ریشهٔ کلمه
        """
        if not pos and word in self.words:
            return word

        if (not pos or pos == "V") and word in self.verbs:
            return self.verbs[word]

        if pos.startswith("AJ") and word[-1] == "ی":
            return word

        if pos == "PRO":
            return word

        if word in self.words:
            return word

        stem = self.stemmer.stem(word)
        if stem and stem in self.words:
            return stem

        return word

    def conjugations(self, verb):
        """صورت‌های صرفی فعل را برمی‌گرداند.

        Examples:
                >>> lemmatizer = Lemmatizer()
                >>> lemmatizer.conjugations('خورد#خور')
                ['خوردم', 'خوردی', 'خورد', 'خوردیم', 'خوردید', 'خوردند', 'نخوردم', 'نخوردی', 'نخورد', 'نخوردیم', 'نخوردید', 'نخوردند', 'خورم', 'خوری', 'خورد', 'خوریم', 'خورید', 'خورند', 'نخورم', 'نخوری', 'نخورد', 'نخوریم', 'نخورید', 'نخورند', 'می‌خوردم', 'می‌خوردی', 'می‌خورد', 'می‌خوردیم', 'می‌خوردید', 'می‌خوردند', 'نمی‌خوردم', 'نمی‌خوردی', 'نمی‌خورد', 'نمی‌خوردیم', 'نمی‌خوردید', 'نمی‌خوردند', 'خورده‌ام', 'خورده‌ای', 'خورده', 'خورده‌ایم', 'خورده‌اید', 'خورده‌اند', 'نخورده‌ام', 'نخورده‌ای', 'نخورده', 'نخورده‌ایم', 'نخورده‌اید', 'نخورده‌اند', 'خورم', 'خوری', 'خورد', 'خوریم', 'خورید', 'خورند', 'نخورم', 'نخوری', 'نخورد', 'نخوریم', 'نخورید', 'نخورند', 'می‌خورم', 'می‌خوری', 'می‌خورد', 'می‌خوریم', 'می‌خورید', 'می‌خورند', 'نمی‌خورم', 'نمی‌خوری', 'نمی‌خورد', 'نمی‌خوریم', 'نمی‌خورید', 'نمی‌خورند', 'بخورم', 'بخوری', 'بخورد', 'بخوریم', 'بخورید', 'بخورند', 'نخورم', 'نخوری', 'نخورد', 'نخوریم', 'نخورید', 'نخورند', 'بخور', 'نخور']
                >>> lemmatizer.conjugations('آورد#آور')
                ['آوردم', 'آوردی', 'آورد', 'آوردیم', 'آوردید', 'آوردند', 'نیاوردم', 'نیاوردی', 'نیاورد', 'نیاوردیم', 'نیاوردید', 'نیاوردند', 'آورم', 'آوری', 'آورد', 'آوریم', 'آورید', 'آورند', 'نیاورم', 'نیاوری', 'نیاورد', 'نیاوریم', 'نیاورید', 'نیاورند', 'می‌آوردم', 'می‌آوردی', 'می‌آورد', 'می‌آوردیم', 'می‌آوردید', 'می‌آوردند', 'نمی‌آوردم', 'نمی‌آوردی', 'نمی‌آورد', 'نمی‌آوردیم', 'نمی‌آوردید', 'نمی‌آوردند', 'آورده‌ام', 'آورده‌ای', 'آورده', 'آورده‌ایم', 'آورده‌اید', 'آورده‌اند', 'نیاورده‌ام', 'نیاورده‌ای', 'نیاورده', 'نیاورده‌ایم', 'نیاورده‌اید', 'نیاورده‌اند', 'آورم', 'آوری', 'آورد', 'آوریم', 'آورید', 'آورند', 'نیاورم', 'نیاوری', 'نیاورد', 'نیاوریم', 'نیاورید', 'نیاورند', 'می‌آورم', 'می‌آوری', 'می‌آورد', 'می‌آوریم', 'می‌آورید', 'می‌آورند', 'نمی‌آورم', 'نمی‌آوری', 'نمی‌آورد', 'نمی‌آوریم', 'نمی‌آورید', 'نمی‌آورند', 'بیاورم', 'بیاوری', 'بیاورد', 'بیاوریم', 'بیاورید', 'بیاورند', 'نیاورم', 'نیاوری', 'نیاورد', 'نیاوریم', 'نیاورید', 'نیاورند', 'بیاور', 'نیاور']

        Args:
                verb (str): فعلی که باید صرف شود.

        Returns:
                (List[str]): لیستِ صورت‌های صرفی فعل.
        """

        past, present = verb.split("#")
        ends = ["م", "ی", "", "یم", "ید", "ند"]

        if verb == "#هست":
            return ["هست" + end for end in ends] + ["نیست" + end for end in ends]

        past_simples = [past + end for end in ends]
        past_imperfects = ["می‌" + item for item in past_simples]
        ends = ["ه‌ام", "ه‌ای", "ه", "ه‌ایم", "ه‌اید", "ه‌اند"]
        past_narratives = [past + end for end in ends]

        imperatives = ["ب" + present, "ن" + present]

        if present.endswith("ا") or present in ("آ", "گو"):
            present = present + "ی"

        ends = ["م", "ی", "د", "یم", "ید", "ند"]
        present_simples = [present + end for end in ends]
        present_imperfects = ["می‌" + item for item in present_simples]
        present_subjunctives = [
            item if item.startswith("ب") else "ب" + item for item in present_simples
        ]
        present_not_subjunctives = ["ن" + item for item in present_simples]

        with_nots = lambda items: items + list(map(lambda item: "ن" + item, items))
        aa_refinement = (
            lambda items: list(
                map(lambda item: item.replace("بآ", "بیا").replace("نآ", "نیا"), items)
            )
            if items[0].startswith("آ")
            else items
        )
        return aa_refinement(
            with_nots(past_simples)
            + with_nots(present_simples)
            + with_nots(past_imperfects)
            + with_nots(past_narratives)
            + with_nots(present_simples)
            + with_nots(present_imperfects)
            + present_subjunctives
            + present_not_subjunctives
            + imperatives
        )
