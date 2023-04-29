# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای تجزیهٔ متن به عبارات اسمی، فعلی و حرف
اضافه‌ای است. **میزان دقت تجزیه‌گر سطحی در نسخهٔ حاضر ۸۹.۹ درصد [^1] است.**
[^1]:
این عدد با انتشار هر نسخه بروزرسانی می‌شود.

"""

from __future__ import unicode_literals
from nltk.chunk import RegexpParser, tree2conlltags, conlltags2tree
from .SequenceTagger import IOBTagger
from .POSTagger import POSTagger


def tree2brackets(tree):
    """خروجی درختی تابع [parse()][hazm.Chunker.Chunker.parse] را به یک ساختار
    کروشه‌ای تبدیل می‌کند.

    Examples:
        >>> chunker = Chunker(model='resources/chunker.model')
        >>> tree=chunker.parse([('نامه', 'Ne'), ('ایشان', 'PRO'), ('را', 'POSTP'), ('دریافت', 'N'), ('داشتم', 'V'), ('.', 'PUNC')])
        >>> print(tree)
        (S
          (NP نامه/Ne ایشان/PRO)
          (POSTP را/POSTP)
          (VP دریافت/N داشتم/V)
          ./PUNC)
        >>> tree2brackets(tree)
        '[نامه ایشان NP] [را POSTP] [دریافت داشتم VP] .'

    Args:
        tree (str): ساختار درختی حاصل از پردزاش تابع parse()

    Returns:
        (str): رشته‌ای از کروشه‌ها که در هر کروشه جزئی از متن به همراه نوع آن جای گرفته است.

    """
    str, tag = "", ""
    for item in tree2conlltags(tree):
        if item[2][0] in {"B", "O"} and tag:
            str += tag + "] "
            tag = ""

        if item[2][0] == "B":
            tag = item[2].split("-")[1]
            str += "["
        str += item[0] + " "

    if tag:
        str += tag + "] "

    return str.strip()


class Chunker(IOBTagger):
    """این کلاس شامل توابعی برای تقطیع متن، آموزش و ارزیابی مدل است."""

    def __init__(self, model=None, data_maker=None):
        data_maker = self.data_maker if data_maker == None else data_maker
        self.posTagger = POSTagger()
        super().__init__(model, data_maker)

    def data_maker(self, tokens):
        """تابعی که لیستی دو بعدی از کلمات به همراه لیبل را گرفته و لیست دو بعدی از از دیکشنری‌هایی که تعیین‌کننده ویژگی‌ها هر کلمه هستند را برمی‌گرداند.

        Examples:
            >>> chunker = Chunker(model = 'tagger.model')
            >>> chunker.data_maker(tokens = [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]])
            [[{'word': 'نتوانستم', 'is_first': True, 'is_last': False, 'prefix-1': 'ن', ..., 'next_pos': 'ADP'}, ..., 'prev_is_punc': False, 'next_is_punc': '', 'pos': 'PUNCT', 'prev_pos': 'VERB', 'next_pos': ''}]]

        Args:
            tokens (List[List[Tuple[str, str]]]): جملاتی که نیاز به تبدیل آن به برداری از ویژگی‌ها است.

        Returns:
            List(List(Dict())): لیستی از لیستی از دیکشنری‌های بیان‌کننده ویژگی‌های یک کلمه.

        """
        words = [[word for word, _ in token] for token in tokens]
        tags = [[tag for _, tag in token] for token in tokens]
        return [
            [
                self.features(words=word_tokens, pos_taggs=tag_tokens, index=index)
                for index in range(len(word_tokens))
            ]
            for word_tokens, tag_tokens in zip(words, tags)
        ]

    def features(self, words, pos_taggs, index):
        word_features = self.posTagger.features(words, index)
        word_features.update(
            {
                "pos": pos_taggs[index],
                "prev_pos": "" if index == 0 else pos_taggs[index - 1],
                "next_pos": "" if index == len(pos_taggs) - 1 else pos_taggs[index + 1],
            }
        )
        return word_features

    def train(
        self,
        trees,
        c1=0.4,
        c2=0.04,
        max_iteration=400,
        verbose=True,
        file_name="chunker_crf.model",
        report_duration=True,
    ):
        """از روی درخت ورودی، مدل را آموزش می‌دهد.

        Args:
            trees (List[Tree]): لیستی از درخت‌ها برای آموزش مدل.
            c1 (float): مقدار L1 regularization.
            c2 (float): مقدار L2 regularization.
            max_iteration (int): تعداد تکرار آموزش بر کل دیتا.
            verbose (boolean): نمایش اطلاعات مربوط به آموزش.
            file_name (str): نام و مسیر فایلی که می‌خواهید مدل در آن ذخیره شود.
            report_duraion (boolean): نمایش گزارشات مربوط به زمان.

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

    def parse(self, sentence):
        """جمله‌ای را در قالب لیستی از تاپل‌های دوتایی [(توکن, نوع), (توکن, نوع), ...]
        دریافت می‌کند و درخت تقطع‌شدهٔ آن را بر می‌گرداند.

        Examples:
            >>> chunker = Chunker(model = 'tagger.model')
            >>> tree = chunker.parse(sentence = [('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')])
            >>> print(tree)
            (S
              (NP نامه/NOUN,EZ ایشان/PRON)
              (POSTP را/ADP)
              (VP دریافت/NOUN داشتم/VERB)
              ./PUNCT)

        Args:
            sentence (List[Tuple[str,str]): جمله‌ای که باید درخت تقطیع‌شدهٔ آن تولید شود.

        Returns:
            (str): ساختار درختی حاصل از تقطیع.
            برای تبدیل این ساختار درختی به یک ساختار کروشه‌ای و قابل‌درک‌تر
            می‌توانید از تابع `tree2brackets()` استفاده کنید.

        """
        return conlltags2tree(super().tag(sentence))

    def parse_sents(self, sentences):
        """جملات ورودی را به‌شکل تقطیع‌شده و در قالب یک برمی‌گرداند.

        Args:
            sentences (List[List[Tuple(str,str)]]): جملات ورودی.

        Yields:
            (Iterator[str]): یک `Iterator` از جملات تقطیع شده.

        """
        for conlltagged in super(Chunker, self).tag_sents(sentences):
            yield conlltags2tree(conlltagged)


class RuleBasedChunker(RegexpParser):
    """

    Examples:
        >>> chunker = RuleBasedChunker()
        >>> tree2brackets(chunker.parse([('نامه', 'Ne'), ('۱۰', 'NUMe'), ('فوریه', 'Ne'), ('شما', 'PRO'), ('را', 'POSTP'), ('دریافت', 'N'), ('داشتم', 'V'), ('.', 'PUNC')]))
        '[نامه ۱۰ فوریه شما NP] [را POSTP] [دریافت داشتم VP] .'

    """

    def __init__(self):
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

        super(RuleBasedChunker, self).__init__(grammar=grammar)
