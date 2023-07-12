# ruff: noqa: EXE002
"""این ماژول شامل کلاس‌ها و توابعی برای تجزیهٔ متن به عبارات اسمی، فعلی و حرف
اضافه‌ای است. **میزان دقت تجزیه‌گر سطحی در نسخهٔ حاضر ۹۳.۴ درصد [^1] است.**
[^1]:
این عدد با انتشار هر نسخه بروزرسانی می‌شود.

"""

from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from nltk.chunk import RegexpParser
from nltk.chunk import conlltags2tree
from nltk.chunk import tree2conlltags

from hazm import IOBTagger
from hazm import POSTagger


def tree2brackets(tree: str) -> str:
    """خروجی درختی تابع [parse()][hazm.chunker.Chunker.parse] را به یک ساختار
    کروشه‌ای تبدیل می‌کند.

    Examples:
        >>> chunker = Chunker(model='chunker.model')
        >>> tree=chunker.parse([('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')])
        >>> print(tree)
        (S
          (NP نامه/NOUN,EZ ایشان/PRON)
          (POSTP را/ADP)
          (VP دریافت/NOUN داشتم/VERB)
          ./PUNCT)

        >>> tree2brackets(tree)
        '[نامه ایشان NP] [را POSTP] [دریافت داشتم VP] .'

    Args:
        tree: ساختار درختی حاصل از پردزاش تابع parse()

    Returns:
        رشته‌ای از کروشه‌ها که در هر کروشه جزئی از متن به همراه نوع آن جای گرفته است.

    """
    s, tag = "", ""
    for item in tree2conlltags(tree):
        if item[2][0] in {"B", "O"} and tag:
            s += tag + "] "
            tag = ""

        if item[2][0] == "B":
            tag = item[2].split("-")[1]
            s += "["
        s += item[0] + " "

    if tag:
        s += tag + "] "

    return s.strip()


class Chunker(IOBTagger):
    """این کلاس شامل توابعی برای تقطیع متن، آموزش و ارزیابی مدل است."""

    def __init__(
        self: "Chunker",
        model: Optional[str] = None,
        data_maker: Optional[List[List[Dict]]] = None,
    ) -> None:
        """constructor."""
        data_maker = self.data_maker if data_maker is None else data_maker
        self.posTagger = POSTagger()
        super().__init__(model, data_maker)

    def data_maker(
        self: "Chunker",
        tokens: List[List[Tuple[str, str]]],
    ) -> List[List[Dict]]:
        """تابعی که لیستی دو بعدی از کلمات به همراه لیبل را گرفته و لیست دو بعدی از از دیکشنری‌هایی که تعیین‌کننده ویژگی‌ها هر کلمه هستند را برمی‌گرداند.

        Examples:
            >>> chunker = Chunker(model = 'chunker.model')
            >>> chunker.data_maker(tokens = [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]])
            [[{'word': 'من', 'is_first': True, 'is_last': False, 'prefix-1': 'م', 'prefix-2': 'من', 'prefix-3': 'من', 'suffix-1': 'ن', 'suffix-2': 'من', 'suffix-3': 'من', 'prev_word': '', 'two_prev_word': '', 'next_word': 'به', 'two_next_word': 'مدرسه', 'is_numeric': False, 'prev_is_numeric': '', 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': '', 'next_is_punc': False, 'pos': 'PRON', 'prev_pos': '', 'next_pos': 'ADP'}, {'word': 'به', 'is_first': False, 'is_last': False, 'prefix-1': 'ب', 'prefix-2': 'به', 'prefix-3': 'به', 'suffix-1': 'ه', 'suffix-2': 'به', 'suffix-3': 'به', 'prev_word': 'من', 'two_prev_word': '.', 'next_word': 'مدرسه', 'two_next_word': 'ایران', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': False, 'pos': 'ADP', 'prev_pos': 'PRON', 'next_pos': 'NOUN,EZ'}, {'word': 'مدرسه', 'is_first': False, 'is_last': False, 'prefix-1': 'م', 'prefix-2': 'مد', 'prefix-3': 'مدر', 'suffix-1': 'ه', 'suffix-2': 'سه', 'suffix-3': 'رسه', 'prev_word': 'به', 'two_prev_word': 'من', 'next_word': 'ایران', 'two_next_word': 'رفته_بودم', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': False, 'pos': 'NOUN,EZ', 'prev_pos': 'ADP', 'next_pos': 'NOUN'}, {'word': 'ایران', 'is_first': False, 'is_last': False, 'prefix-1': 'ا', 'prefix-2': 'ای', 'prefix-3': 'ایر', 'suffix-1': 'ن', 'suffix-2': 'ان', 'suffix-3': 'ران', 'prev_word': 'مدرسه', 'two_prev_word': 'به', 'next_word': 'رفته_بودم', 'two_next_word': '.', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': False, 'pos': 'NOUN', 'prev_pos': 'NOUN,EZ', 'next_pos': 'VERB'}, {'word': 'رفته_بودم', 'is_first': False, 'is_last': False, 'prefix-1': 'ر', 'prefix-2': 'رف', 'prefix-3': 'رفت', 'suffix-1': 'م', 'suffix-2': 'دم', 'suffix-3': 'ودم', 'prev_word': 'ایران', 'two_prev_word': 'مدرسه', 'next_word': '.', 'two_next_word': '', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': True, 'pos': 'VERB', 'prev_pos': 'NOUN', 'next_pos': 'PUNCT'}, {'word': '.', 'is_first': False, 'is_last': True, 'prefix-1': '.', 'prefix-2': '.', 'prefix-3': '.', 'suffix-1': '.', 'suffix-2': '.', 'suffix-3': '.', 'prev_word': 'رفته_بودم', 'two_prev_word': 'ایران', 'next_word': '', 'two_next_word': '', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': '', 'is_punc': True, 'prev_is_punc': False, 'next_is_punc': '', 'pos': 'PUNCT', 'prev_pos': 'VERB', 'next_pos': ''}]]

        Args:
            tokens: جملاتی که نیاز به تبدیل آن به برداری از ویژگی‌ها است.

        Returns:
            لیستی از لیستی از دیکشنری‌های بیان‌کننده ویژگی‌های یک کلمه.

        """
        words = [[word for word, _ in token] for token in tokens]
        tags = [[tag for _, tag in token] for token in tokens]
        return [
            [
                self.features(words=word_tokens, pos_tags=tag_tokens, index=index)
                for index in range(len(word_tokens))
            ]
            for word_tokens, tag_tokens in zip(words, tags)
        ]

    def features(
        self: "Chunker",
        words: List[str],
        pos_tags: List[str],
        index: int,
    ) -> Dict[str, Union[str, bool]]:
        """ویژگی‌های کلمه را برمی‌گرداند."""
        word_features = self.posTagger.features(words, index)
        word_features.update(
            {
                "pos": pos_tags[index],
                "prev_pos": "" if index == 0 else pos_tags[index - 1],
                "next_pos": "" if index == len(pos_tags) - 1 else pos_tags[index + 1],
            },
        )
        return word_features

    def train(
        self: "Chunker",
        trees: List[str],
        c1: float = 0.4,
        c2: float = 0.04,
        max_iteration: int = 400,
        verbose: bool = True,
        file_name: str = "chunker_crf.model",
        report_duration: bool = True,
    ) -> None:
        """از روی درخت ورودی، مدل را آموزش می‌دهد.

        Args:
            trees: لیستی از درخت‌ها برای آموزش مدل.
            c1: مقدار L1 regularization.
            c2: مقدار L2 regularization.
            max_iteration: تعداد تکرار آموزش بر کل دیتا.
            verbose: نمایش اطلاعات مربوط به آموزش.
            file_name: نام و مسیر فایلی که می‌خواهید مدل در آن ذخیره شود.
            report_duration: نمایش گزارشات مربوط به زمان.

        """
        return super().train(
            [tree2conlltags(tree) for tree in trees],
            c1,
            c2,
            max_iteration,
            verbose,
            file_name,
            report_duration,
        )

    def parse(self: "Chunker", sentence: List[Tuple[str, str]]) -> str:
        """جمله‌ای را در قالب لیستی از تاپل‌های دوتایی [(توکن, نوع), (توکن, نوع), ...]
        دریافت می‌کند و درخت تقطع‌شدهٔ آن را بر می‌گرداند.

        Examples:
            >>> chunker = Chunker(model = 'chunker.model')
            >>> tree = chunker.parse(sentence = [('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')])
            >>> print(tree)
            (S
              (NP نامه/NOUN,EZ ایشان/PRON)
              (POSTP را/ADP)
              (VP دریافت/NOUN داشتم/VERB)
              ./PUNCT)

        Args:
            sentence: جمله‌ای که باید درخت تقطیع‌شدهٔ آن تولید شود.

        Returns:
            ساختار درختی حاصل از تقطیع.
            برای تبدیل این ساختار درختی به یک ساختار کروشه‌ای و قابل‌درک‌تر
            می‌توانید از تابع `tree2brackets()` استفاده کنید.

        """
        return conlltags2tree(super().tag(sentence))

    def parse_sents(
        self: "Chunker",
        sentences: List[List[Tuple[str, str]]],
    ) -> Iterator[str]:
        """جملات ورودی را به‌شکل تقطیع‌شده و در قالب یک برمی‌گرداند.

        Args:
            sentences: جملات ورودی.

        Yields:
            یک `Iterator` از جملات تقطیع شده.

        """
        for conlltagged in super().tag_sents(sentences):
            yield conlltags2tree(conlltagged)

    def evaluate(self: "Chunker", trees: List[str]) -> float:
        """داده صحیح دریافت شده را با استفاده از مدل لیبل می‌زند و دقت مدل را برمی‌گرداند.

        Examples:
            >>> chunker = Chunker(model = 'chunker.model')
            >>> trees = list(chunker.parse_sents([[('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')]]))
            >>> chunker.evaluate(trees)
            1.0

        Args:
            trees: لیست درختانی که با استفاده از آن مدل را ارزیابی می‌کنیم.

        Returns:
            دقت مدل

        """
        return super().evaluate([tree2conlltags(tree) for tree in trees])


class RuleBasedChunker(RegexpParser):
    """کلاس RuleBasedChunker.


    Examples:
    >>> chunker = RuleBasedChunker()
    >>> tree2brackets(chunker.parse([('نامه', 'Ne'), ('۱۰', 'NUMe'), ('فوریه', 'Ne'), ('شما', 'PRO'), ('را', 'POSTP'), ('دریافت', 'N'), ('داشتم', 'V'), ('.', 'PUNC')]))
    '[نامه ۱۰ فوریه شما NP] [را POSTP] [دریافت داشتم VP] .'

    """

    def __init__(self: "RuleBasedChunker") -> None:
        grammar = r"""

            NP:
                <P>{<N>}<V>

            VP:
                <.*[^e]>{<N>?<V>}
                {<V>}

            ADVP:
                {<ADVe?><AJ>?}

            ADJP:
                <.*[^e]>{<AJe?>}

            NP:
                {<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?|AJe?|PRO|CL|RESe?>*}
                <N>}{<.*e?>

            ADJP:
                {<AJe?>}

            POSTP:
                {<POSTP>}

            PP:
                {<Pe?>+}

        """

        super().__init__(grammar=grammar)
