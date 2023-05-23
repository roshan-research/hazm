"""این ماژول شامل کلاس‌ها و توابعی برای ریشه‌یابی کلمات است.

فرق بین [Lemmatizer](./lemmatizer.md) و [Stemmer](./stemmer.md) این است که
اِستمر درکی از معنای کلمه ندارد و صرفاً براساس حذف برخی از پسوندهای ساده تلاش
می‌کند ریشهٔ کلمه را بیابد؛ بنابراین ممکن است در ریشه‌یابیِ برخی از کلمات نتایج
نادرستی ارائه دهد؛ اما لماتایزر براساس لیستی از کلمات مرجع به همراه ریشهٔ آن
این
کار را انجام می‌دهد و نتایج دقیق‌تری ارائه می‌دهد. البته هزینهٔ این دقت، سرعتِ
کمتر در ریشه‌یابی است.

**میزان دقت
لماتایزر در نسخهٔ حاضر ۸۹.۹ درصد [^1] است.**
[^1]:
این عدد با انتشار هر نسخه بروزرسانی می‌شود

"""


from typing import List

from hazm import Stemmer
from hazm import WordTokenizer
from hazm import default_verbs
from hazm import default_words


class Lemmatizer:
    """این کلاس شامل توابعی برای ریشه‌یابی کلمات است.

    Args:
        words_file: ریشه‌یابی کلمات از روی این فایل صورت
            می‌گیرد. هضم به صورت پیش‌فرض فایلی برای این منظور در نظر گرفته است؛ با
            این حال شما می‌توانید فایل موردنظر خود را معرفی کنید. برای آگاهی از
            ساختار این فایل به فایل پیش‌فرض مراجعه کنید.
        verbs_file: اشکال صرفی فعل از روی این فایل ساخته
            می‌شود. هضم به صورت پیش‌فرض فایلی برای این منظور در نظر گرفته است؛ با
            این حال شما می‌توانید فایل موردنظر خود را معرفی کنید. برای آگاهی از
            ساختار این فایل به فایل پیش‌فرض مراجعه کنید.
        joined_verb_parts: اگر `True` باشد افعال چندبخشی را با کاراکتر زیرخط به هم می‌چسباند.

    """

    def __init__(
        self: "Lemmatizer",
        words_file: str = default_words,
        verbs_file: str = default_verbs,
        joined_verb_parts: bool = True,
    ) -> None:
        self.words_file = words_file
        self.verbs = {}
        self.stemmer = Stemmer()
        self.conjugation = Conjugation()

        tokenizer = WordTokenizer(words_file=default_words, verbs_file=verbs_file)
        self.words = tokenizer.words

        if verbs_file:
            self.verbs["است"] = "#است"
            for verb in tokenizer.verbs:
                for tense in self.conjugation.get_all(verb):
                    self.verbs[tense] = verb
            if joined_verb_parts:
                for verb in tokenizer.verbs:
                    bon = verb.split("#")[0]
                    for after_verb in tokenizer.after_verbs:
                        self.verbs[bon + "ه_" + after_verb] = verb
                        self.verbs["ن" + bon + "ه_" + after_verb] = verb
                    for before_verb in tokenizer.before_verbs:
                        self.verbs[before_verb + "_" + bon] = verb

    def lemmatize(self: "Lemmatizer", word: str, pos: str = "") -> str:
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
            word: کلمه‌ای که باید پردازش شود.
            pos: نوع کلمه. این پارامتر سه مقدار `V` (فعل) و `AJ` (صفت) و `PRO` (ضمیر) را می‌پذیرد.

        Returns:
            ریشهٔ کلمه

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


class Conjugation:
    """این کلاس دارای توابعی برای صرف‌کردن افعال است."""

    def perfective_past(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ مطلق صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.perfective_past('دید')
            ['دیدم', 'دیدی', 'دید', 'دیدیم', 'دیدید', 'دیدند']

        Args:
            ri: بن ماضی فعل.

        Returns:
            صورت‌های صرفی فعل در زمان گذشتهٔ مطلق.
        """
        return [ri + x for x in ["م", "ی", "", "یم", "ید", "ند"]]

    def negative_perfective_past(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ مطلق به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_perfective_past('دید')
            ['ندیدم', 'ندیدی', 'ندید', 'ندیدیم', 'ندیدید', 'ندیدند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ مطلق به‌شکل منفی.
        """
        return ["ن" + x for x in self.perfective_past(ri)]

    def passive_perfective_past(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ مطلق در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_perfective_past('دید')
            ['دیده شدم', 'دیده شدی', 'دیده شد', 'دیده شدیم', 'دیده شدید', 'دیده شدند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ مطلق در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.perfective_past("شد")]

    def negative_passive_perfective_past(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ مطلق در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_perfective_past('دید')
            ['دیده نشدم', 'دیده نشدی', 'دیده نشد', 'دیده نشدیم', 'دیده نشدید', 'دیده نشدند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ مطلق در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_perfective_past("شد")]

    def imperfective_past(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پایا صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.imperfective_past('دید')
            ['می‌دیدم', 'می‌دیدی', 'می‌دید', 'می‌دیدیم', 'می‌دیدید', 'می‌دیدند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پایا.
        """
        return ["می‌" + x for x in self.perfective_past(ri)]

    def negative_imperfective_past(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پایا به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_imperfective_past('دید')
            ['نمی‌دیدم', 'نمی‌دیدی', 'نمی‌دید', 'نمی‌دیدیم', 'نمی‌دیدید', 'نمی‌دیدند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پایا به‌شکل منفی.
        """
        return ["ن" + x for x in self.imperfective_past(ri)]

    def passive_imperfective_past(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پایا در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_imperfective_past('دید')
            ['دیده می‌شدم', 'دیده می‌شدی', 'دیده می‌شد', 'دیده می‌شدیم', 'دیده می‌شدید', 'دیده می‌شدند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پایا در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.imperfective_past("شد")]

    def negative_passive_imperfective_past(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پایا در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_imperfective_past('دید')
            ['دیده نمی‌شدم', 'دیده نمی‌شدی', 'دیده نمی‌شد', 'دیده نمی‌شدیم', 'دیده نمی‌شدید', 'دیده نمی‌شدند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پایا در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_imperfective_past("شد")]

    def past_progresive(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ استمراری صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.past_progresive('دید')
            ['داشتم می‌دیدم', 'داشتی می‌دیدی', 'داشت می‌دید', 'داشتیم می‌دیدیم', 'داشتید می‌دیدید', 'داشتند می‌دیدند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ استمراری.
        """
        return [
            x + " " + y
            for x, y in zip(self.perfective_past("داشت"), self.imperfective_past(ri))
        ]

    def passive_past_progresive(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ استمراری در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_past_progresive('دید')
            ['داشتم دیده می‌شدم', 'داشتی دیده می‌شدی', 'داشت دیده می‌شد', 'داشتیم دیده می‌شدیم', 'داشتید دیده می‌شدید', 'داشتند دیده می‌شدند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ استمراری در حالت مجهول.
        """
        return [
            x + " " + y
            for x, y in zip(
                self.perfective_past("داشت"),
                self.passive_imperfective_past(ri),
            )
        ]

    def present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.present_perfect('دید')
            ['دیده‌ام', 'دیده‌ای', 'دیده است', 'دیده', 'دیده‌ایم', 'دیده‌اید', 'دیده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل.
        """
        return [ri + x for x in ["ه‌ام", "ه‌ای", "ه است", "ه", "ه‌ایم", "ه‌اید", "ه‌اند"]]

    def negative_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_present_perfect('دید')
            ['ندیده‌ام', 'ندیده‌ای', 'ندیده است', 'ندیده', 'ندیده‌ایم', 'ندیده‌اید', 'ندیده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل به‌شکل منفی.
        """
        return ["ن" + x for x in self.present_perfect(ri)]

    def subjunctive_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل در وجه التزامی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.subjunctive_present_perfect('دید')
            ['دیده باشم', 'دیده باشی', 'دیده باشد', 'دیده باشیم', 'دیده باشید', 'دیده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل در وجه التزامی.
        """
        return [ri + "ه " + x for x in self.perfective_present("باش")]

    def negative_subjunctive_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل در وجه التزامی به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_subjunctive_present_perfect('دید')
            ['ندیده باشم', 'ندیده باشی', 'ندیده باشد', 'ندیده باشیم', 'ندیده باشید', 'ندیده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل در وجه التزامی به‌شکل منفی.
        """
        return ["ن" + x for x in self.subjunctive_present_perfect(ri)]

    def grammatical_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل در وجه دستوری صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.grammatical_present_perfect('دید')
            ['دیده باشم', 'دیده باش', 'دیده باشد', 'دیده باشیم', 'دیده باشید', 'دیده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل در وجه دستوری.
        """
        return [
            ri + "ه " + ("باش" if x == "باشی" else x)
            for x in self.perfective_present("باش")
        ]

    def negative_grammatical_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل در وجه دستوری به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_grammatical_present_perfect('دید')
            ['ندیده باشم', 'ندیده باش', 'ندیده باشد', 'ندیده باشیم', 'ندیده باشید', 'ندیده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل در وجه دستوری به‌شکل منفی.
        """
        return [
            "ن" + ri + "ه " + ("باش" if x == "باشی" else x)
            for x in self.perfective_present("باش")
        ]

    def passive_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_present_perfect('دید')
            ['دیده شده‌ام', 'دیده شده‌ای', 'دیده شده است', 'دیده شده', 'دیده شده‌ایم', 'دیده شده‌اید', 'دیده شده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.present_perfect("شد")]

    def negative_passive_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_present_perfect('دید')
            ['دیده نشده‌ام', 'دیده نشده‌ای', 'دیده نشده است', 'دیده نشده', 'دیده نشده‌ایم', 'دیده نشده‌اید', 'دیده نشده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_present_perfect("شد")]

    def passive_subjunctive_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل در وجه التزامی در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_subjunctive_present_perfect('دید')
            ['دیده شده باشم', 'دیده شده باشی', 'دیده شده باشد', 'دیده شده باشیم', 'دیده شده باشید', 'دیده شده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل در وجه التزامی در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.subjunctive_present_perfect("شد")]

    def negative_passive_subjunctive_present_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال کامل در وجه التزامی در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_subjunctive_present_perfect('دید')
            ['دیده نشده باشم', 'دیده نشده باشی', 'دیده نشده باشد', 'دیده نشده باشیم', 'دیده نشده باشید', 'دیده نشده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل در وجه التزامی در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_subjunctive_present_perfect("شد")]

    def passive_grammatical_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل در وجه دستوری در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_grammatical_present_perfect('دید')
            ['دیده شده باشم', 'دیده شده باش', 'دیده شده باشد', 'دیده شده باشیم', 'دیده شده باشید', 'دیده شده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل در وجه دستوری در حالت مجهول.
        """
        return [
            ri + "ه شده " + ("باش" if x == "باشی" else x)
            for x in self.perfective_present("باش")
        ]

    def negative_passive_grammatical_present_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال کامل در وجه دستوری در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_grammatical_present_perfect('دید')
            ['دیده نشده باشم', 'دیده نشده باش', 'دیده نشده باشد', 'دیده نشده باشیم', 'دیده نشده باشید', 'دیده نشده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل در وجه دستوری در حالت مجهول به‌شکل منفی.
        """
        return [
            ri + "ه نشده " + ("باش" if x == "باشی" else x)
            for x in self.perfective_present("باش")
        ]

    def imperfective_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل پایا صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.imperfective_present_perfect('دید')
            ['می‌دیده‌ام', 'می‌دیده‌ای', 'می‌دیده است', 'می‌دیده', 'می‌دیده‌ایم', 'می‌دیده‌اید', 'می‌دیده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل پایا.
        """
        return ["می‌" + x for x in self.present_perfect(ri)]

    def negative_imperfective_present_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال کامل پایا به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_imperfective_present_perfect('دید')
            ['نمی‌دیده‌ام', 'نمی‌دیده‌ای', 'نمی‌دیده است', 'نمی‌دیده', 'نمی‌دیده‌ایم', 'نمی‌دیده‌اید', 'نمی‌دیده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل پایا به‌شکل منفی.
        """
        return ["ن" + x for x in self.imperfective_present_perfect(ri)]

    def subjunctive_imperfective_present_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال کامل پایا در وجه التزامی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.subjunctive_imperfective_present_perfect('دید')
            ['می‌دیده باشم', 'می‌دیده باشی', 'می‌دیده باشد', 'می‌دیده باشیم', 'می‌دیده باشید', 'می‌دیده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل پایا در وجه التزامی.
        """
        return ["می‌" + x for x in self.subjunctive_present_perfect(ri)]

    def negative_subjunctive_imperfective_present_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال کامل پایا در وجه التزامی به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_subjunctive_imperfective_present_perfect('دید')
            ['نمی‌دیده باشم', 'نمی‌دیده باشی', 'نمی‌دیده باشد', 'نمی‌دیده باشیم', 'نمی‌دیده باشید', 'نمی‌دیده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل پایا در وجه التزامی به‌شکل منفی.
        """
        return ["ن" + x for x in self.subjunctive_imperfective_present_perfect(ri)]

    def passive_imperfective_present_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل پایا در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_imperfective_present_perfect('دید')
            ['دیده می‌شده‌ام', 'دیده می‌شده‌ای', 'دیده می‌شده است', 'دیده می‌شده', 'دیده می‌شده‌ایم', 'دیده می‌شده‌اید', 'دیده می‌شده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل پایا در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.imperfective_present_perfect("شد")]

    def negative_passive_imperfective_present_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال کامل پایا در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_imperfective_present_perfect('دید')
            ['دیده نمی‌شده‌ام', 'دیده نمی‌شده‌ای', 'دیده نمی‌شده است', 'دیده نمی‌شده', 'دیده نمی‌شده‌ایم', 'دیده نمی‌شده‌اید', 'دیده نمی‌شده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل پایا در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_imperfective_present_perfect("شد")]

    def passive_subjunctive_imperfective_present_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال کامل پایا در وجه التزامی در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_subjunctive_imperfective_present_perfect('دید')
            ['دیده می‌شده باشم', 'دیده می‌شده باشی', 'دیده می‌شده باشد', 'دیده می‌شده باشیم', 'دیده می‌شده باشید', 'دیده می‌شده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل پایا در وجه التزامی در حالت مجهول.
        """
        return [
            ri + "ه " + x for x in self.subjunctive_imperfective_present_perfect("شد")
        ]

    def negative_passive_subjunctive_imperfective_present_perfect(
        self: "Conjugation",
        ri: str,
    ) -> List[str]:
        """فعل را در زمان حال کامل پایا در وجه التزامی در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_subjunctive_imperfective_present_perfect('دید')
            ['دیده نمی‌شده باشم', 'دیده نمی‌شده باشی', 'دیده نمی‌شده باشد', 'دیده نمی‌شده باشیم', 'دیده نمی‌شده باشید', 'دیده نمی‌شده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل پایا در وجه التزامی در حالت مجهول به‌شکل منفی.
        """
        return [
            ri + "ه " + x
            for x in self.negative_subjunctive_imperfective_present_perfect("شد")
        ]

    def present_perfect_progressive(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل استمراری صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.present_perfect_progressive('دید')
            ['داشته‌ام می‌دیده‌ام', 'داشته‌ای می‌دیده‌ای', 'داشته است می‌دیده است', 'داشته می‌دیده', 'داشته‌ایم می‌دیده‌ایم', 'داشته‌اید می‌دیده‌اید', 'داشته‌اند می‌دیده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل استمراری.
        """
        return [
            x + " " + y
            for x, y in zip(
                self.present_perfect("داشت"),
                self.imperfective_present_perfect(ri),
            )
        ]

    def passive_present_perfect_progressive(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال کامل استمراری در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_present_perfect_progressive('دید')
            ['داشته‌ام دیده می‌شده‌ام', 'داشته‌ای دیده می‌شده‌ای', 'داشته است دیده می‌شده است', 'داشته دیده می‌شده', 'داشته‌ایم دیده می‌شده‌ایم', 'داشته‌اید دیده می‌شده‌اید', 'داشته‌اند دیده می‌شده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال کامل استمراری در حالت مجهول.
        """
        return [
            x + " " + y
            for x, y in zip(
                self.present_perfect("داشت"),
                self.passive_imperfective_present_perfect(ri),
            )
        ]

    def past_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.past_precedent('دید')
            ['دیده بودم', 'دیده بودی', 'دیده بود', 'دیده بودیم', 'دیده بودید', 'دیده بودند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین.
        """
        return [ri + "ه " + x for x in self.perfective_past("بود")]

    def negative_past_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_past_precedent('دید')
            ['ندیده بودم', 'ندیده بودی', 'ندیده بود', 'ندیده بودیم', 'ندیده بودید', 'ندیده بودند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین به‌شکل منفی.
        """
        return ["ن" + x for x in self.past_precedent(ri)]

    def passive_past_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_past_precedent('دید')
            ['دیده شده بودم', 'دیده شده بودی', 'دیده شده بود', 'دیده شده بودیم', 'دیده شده بودید', 'دیده شده بودند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.past_precedent("شد")]

    def negative_passive_past_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_past_precedent('دید')
            ['دیده نشده بودم', 'دیده نشده بودی', 'دیده نشده بود', 'دیده نشده بودیم', 'دیده نشده بودید', 'دیده نشده بودند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_past_precedent("شد")]

    def imperfective_past_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین پایا صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.imperfective_past_precedent('دید')
            ['می‌دیده بودم', 'می‌دیده بودی', 'می‌دیده بود', 'می‌دیده بودیم', 'می‌دیده بودید', 'می‌دیده بودند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین پایا.
        """
        return ["می‌" + x for x in self.past_precedent(ri)]

    def negative_imperfective_past_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین پایا به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_imperfective_past_precedent('دید')
            ['نمی‌دیده بودم', 'نمی‌دیده بودی', 'نمی‌دیده بود', 'نمی‌دیده بودیم', 'نمی‌دیده بودید', 'نمی‌دیده بودند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین پایا به‌شکل منفی.
        """
        return ["ن" + x for x in self.imperfective_past_precedent(ri)]

    def passive_imperfective_past_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین پایا در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_imperfective_past_precedent('دید')
            ['دیده می‌شده بودم', 'دیده می‌شده بودی', 'دیده می‌شده بود', 'دیده می‌شده بودیم', 'دیده می‌شده بودید', 'دیده می‌شده بودند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین پایا در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.imperfective_past_precedent("شد")]

    def negative_passive_imperfective_past_precedent(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین پایا در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_imperfective_past_precedent('دید')
            ['دیده نمی‌شده بودم', 'دیده نمی‌شده بودی', 'دیده نمی‌شده بود', 'دیده نمی‌شده بودیم', 'دیده نمی‌شده بودید', 'دیده نمی‌شده بودند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین پایا در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_imperfective_past_precedent("شد")]

    def past_precedent_progressive(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین استمراری صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.past_precedent_progressive('دید')
            ['داشتم می‌دیده بودم', 'داشتی می‌دیده بودی', 'داشت می‌دیده بود', 'داشتیم می‌دیده بودیم', 'داشتید می‌دیده بودید', 'داشتند می‌دیده بودند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین استمراری.
        """
        return [
            x + " " + y
            for x, y in zip(
                self.perfective_past("داشت"),
                self.imperfective_past_precedent(ri),
            )
        ]

    def passive_past_precedent_progressive(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین استمراری در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_past_precedent_progressive('دید')
            ['داشتم دیده می‌شده بودم', 'داشتی دیده می‌شده بودی', 'داشت دیده می‌شده بود', 'داشتیم دیده می‌شده بودیم', 'داشتید دیده می‌شده بودید', 'داشتند دیده می‌شده بودند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین استمراری در حالت مجهول.
        """
        return [
            x + " " + y
            for x, y in zip(
                self.perfective_past("داشت"),
                self.passive_imperfective_past_precedent(ri),
            )
        ]

    def past_precedent_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.past_precedent_perfect('دید')
            ['دیده بوده‌ام', 'دیده بوده‌ای', 'دیده بوده است', 'دیده بوده', 'دیده بوده‌ایم', 'دیده بوده‌اید', 'دیده بوده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل.
        """
        return [ri + "ه " + x for x in self.present_perfect("بود")]

    def negative_past_precedent_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_past_precedent_perfect('دید')
            ['ندیده بوده‌ام', 'ندیده بوده‌ای', 'ندیده بوده است', 'ندیده بوده', 'ندیده بوده‌ایم', 'ندیده بوده‌اید', 'ندیده بوده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل به‌شکل منفی.
        """
        return ["ن" + x for x in self.past_precedent_perfect(ri)]

    def subjunctive_past_precedent_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل در وجه التزامی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.subjunctive_past_precedent_perfect('دید')
            ['دیده بوده باشم', 'دیده بوده باشی', 'دیده بوده باشد', 'دیده بوده باشیم', 'دیده بوده باشید', 'دیده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل در وجه التزامی.
        """
        return [ri + "ه " + x for x in self.subjunctive_present_perfect("بود")]

    def negative_subjunctive_past_precedent_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل در وجه التزامی به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_subjunctive_past_precedent_perfect('دید')
            ['ندیده بوده باشم', 'ندیده بوده باشی', 'ندیده بوده باشد', 'ندیده بوده باشیم', 'ندیده بوده باشید', 'ندیده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل در وجه التزامی به‌شکل منفی.
        """
        return ["ن" + x for x in self.subjunctive_past_precedent_perfect(ri)]

    def grammatical_past_precedent_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل در وجه دستوری صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.grammatical_past_precedent_perfect('دید')
            ['دیده بوده باشم', 'دیده بوده باش', 'دیده بوده باشد', 'دیده بوده باشیم', 'دیده بوده باشید', 'دیده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل در وجه دستوری.
        """
        return [
            ri + "ه بوده " + ("باش" if x == "باشی" else x)
            for x in self.perfective_present("باش")
        ]

    def negative_grammatical_past_precedent_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل در وجه دستوری به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_grammatical_past_precedent_perfect('دید')
            ['ندیده بوده باشم', 'ندیده بوده باش', 'ندیده بوده باشد', 'ندیده بوده باشیم', 'ندیده بوده باشید', 'ندیده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل در وجه دستوری به‌شکل منفی.
        """
        return ["ن" + x for x in self.grammatical_past_precedent_perfect(ri)]

    def passive_past_precedent_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_past_precedent_perfect('دید')
            ['دیده شده بوده‌ام', 'دیده شده بوده‌ای', 'دیده شده بوده است', 'دیده شده بوده', 'دیده شده بوده‌ایم', 'دیده شده بوده‌اید', 'دیده شده بوده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.past_precedent_perfect("شد")]

    def negative_passive_past_precedent_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_past_precedent_perfect('دید')
            ['دیده نشده بوده‌ام', 'دیده نشده بوده‌ای', 'دیده نشده بوده است', 'دیده نشده بوده', 'دیده نشده بوده‌ایم', 'دیده نشده بوده‌اید', 'دیده نشده بوده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_past_precedent_perfect("شد")]

    def passive_subjunctive_past_precedent_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل در وجه التزامی در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_subjunctive_past_precedent_perfect('دید')
            ['دیده شده بوده باشم', 'دیده شده بوده باشی', 'دیده شده بوده باشد', 'دیده شده بوده باشیم', 'دیده شده بوده باشید', 'دیده شده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل در وجه التزامی در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.subjunctive_past_precedent_perfect("شد")]

    def negative_passive_subjunctive_past_precedent_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل در وجه التزامی در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_subjunctive_past_precedent_perfect('دید')
            ['دیده نشده بوده باشم', 'دیده نشده بوده باشی', 'دیده نشده بوده باشد', 'دیده نشده بوده باشیم', 'دیده نشده بوده باشید', 'دیده نشده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل در وجه التزامی در حالت مجهول به‌شکل منفی.
        """
        return [
            ri + "ه " + "ن" + x for x in self.subjunctive_past_precedent_perfect("شد")
        ]

    def passive_grammatical_past_precedent_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل در وجه دستوری در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_grammatical_past_precedent_perfect('دید')
            ['دیده شده بوده باشم', 'دیده شده بوده باش', 'دیده شده بوده باشد', 'دیده شده بوده باشیم', 'دیده شده بوده باشید', 'دیده شده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل در وجه دستوری در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.grammatical_past_precedent_perfect("شد")]

    def negative_passive_grammatical_past_precedent_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل در وجه دستوری در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_grammatical_past_precedent_perfect('دید')
            ['دیده نشده بوده باشم', 'دیده نشده بوده باش', 'دیده نشده بوده باشد', 'دیده نشده بوده باشیم', 'دیده نشده بوده باشید', 'دیده نشده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل در وجه دستوری در حالت مجهول به‌شکل منفی.
        """
        return [
            ri + "ه " + x
            for x in self.negative_grammatical_past_precedent_perfect("شد")
        ]

    def imperfective_past_precedent_perfect(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل پایا صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.imperfective_past_precedent_perfect('دید')
            ['می‌دیده بوده‌ام', 'می‌دیده بوده‌ای', 'می‌دیده بوده است', 'می‌دیده بوده', 'می‌دیده بوده‌ایم', 'می‌دیده بوده‌اید', 'می‌دیده بوده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل پایا.
        """
        return ["می‌" + x for x in self.past_precedent_perfect(ri)]

    def negative_imperfective_past_precedent_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل پایا به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_imperfective_past_precedent_perfect('دید')
            ['نمی‌دیده بوده‌ام', 'نمی‌دیده بوده‌ای', 'نمی‌دیده بوده است', 'نمی‌دیده بوده', 'نمی‌دیده بوده‌ایم', 'نمی‌دیده بوده‌اید', 'نمی‌دیده بوده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل پایا به‌شکل منفی.
        """
        return ["ن" + x for x in self.imperfective_past_precedent_perfect(ri)]

    def subjunctive_imperfective_past_precedent_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل پایا در وجه التزامی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.subjunctive_imperfective_past_precedent_perfect('دید')
            ['می‌دیده بوده باشم', 'می‌دیده بوده باشی', 'می‌دیده بوده باشد', 'می‌دیده بوده باشیم', 'می‌دیده بوده باشید', 'می‌دیده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل پایا در وجه التزامی.
        """
        return ["می‌" + x for x in self.subjunctive_past_precedent_perfect(ri)]

    def negative_subjunctive_imperfective_past_precedent_perfect(
        self: "Conjugation",
        ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل پایا در وجه التزامی به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_subjunctive_imperfective_past_precedent_perfect('دید')
            ['نمی‌دیده بوده باشم', 'نمی‌دیده بوده باشی', 'نمی‌دیده بوده باشد', 'نمی‌دیده بوده باشیم', 'نمی‌دیده بوده باشید', 'نمی‌دیده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل پایا در وجه التزامی به‌شکل منفی.
        """
        return [
            "ن" + x for x in self.subjunctive_imperfective_past_precedent_perfect(ri)
        ]

    def passive_imperfective_past_precedent_perfect(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل پایا در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_imperfective_past_precedent_perfect('دید')
            ['دیده می‌شده بوده‌ام', 'دیده می‌شده بوده‌ای', 'دیده می‌شده بوده است', 'دیده می‌شده بوده', 'دیده می‌شده بوده‌ایم', 'دیده می‌شده بوده‌اید', 'دیده می‌شده بوده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل پایا در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.imperfective_past_precedent_perfect("شد")]

    def negative_passive_imperfective_past_precedent_perfect(
        self: "Conjugation",
        ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل پایا در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_imperfective_past_precedent_perfect('دید')
            ['دیده نمی‌شده بوده‌ام', 'دیده نمی‌شده بوده‌ای', 'دیده نمی‌شده بوده است', 'دیده نمی‌شده بوده', 'دیده نمی‌شده بوده‌ایم', 'دیده نمی‌شده بوده‌اید', 'دیده نمی‌شده بوده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل پایا در حالت مجهول به‌شکل منفی.
        """
        return [
            ri + "ه " + x
            for x in self.negative_imperfective_past_precedent_perfect("شد")
        ]

    def passive_subjunctive_imperfective_past_precedent_perfect(
        self: "Conjugation",
        ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل پایا در وجه التزامی در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_subjunctive_imperfective_past_precedent_perfect('دید')
            ['دیده می‌شده بوده باشم', 'دیده می‌شده بوده باشی', 'دیده می‌شده بوده باشد', 'دیده می‌شده بوده باشیم', 'دیده می‌شده بوده باشید', 'دیده می‌شده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل پایا در وجه التزامی در حالت مجهول.
        """
        return [
            ri + "ه " + x
            for x in self.subjunctive_imperfective_past_precedent_perfect("شد")
        ]

    def negative_passive_subjunctive_imperfective_past_precedent_perfect(
        self: "Conjugation",
        ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل پایا در وجه التزامی در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_subjunctive_imperfective_past_precedent_perfect('دید')
            ['دیده نمی‌شده بوده باشم', 'دیده نمی‌شده بوده باشی', 'دیده نمی‌شده بوده باشد', 'دیده نمی‌شده بوده باشیم', 'دیده نمی‌شده بوده باشید', 'دیده نمی‌شده بوده باشند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل پایا در وجه التزامی در حالت مجهول به‌شکل منفی.
        """
        return [
            ri + "ه " + "ن" + x
            for x in self.subjunctive_imperfective_past_precedent_perfect("شد")
        ]

    def past_precedent_perfect_progressive(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل استمراری صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.past_precedent_perfect_progressive('دید')
            ['داشته‌ام می‌دیده بوده‌ام', 'داشته‌ای می‌دیده بوده‌ای', 'داشته است می‌دیده بوده است', 'داشته می‌دیده بوده', 'داشته‌ایم می‌دیده بوده‌ایم', 'داشته‌اید می‌دیده بوده‌اید', 'داشته‌اند می‌دیده بوده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل استمراری.
        """
        return [
            x + " " + y
            for x, y in zip(
                self.present_perfect("داشت"),
                self.imperfective_past_precedent_perfect(ri),
            )
        ]

    def passive_past_precedent_perfect_progressive(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان گذشتهٔ پیشین کامل استمراری در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_past_precedent_perfect_progressive('دید')
            ['داشته‌ام دیده می‌شده بوده‌ام', 'داشته‌ای دیده می‌شده بوده‌ای', 'داشته است دیده می‌شده بوده است', 'داشته دیده می‌شده بوده', 'داشته‌ایم دیده می‌شده بوده‌ایم', 'داشته‌اید دیده می‌شده بوده‌اید', 'داشته‌اند دیده می‌شده بوده‌اند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان گذشتهٔ پیشین کامل استمراری در حالت مجهول.
        """
        return [
            x + " " + y
            for x, y in zip(
                self.present_perfect("داشت"),
                self.passive_imperfective_past_precedent_perfect(ri),
            )
        ]

    def perfective_present(self: "Conjugation", rii: str) -> List[str]:
        """فعل را در زمان حال مطلق صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.perfective_present('بین')
            ['بینم', 'بینی', 'بیند', 'بینیم', 'بینید', 'بینند']

        Args:
            rii: بن مضارع فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق.
        """
        return [rii + x for x in ["م", "ی", "د", "یم", "ید", "ند"]]

    def negative_perfective_present(self: "Conjugation", rii: str) -> List[str]:
        """فعل را در زمان حال مطلق به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_perfective_present('بین')
            ['نبینم', 'نبینی', 'نبیند', 'نبینیم', 'نبینید', 'نبینند']

        Args:
            rii: بن مضارع فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق به‌شکل منفی.
        """
        return ["ن" + x for x in self.perfective_present(rii)]

    def subjunctive_perfective_present(self: "Conjugation", rii: str) -> List[str]:
        """فعل را در زمان حال مطلق در وجه التزامی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.subjunctive_perfective_present('بین')
            ['ببینم', 'ببینی', 'ببیند', 'ببینیم', 'ببینید', 'ببینند']

        Args:
            rii: بن مضارع فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق در وجه التزامی.
        """
        return ["ب" + x for x in self.perfective_present(rii)]

    def negative_subjunctive_perfective_present(
        self: "Conjugation", rii: str,
    ) -> List[str]:
        """فعل را در زمان حال مطلق در وجه التزامی به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_subjunctive_perfective_present('بین')
            ['نبینم', 'نبینی', 'نبیند', 'نبینیم', 'نبینید', 'نبینند']

        Args:
            rii: بن مضارع فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق در وجه التزامی به‌شکل منفی.
        """
        return ["ن" + x for x in self.perfective_present(rii)]

    def grammatical_perfective_present(self: "Conjugation", rii: str) -> List[str]:
        """فعل را در زمان حال مطلق در وجه دستوری صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.grammatical_perfective_present('بین')
            ['ببینم', 'ببین', 'ببیند', 'ببینیم', 'ببینید', 'ببینند']

        Args:
            rii: بن مضارع فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق در وجه دستوری.
        """
        return [
            "ببین" if x == "ببینی" else x
            for x in self.subjunctive_perfective_present(rii)
        ]

    def negative_grammatical_perfective_present(
        self: "Conjugation", rii: str,
    ) -> List[str]:
        """فعل را در زمان حال مطلق در وجه دستوری به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_grammatical_perfective_present('بین')
            ['نبینم', 'نبین', 'نبیند', 'نبینیم', 'نبینید', 'نبینند']

        Args:
            rii: بن مضارع فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق در وجه دستوری به‌شکل منفی.
        """
        return [
            "ن" + ("بین" if x == "بینی" else x) for x in self.perfective_present(rii)
        ]

    def passive_perfective_present(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال مطلق در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_perfective_present('دید')
            ['دیده شوم', 'دیده شوی', 'دیده شود', 'دیده شویم', 'دیده شوید', 'دیده شوند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.perfective_present("شو")]

    def negative_passive_perfective_present(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال مطلق در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_perfective_present('دید')
            ['دیده نشوم', 'دیده نشوی', 'دیده نشود', 'دیده نشویم', 'دیده نشوید', 'دیده نشوند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_perfective_present("شو")]

    def passive_subjunctive_perfective_present(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال مطلق در وجه التزامی در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_subjunctive_perfective_present('دید')
            ['دیده بشوم', 'دیده بشوی', 'دیده بشود', 'دیده بشویم', 'دیده بشوید', 'دیده بشوند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق در وجه التزامی در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.subjunctive_perfective_present("شو")]

    def negative_passive_subjunctive_perfective_present(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال مطلق در وجه التزامی در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_subjunctive_perfective_present('دید')
            ['دیده نشوم', 'دیده نشوی', 'دیده نشود', 'دیده نشویم', 'دیده نشوید', 'دیده نشوند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق در وجه التزامی در حالت مجهول به‌شکل منفی.
        """
        return [
            ri + "ه " + x for x in self.negative_subjunctive_perfective_present("شو")
        ]

    def passive_grammatical_perfective_present(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال مطلق در وجه دستوری در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_grammatical_perfective_present('دید')
            ['دیده بشوم', 'دیده بشو', 'دیده بشود', 'دیده بشویم', 'دیده بشوید', 'دیده بشوند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق در وجه دستوری در حالت مجهول.
        """
        return [
            ri + "ه " + ("بشو" if x == "بشوی" else x)
            for x in self.grammatical_perfective_present("شو")
        ]

    def negative_passive_grammatical_perfective_present(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال مطلق در وجه دستوری در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_grammatical_perfective_present('دید')
            ['دیده نشوم', 'دیده نشو', 'دیده نشود', 'دیده نشویم', 'دیده نشوید', 'دیده نشوند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال مطلق در وجه دستوری در حالت مجهول به‌شکل منفی.
        """
        return [
            ri + "ه " + ("نشو" if x == "نشوی" else x)
            for x in self.negative_grammatical_perfective_present("شو")
        ]

    def imperfective_present(self: "Conjugation", rii: str) -> List[str]:
        """فعل را در زمان حال پایا صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.imperfective_present('بین')
            ['می‌بینم', 'می‌بینی', 'می‌بیند', 'می‌بینیم', 'می‌بینید', 'می‌بینند']

        Args:
            rii: بن مضارع فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال پایا.
        """
        return ["می‌" + x for x in self.perfective_present(rii)]

    def negative_imperfective_present(self: "Conjugation", rii: str) -> List[str]:
        """فعل را در زمان حال پایا به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_imperfective_present('بین')
            ['نمی‌بینم', 'نمی‌بینی', 'نمی‌بیند', 'نمی‌بینیم', 'نمی‌بینید', 'نمی‌بینند']

        Args:
            rii: بن مضارع فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال پایا به‌شکل منفی.
        """
        return ["ن" + x for x in self.imperfective_present(rii)]

    def passive_imperfective_present(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال پایا در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_imperfective_present('دید')
            ['دیده می‌شوم', 'دیده می‌شوی', 'دیده می‌شود', 'دیده می‌شویم', 'دیده می‌شوید', 'دیده می‌شوند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال پایا در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.imperfective_present("شو")]

    def negative_passive_imperfective_present(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان حال پایا در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_imperfective_present('دید')
            ['دیده نمی‌شوم', 'دیده نمی‌شوی', 'دیده نمی‌شود', 'دیده نمی‌شویم', 'دیده نمی‌شوید', 'دیده نمی‌شوند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال پایا در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_imperfective_present("شو")]

    def present_progressive(self: "Conjugation", rii: str) -> List[str]:
        """فعل را در زمان حال استمراری صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.present_progressive('بین')
            ['دارم می‌بینم', 'داری می‌بینی', 'دارد می‌بیند', 'داریم می‌بینیم', 'دارید می‌بینید', 'دارند می‌بینند']

        Args:
            rii: بن مضارع فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال استمراری.
        """
        return [
            x + " " + y
            for x, y in zip(
                self.perfective_present("دار"),
                self.imperfective_present(rii),
            )
        ]

    def passive_present_progressive(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان حال استمراری در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_present_progressive('دید')
            ['دارم دیده می‌شوم', 'داری دیده می‌شوی', 'دارد دیده می‌شود', 'داریم دیده می‌شویم', 'دارید دیده می‌شوید', 'دارند دیده می‌شوند']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان حال استمراری در حالت مجهول.
        """
        return [
            x + " " + y
            for x, y in zip(
                self.perfective_present("دار"),
                self.passive_imperfective_present(ri),
            )
        ]

    def perfective_future(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ مطلق صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.perfective_future('دید')
            ['خواهم دید', 'خواهی دید', 'خواهد دید', 'خواهیم دید', 'خواهید دید', 'خواهند دید']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ مطلق.
        """
        return [x + " " + ri for x in self.perfective_present("خواه")]

    def negative_perfective_future(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ مطلق به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_perfective_future('دید')
            ['نخواهم دید', 'نخواهی دید', 'نخواهد دید', 'نخواهیم دید', 'نخواهید دید', 'نخواهند دید']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ مطلق به‌شکل منفی.
        """
        return ["ن" + x for x in self.perfective_future(ri)]

    def passive_perfective_future(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ مطلق در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_perfective_future('دید')
            ['دیده خواهم شد', 'دیده خواهی شد', 'دیده خواهد شد', 'دیده خواهیم شد', 'دیده خواهید شد', 'دیده خواهند شد']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ مطلق در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.perfective_future("شد")]

    def negative_passive_perfective_future(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ مطلق در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_perfective_future('دید')
            ['دیده نخواهم شد', 'دیده نخواهی شد', 'دیده نخواهد شد', 'دیده نخواهیم شد', 'دیده نخواهید شد', 'دیده نخواهند شد']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ مطلق در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_perfective_future("شد")]

    def imperfective_future(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ پایا صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.imperfective_future('دید')
            ['می‌خواهم دید', 'می‌خواهی دید', 'می‌خواهد دید', 'می‌خواهیم دید', 'می‌خواهید دید', 'می‌خواهند دید']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پایا.
        """
        return ["می‌" + x for x in self.perfective_future(ri)]

    def negative_imperfective_future(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ پایا به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_imperfective_future('دید')
            ['نمی‌خواهم دید', 'نمی‌خواهی دید', 'نمی‌خواهد دید', 'نمی‌خواهیم دید', 'نمی‌خواهید دید', 'نمی‌خواهند دید']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پایا به‌شکل منفی.
        """
        return ["ن" + x for x in self.imperfective_future(ri)]

    def passive_imperfective_future(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ پایا در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_imperfective_future('دید')
            ['دیده می‌خواهم شد', 'دیده می‌خواهی شد', 'دیده می‌خواهد شد', 'دیده می‌خواهیم شد', 'دیده می‌خواهید شد', 'دیده می‌خواهند شد']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پایا در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.imperfective_future("شد")]

    def negative_passive_imperfective_future(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ پایا در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_imperfective_future('دید')
            ['دیده نمی‌خواهم شد', 'دیده نمی‌خواهی شد', 'دیده نمی‌خواهد شد', 'دیده نمی‌خواهیم شد', 'دیده نمی‌خواهید شد', 'دیده نمی‌خواهند شد']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پایا در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_imperfective_future("شد")]

    def future_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ پیشین صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.future_precedent('دید')
            ['دیده خواهم بود', 'دیده خواهی بود', 'دیده خواهد بود', 'دیده خواهیم بود', 'دیده خواهید بود', 'دیده خواهند بود']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پیشین.
        """
        return [ri + "ه " + x for x in self.perfective_future("بود")]

    def negative_future_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ پیشین به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_future_precedent('دید')
            ['ندیده خواهم بود', 'ندیده خواهی بود', 'ندیده خواهد بود', 'ندیده خواهیم بود', 'ندیده خواهید بود', 'ندیده خواهند بود']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پیشین به‌شکل منفی.
        """
        return ["ن" + x for x in self.future_precedent(ri)]

    def passive_future_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ پیشین در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_future_precedent('دید')
            ['دیده شده خواهم بود', 'دیده شده خواهی بود', 'دیده شده خواهد بود', 'دیده شده خواهیم بود', 'دیده شده خواهید بود', 'دیده شده خواهند بود']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پیشین در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.future_precedent("شد")]

    def negative_passive_future_precedent(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ پیشین در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_future_precedent('دید')
            ['دیده نشده خواهم بود', 'دیده نشده خواهی بود', 'دیده نشده خواهد بود', 'دیده نشده خواهیم بود', 'دیده نشده خواهید بود', 'دیده نشده خواهند بود']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پیشین در حالت مجهول به‌شکل منفی.
        """
        return [ri + "ه " + x for x in self.negative_future_precedent("شد")]

    def future_precedent_imperfective(self: "Conjugation", ri: str) -> List[str]:
        """فعل را در زمان آیندهٔ پیشین پایا صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.future_precedent_imperfective('دید')
            ['می‌دیده خواهم بود', 'می‌دیده خواهی بود', 'می‌دیده خواهد بود', 'می‌دیده خواهیم بود', 'می‌دیده خواهید بود', 'می‌دیده خواهند بود']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پیشین پایا.
        """
        return ["می‌" + x for x in self.future_precedent(ri)]

    def negative_future_precedent_imperfective(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان آیندهٔ پیشین پایا به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_future_precedent_imperfective('دید')
            ['نمی‌دیده خواهم بود', 'نمی‌دیده خواهی بود', 'نمی‌دیده خواهد بود', 'نمی‌دیده خواهیم بود', 'نمی‌دیده خواهید بود', 'نمی‌دیده خواهند بود']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پیشین پایا به‌شکل منفی.
        """
        return ["ن" + x for x in self.future_precedent_imperfective(ri)]

    def passive_future_precedent_imperfective(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان آیندهٔ پیشین پایا در حالت مجهول صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.passive_future_precedent_imperfective('دید')
            ['دیده می‌شده خواهم بود', 'دیده می‌شده خواهی بود', 'دیده می‌شده خواهد بود', 'دیده می‌شده خواهیم بود', 'دیده می‌شده خواهید بود', 'دیده می‌شده خواهند بود']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پیشین پایا در حالت مجهول.
        """
        return [ri + "ه " + x for x in self.future_precedent_imperfective("شد")]

    def negative_passive_future_precedent_imperfective(
        self: "Conjugation", ri: str,
    ) -> List[str]:
        """فعل را در زمان آیندهٔ پیشین پایا در حالت مجهول به‌شکل منفی صرف می‌کند.

        Examples:
            >>> conj = Conjugation()
            >>> conj.negative_passive_future_precedent_imperfective('دید')
            ['دیده نمی‌شده خواهم بود', 'دیده نمی‌شده خواهی بود', 'دیده نمی‌شده خواهد بود', 'دیده نمی‌شده خواهیم بود', 'دیده نمی‌شده خواهید بود', 'دیده نمی‌شده خواهند بود']

        Args:
            ri: بن ماضی فعل.

        Returns:
             صورت‌های صرفی فعل در زمان آیندهٔ پیشین پایا در حالت مجهول به‌شکل منفی.
        """
        return [
            ri + "ه " + x for x in self.negative_future_precedent_imperfective("شد")
        ]

    def get(self: "Conjugation", verb, negative=False, passive=False) -> List[str]:
        """صورت‌های صرفی فعل را برمی‌گرداند.

        Args:
            verb (str): فعلی که باید صرف شود. به‌صورت بن ماضی#بن مضارع؛ مانند: دید#بین.
            negative (bool, optional): اگر `True` باشد صورت‌های صرفی منفی را برمی‌گرداند.
            passive (bool, optional): اگر `True` باشد صورت‌های صرفی مجهول را برمی‌گرداند.

        Returns:
            (List(str)): صورت‌های صرفی فعل.
        """
        ri, rii = verb.split("#")
        infinitive = [ri + "ن"]
        result = [infinitive]

        if negative and passive:
            result.append(self.negative_passive_perfective_past(ri))
            result.append(self.negative_passive_imperfective_past(ri))
            result.append(self.negative_passive_present_perfect(ri))
            result.append(self.negative_passive_subjunctive_present_perfect(ri))
            result.append(self.negative_passive_grammatical_present_perfect(ri))
            result.append(self.negative_passive_imperfective_present_perfect(ri))
            result.append(
                self.negative_passive_subjunctive_imperfective_present_perfect(ri),
            )
            result.append(self.negative_passive_past_precedent(ri))
            result.append(self.negative_passive_imperfective_past_precedent(ri))
            result.append(self.negative_passive_past_precedent_perfect(ri))
            result.append(self.negative_passive_subjunctive_past_precedent_perfect(ri))
            result.append(self.negative_passive_grammatical_past_precedent_perfect(ri))
            result.append(self.negative_passive_imperfective_past_precedent_perfect(ri))
            result.append(
                self.negative_passive_subjunctive_imperfective_past_precedent_perfect(
                    ri,
                ),
            )
            result.append(self.negative_passive_perfective_present(ri))
            result.append(self.negative_passive_subjunctive_perfective_present(ri))
            result.append(self.negative_passive_grammatical_perfective_present(ri))
            result.append(self.negative_passive_imperfective_present(ri))
            result.append(self.negative_passive_perfective_future(ri))
            result.append(self.negative_passive_imperfective_future(ri))
            result.append(self.negative_passive_future_precedent(ri))
            result.append(self.negative_passive_future_precedent_imperfective(ri))

        elif passive and not negative:
            result.append(self.passive_perfective_past(ri))
            result.append(self.passive_imperfective_past(ri))
            result.append(self.passive_past_progresive(ri))
            result.append(self.passive_present_perfect(ri))
            result.append(self.passive_subjunctive_present_perfect(ri))
            result.append(self.passive_grammatical_present_perfect(ri))
            result.append(self.passive_imperfective_present_perfect(ri))
            result.append(self.passive_subjunctive_imperfective_present_perfect(ri))
            result.append(self.passive_present_perfect_progressive(ri))
            result.append(self.passive_past_precedent(ri))
            result.append(self.passive_imperfective_past_precedent(ri))
            result.append(self.passive_past_precedent_progressive(ri))
            result.append(self.passive_past_precedent_perfect(ri))
            result.append(self.passive_subjunctive_past_precedent_perfect(ri))
            result.append(self.passive_grammatical_past_precedent_perfect(ri))
            result.append(self.passive_imperfective_past_precedent_perfect(ri))
            result.append(
                self.passive_subjunctive_imperfective_past_precedent_perfect(ri),
            )
            result.append(self.passive_past_precedent_perfect_progressive(ri))
            result.append(self.passive_perfective_present(ri))
            result.append(self.passive_subjunctive_perfective_present(ri))
            result.append(self.passive_grammatical_perfective_present(ri))
            result.append(self.passive_imperfective_present(ri))
            result.append(self.passive_present_progressive(ri))
            result.append(self.passive_perfective_future(ri))
            result.append(self.passive_imperfective_future(ri))
            result.append(self.passive_future_precedent(ri))
            result.append(self.passive_future_precedent_imperfective(ri))

        elif negative and not passive:
            result.append(self.negative_perfective_past(ri))
            result.append(self.negative_imperfective_past(ri))
            result.append(self.negative_present_perfect(ri))
            result.append(self.negative_subjunctive_present_perfect(ri))
            result.append(self.negative_grammatical_present_perfect(ri))
            result.append(self.negative_imperfective_present_perfect(ri))
            result.append(self.negative_subjunctive_imperfective_present_perfect(ri))
            result.append(self.negative_past_precedent(ri))
            result.append(self.negative_imperfective_past_precedent(ri))
            result.append(self.negative_past_precedent_perfect(ri))
            result.append(self.negative_subjunctive_past_precedent_perfect(ri))
            result.append(self.negative_grammatical_past_precedent_perfect(ri))
            result.append(self.negative_imperfective_past_precedent_perfect(ri))
            result.append(
                self.negative_subjunctive_imperfective_past_precedent_perfect(ri),
            )
            result.append(self.negative_perfective_present(rii))
            result.append(self.negative_subjunctive_perfective_present(rii))
            result.append(self.negative_grammatical_perfective_present(rii))
            result.append(self.negative_imperfective_present(rii))
            result.append(self.negative_perfective_future(ri))
            result.append(self.negative_imperfective_future(ri))
            result.append(self.negative_future_precedent(ri))
            result.append(self.negative_future_precedent_imperfective(ri))

        elif not negative and not passive:
            result.append(self.perfective_past(ri))
            result.append(self.imperfective_past(ri))
            result.append(self.past_progresive(ri))
            result.append(self.present_perfect(ri))
            result.append(self.subjunctive_present_perfect(ri))
            result.append(self.grammatical_present_perfect(ri))
            result.append(self.imperfective_present_perfect(ri))
            result.append(self.subjunctive_imperfective_present_perfect(ri))
            result.append(self.present_perfect_progressive(ri))
            result.append(self.past_precedent(ri))
            result.append(self.imperfective_past_precedent(ri))
            result.append(self.past_precedent_progressive(ri))
            result.append(self.past_precedent_perfect(ri))
            result.append(self.subjunctive_past_precedent_perfect(ri))
            result.append(self.grammatical_past_precedent_perfect(ri))
            result.append(self.imperfective_past_precedent_perfect(ri))
            result.append(self.subjunctive_imperfective_past_precedent_perfect(ri))
            result.append(self.past_precedent_perfect_progressive(ri))
            result.append(self.perfective_present(rii))
            result.append(self.subjunctive_perfective_present(rii))
            result.append(self.grammatical_perfective_present(rii))
            result.append(self.imperfective_present(rii))
            result.append(self.present_progressive(rii))
            result.append(self.perfective_future(ri))
            result.append(self.imperfective_future(ri))
            result.append(self.future_precedent(ri))
            result.append(self.future_precedent_imperfective(ri))

        return sum(result, [])

    def get_all(self: "Conjugation", verb: str) -> List[str]:
        """تمام صورت‌های صرفی فعل را در وجوه اخباری، التزامی، دستوری و در اشکال منفی و مثبت و مجهول برمی‌گرداند.

        Args:
            verb (str): فعلی که باید صرف شود. به‌صورت بن ماضی#بن مضارع؛ مانند: دید#بین.

        Returns:
             لیست تمام صورت‌های صرفی فعل.
        """
        ri, rii = verb.split("#")
        infinitive = [ri + "ن"]
        result = [infinitive]

        # گذشتهٔ مطلق
        result.append(self.perfective_past(ri))

        # گذشتهٔ مطلق منفی
        result.append(self.negative_perfective_past(ri))

        # گذشتهٔ مطلق مجهول
        result.append(self.passive_perfective_past(ri))

        # گذشتهٔ مطلق مجهول منفی
        result.append(self.negative_passive_perfective_past(ri))

        # گذشتهٔ پایا
        result.append(self.imperfective_past(ri))

        # گذشتهٔ پایای منفی
        result.append(self.negative_imperfective_past(ri))

        # گذشتهٔ پایای مجهول
        result.append(self.passive_imperfective_past(ri))

        # گذشتهٔ پایای مجهول منفی
        result.append(self.negative_passive_imperfective_past(ri))

        # گذشتهٔ استمراری
        result.append(self.past_progresive(ri))

        # گذشتهٔ استمراری مجهول
        result.append(self.passive_past_progresive(ri))

        # حال کامل
        result.append(self.present_perfect(ri))

        # حال کامل منفی
        result.append(self.negative_present_perfect(ri))

        # حال کامل التزامی
        result.append(self.subjunctive_present_perfect(ri))

        # حال کامل التزامی منفی
        result.append(self.negative_subjunctive_present_perfect(ri))

        # حال کامل دستوری
        result.append(self.grammatical_present_perfect(ri))

        # حال کامل دستوری منفی
        result.append(self.negative_grammatical_present_perfect(ri))

        # حال کامل مجهول
        result.append(self.passive_present_perfect(ri))

        # حال کامل مجهول منفی
        result.append(self.negative_passive_present_perfect(ri))

        # حال کامل التزامی مجهول
        result.append(self.passive_subjunctive_present_perfect(ri))

        # حال کامل التزامی مجهول منفی
        result.append(self.negative_passive_subjunctive_present_perfect(ri))

        # حال کامل دستوری مجهول
        result.append(self.passive_grammatical_present_perfect(ri))

        # حال کامل دستوری مجهول منفی
        result.append(self.negative_passive_grammatical_present_perfect(ri))

        # حال کامل پایا
        result.append(self.imperfective_present_perfect(ri))

        # حال کامل پایای منفی
        result.append(self.negative_imperfective_present_perfect(ri))

        # حال کامل پایای التزامی
        result.append(self.subjunctive_imperfective_present_perfect(ri))

        # حال کامل پایای التزامی منفی
        result.append(self.negative_subjunctive_imperfective_present_perfect(ri))

        # حال کامل پایای مجهول
        result.append(self.passive_imperfective_present_perfect(ri))

        # حال کامل پایای مجهول منفی
        result.append(self.negative_passive_imperfective_present_perfect(ri))

        # حال کامل پایای التزامی مجهول
        result.append(self.passive_subjunctive_imperfective_present_perfect(ri))

        # حال کامل پایای التزامی مجهول منفی
        result.append(
            self.negative_passive_subjunctive_imperfective_present_perfect(ri),
        )

        # حال کامل استمراری
        result.append(self.present_perfect_progressive(ri))

        # حال کامل استمراری مجهول
        result.append(self.passive_present_perfect_progressive(ri))

        # گذشتهٔ پیشین
        result.append(self.past_precedent(ri))

        # گذشتهٔ پیشین منفی
        result.append(self.negative_past_precedent(ri))

        # گذشتهٔ پیشین مجهول
        result.append(self.passive_past_precedent(ri))

        # گذشتهٔ پیشین مجهول منفی
        result.append(self.negative_passive_past_precedent(ri))

        # گذشتهٔ پیشین پایا
        result.append(self.imperfective_past_precedent(ri))

        # گذشتهٔ پیشین پایای منفی
        result.append(self.negative_imperfective_past_precedent(ri))

        # گذشتهٔ پیشین پایای مجهول
        result.append(self.passive_imperfective_past_precedent(ri))

        # گذشتهٔ پیشین پایای مجهول منفی
        result.append(self.negative_passive_imperfective_past_precedent(ri))

        # گذشتهٔ پیشین استمراری
        result.append(self.past_precedent_progressive(ri))

        # گذشتهٔ پیشین استمراری مجهول
        result.append(self.passive_past_precedent_progressive(ri))

        # گذشتهٔ پیشین کامل
        result.append(self.past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل منفی
        result.append(self.negative_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل التزامی
        result.append(self.subjunctive_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل التزامی منفی
        result.append(self.negative_subjunctive_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل دستوری
        result.append(self.grammatical_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل دستوری منفی
        result.append(self.negative_grammatical_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل مجهول
        result.append(self.passive_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل مجهول منفی
        result.append(self.negative_passive_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل التزامی مجهول
        result.append(self.passive_subjunctive_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل التزامی مجهول منفی
        result.append(self.negative_passive_subjunctive_past_precedent_perfect(ri))

        # گذشتهٔ پیشن کامل دستوری مجهول
        result.append(self.passive_grammatical_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل دستوری مجهول منفی
        result.append(self.negative_passive_grammatical_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل پایا
        result.append(self.imperfective_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل پایای منفی
        result.append(self.negative_imperfective_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل پایای التزامی
        result.append(self.subjunctive_imperfective_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل پایای التزامی منفی
        result.append(self.negative_subjunctive_imperfective_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل پایای مجهول
        result.append(self.passive_imperfective_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل پایای مجهول منفی
        result.append(self.negative_passive_imperfective_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل پایای التزامی مجهول
        result.append(self.passive_subjunctive_imperfective_past_precedent_perfect(ri))

        # گذشتهٔ پیشین کامل پایای التزامی مجهول منفی
        result.append(
            self.negative_passive_subjunctive_imperfective_past_precedent_perfect(ri),
        )

        # گذشتهٔ پیشین کامل استمراری
        result.append(self.past_precedent_perfect_progressive(ri))

        # گذشتهٔ پیشین کامل استمراری مجهول
        result.append(self.passive_past_precedent_perfect_progressive(ri))

        # حال مطلق
        result.append(self.perfective_present(rii))

        # حال مطلق منفی
        result.append(self.negative_perfective_present(rii))

        # حال مطلق التزامی
        result.append(self.subjunctive_perfective_present(rii))

        # حال مطلق التزامی منفی
        result.append(self.negative_subjunctive_perfective_present(rii))

        # حال مطلق دستوری
        result.append(self.grammatical_perfective_present(rii))

        # حال مطلق دستوری منفی
        result.append(self.negative_grammatical_perfective_present(rii))

        # حال مطلق مجهول
        result.append(self.passive_perfective_present(ri))

        # حال مطلق مجهول منفی
        result.append(self.negative_passive_perfective_present(ri))

        # حال مطلق التزامی مجهول
        result.append(self.passive_subjunctive_perfective_present(ri))

        # حال مطلق التزامی مجهول منفی
        result.append(self.negative_passive_subjunctive_perfective_present(ri))

        # حال مطلق دستوری مجهول
        result.append(self.passive_grammatical_perfective_present(ri))

        # حال مطلق دستوری مجهول منفی
        result.append(self.negative_passive_grammatical_perfective_present(ri))

        # حال پایا
        result.append(self.imperfective_present(rii))

        # حال پایای منفی
        result.append(self.negative_imperfective_present(rii))

        # حال پایای مجهول
        result.append(self.passive_imperfective_present(ri))

        # حال پایای مجهول منفی
        result.append(self.negative_passive_imperfective_present(ri))

        # حال استمراری
        result.append(self.present_progressive(rii))

        # حال استمراری مجهول
        result.append(self.passive_present_progressive(ri))

        # آیندهٔ مطلق
        result.append(self.perfective_future(ri))

        # آیندهٔ مطلق منفی
        result.append(self.negative_perfective_future(ri))

        # آیندهٔ مطلق مجهول
        result.append(self.passive_perfective_future(ri))

        # آیندهٔ مطلق مجهول منفی
        result.append(self.negative_passive_perfective_future(ri))

        # آیندهٔ پایا
        result.append(self.imperfective_future(ri))

        # آیندهٔ پایای منفی
        result.append(self.negative_imperfective_future(ri))

        # آیندهٔ پایای مجهول
        result.append(self.passive_imperfective_future(ri))

        # آیندهٔ پایای مجهول منفی
        result.append(self.negative_passive_imperfective_future(ri))

        # آیندهٔ پیشین
        result.append(self.future_precedent(ri))

        # آیندهٔ پیشین منفی
        result.append(self.negative_future_precedent(ri))

        # آیندهٔ پیشین مجهول
        result.append(self.passive_future_precedent(ri))

        # آیندهٔ پیشین مجهول منفی
        result.append(self.negative_passive_future_precedent(ri))

        # آیندهٔ پیشین پایا
        result.append(self.future_precedent_imperfective(ri))

        # آیندهٔ پیشین پایای منفی
        result.append(self.negative_future_precedent_imperfective(ri))

        # آیندهٔ پیشین پایای مجهول
        result.append(self.passive_future_precedent_imperfective(ri))

        # آیندهٔ پیشین پایای مجهول منفی
        result.append(self.negative_passive_future_precedent_imperfective(ri))

        return sum(result, [])
