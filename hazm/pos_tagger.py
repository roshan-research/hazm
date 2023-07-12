"""این ماژول شامل کلاس‌ها و توابعی برای برچسب‌گذاری توکن‌هاست.

 **میزان دقت
برچسب‌زنی در نسخهٔ حاضر ۹۸.۸ درصد [^1] است.**
[^1]:
این عدد با انتشار هر نسخه بروزرسانی می‌شود.

"""

from nltk.tag import stanford

from hazm import SequenceTagger

punctuation_list = [
    '"',
    "#",
    "(",
    ")",
    "*",
    ",",
    "-",
    ".",
    "/",
    ":",
    "[",
    "]",
    "«",
    "»",
    "،",
    ";",
    "?",
    "!",
]


class POSTagger(SequenceTagger):
    """این کلاس‌ها شامل توابعی برای برچسب‌گذاری توکن‌هاست. **میزان دقت برچسب‌زنی در
    نسخهٔ حاضر ۹۸.۸ درصد [^1] است.** این کلاس تمام توابع خود را از کلاس
    [SequenceTagger][hazm.sequence_tagger.SequenceTagger] به ارث می‌برد.
    [^1]:
    این عدد با انتشار هر نسخه بروزرسانی می‌شود.

    """

    def __init__(
        self: "POSTagger", model=None, data_maker=None, universal_tag=False,
    ) -> None:
        data_maker = self.data_maker if data_maker is None else data_maker
        self.__is_universal = universal_tag
        super().__init__(model, data_maker)

    def __universal_converter(self: "POSTagger", tagged_list):
        return [(word, tag.split(",")[0]) for word, tag in tagged_list]

    def __is_punc(self: "POSTagger", word):
        return word in punctuation_list

    def data_maker(self: "POSTagger", tokens):
        """تابعی که لیستی از لیستی از کلمات توکنایز شده را گرفته و لیست دو بعدی از از دیکشنری‌هایی که تعیین‌کننده ویژگی‌ها هر کلمه هستند را برمی‌گرداند.

        Examples:
            >>> posTagger = POSTagger(model = 'pos_tagger.model')
            >>> posTagger.data_maker(tokens = [['دلم', 'اینجا', 'مانده‌است', '.']])
            [[{'word': 'دلم', 'is_first': True, 'is_last': False, 'prefix-1': 'د', 'prefix-2': 'دل', 'prefix-3': 'دلم', 'suffix-1': 'م', 'suffix-2': 'لم', 'suffix-3': 'دلم', 'prev_word': '', 'two_prev_word': '', 'next_word': 'اینجا', 'two_next_word': 'مانده\u200cاست', 'is_numeric': False, 'prev_is_numeric': '', 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': '', 'next_is_punc': False}, {'word': 'اینجا', 'is_first': False, 'is_last': False, 'prefix-1': 'ا', 'prefix-2': 'ای', 'prefix-3': 'این', 'suffix-1': 'ا', 'suffix-2': 'جا', 'suffix-3': 'نجا', 'prev_word': 'دلم', 'two_prev_word': '.', 'next_word': 'مانده\u200cاست', 'two_next_word': '.', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': False}, {'word': 'مانده\u200cاست', 'is_first': False, 'is_last': False, 'prefix-1': 'م', 'prefix-2': 'ما', 'prefix-3': 'مان', 'suffix-1': 'ت', 'suffix-2': 'ست', 'suffix-3': 'است', 'prev_word': 'اینجا', 'two_prev_word': 'دلم', 'next_word': '.', 'two_next_word': '', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': True}, {'word': '.', 'is_first': False, 'is_last': True, 'prefix-1': '.', 'prefix-2': '.', 'prefix-3': '.', 'suffix-1': '.', 'suffix-2': '.', 'suffix-3': '.', 'prev_word': 'مانده\u200cاست', 'two_prev_word': 'اینجا', 'next_word': '', 'two_next_word': '', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': '', 'is_punc': True, 'prev_is_punc': False, 'next_is_punc': ''}]]

        Args:
            tokens (List[List[str]]): جملاتی که نیاز به تبدیل آن به برداری از ویژگی‌ها است.

        Returns:
            List(List(Dict())): لیستی از لیستی از دیکشنری‌های بیان‌کننده ویژگی‌های یک کلمه.
        """
        return [
            [self.features(token, index) for index in range(len(token))]
            for token in tokens
        ]

    def features(self: "POSTagger", sentence, index):
        """features."""
        return {
            "word": sentence[index],
            "is_first": index == 0,
            "is_last": index == len(sentence) - 1,
            # *ix
            "prefix-1": sentence[index][0],
            "prefix-2": sentence[index][:2],
            "prefix-3": sentence[index][:3],
            "suffix-1": sentence[index][-1],
            "suffix-2": sentence[index][-2:],
            "suffix-3": sentence[index][-3:],
            # word
            "prev_word": "" if index == 0 else sentence[index - 1],
            "two_prev_word": "" if index == 0 else sentence[index - 2],
            "next_word": "" if index == len(sentence) - 1 else sentence[index + 1],
            "two_next_word": (
                ""
                if (index == len(sentence) - 1 or index == len(sentence) - 2)
                else sentence[index + 2]
            ),
            # digit
            "is_numeric": sentence[index].isdigit(),
            "prev_is_numeric": "" if index == 0 else sentence[index - 1].isdigit(),
            "next_is_numeric": (
                "" if index == len(sentence) - 1 else sentence[index + 1].isdigit()
            ),
            # punc
            "is_punc": self.__is_punc(sentence[index]),
            "prev_is_punc": "" if index == 0 else self.__is_punc(sentence[index - 1]),
            "next_is_punc": (
                ""
                if index == len(sentence) - 1
                else self.__is_punc(sentence[index + 1])
            ),
        }

    def tag(self: "POSTagger", tokens):
        """یک جمله را در قالب لیستی از توکن‌ها دریافت می‌کند و در خروجی لیستی از
        `(توکن، برچسب)`ها برمی‌گرداند.

        Examples:
            >>> posTagger = POSTagger(model = 'pos_tagger.model')
            >>> posTagger.tag(tokens = ['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.'])
            [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]

            >>> posTagger = POSTagger(model = 'pos_tagger.model', universal_tag = True)
            >>> posTagger.tag(tokens = ['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.'])
            [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]

        Args:
            tokens (List[str]): لیستی از توکن‌های یک جمله که باید برچسب‌گذاری شود.

        Returns:
            (List[Tuple[str,str]]): ‌لیستی از `(توکن، برچسب)`ها.

        """
        tagged_token = super().tag(tokens)
        return (
            self.__universal_converter(tagged_token)
            if self.__is_universal
            else tagged_token
        )

    def tag_sents(self: "POSTagger", sentences):
        """جملات را در قالب لیستی از توکن‌ها دریافت می‌کند
        و در خروجی، لیستی از لیستی از `(توکن، برچسب)`ها برمی‌گرداند.

        هر لیست از `(توکن، برچسب)`ها مربوط به یک جمله است.

        Examples:
            >>> posTagger = POSTagger(model = 'pos_tagger.model')
            >>> posTagger.tag_sents(sentences = [['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.']])
            [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]]

            >>> posTagger = POSTagger(model = 'pos_tagger.model', universal_tag = True)
            >>> posTagger.tag_sents(sentences = [['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.']])
            [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]]

        Args:
            sentences (List[List[str]]): لیستی از جملات که باید برچسب‌گذاری شود.

        Returns:
            (List[List[Tuple[str,str]]]): لیستی از لیستی از `(توکن، برچسب)`ها.
                    هر لیست از `(توکن،برچسب)`ها مربوط به یک جمله است.

        """
        tagged_sents = super().tag_sents(sentences)
        return (
            [self.__universal_converter(tagged_sent) for tagged_sent in tagged_sents]
            if self.__is_universal
            else tagged_sents
        )


class StanfordPOSTagger(stanford.StanfordPOSTagger):
    """StanfordPOSTagger."""

    def __init__(
        self: "StanfordPOSTagger",
        model_filename: "str",
        path_to_jar: str,
        *args, # noqa: ANN002
        **kwargs, # noqa: ANN003
    ) -> None:
        self._SEPARATOR = "/"
        super(stanford.StanfordPOSTagger, self).__init__(
            model_filename=model_filename,
            path_to_jar=path_to_jar,
            *args,  # noqa: B026
            **kwargs,
        )

    def tag(self: "StanfordPOSTagger", tokens):
        """tag.

        Examples:
            >>> tagger = StanfordPOSTagger(model_filename='persian.tagger', path_to_jar='stanford_postagger.jar')
            >>> tagger.tag(['من', 'به', 'مدرسه', 'رفته_بودم', '.'])
            [('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]

        """
        return self.tag_sents([tokens])[0]

    def tag_sents(self: "StanfordPOSTagger", sentences):
        """tag_sents."""
        refined = ([w.replace(" ", "_") for w in s] for s in sentences)
        return super(stanford.StanfordPOSTagger, self).tag_sents(refined)
