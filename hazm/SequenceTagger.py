# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای برچسب‌گذاری توکن‌هاست.
"""

from __future__ import unicode_literals
from nltk.tag.api import TaggerI
from nltk.metrics import accuracy


class SequenceTagger(TaggerI):
    """این کلاس شامل توابعی برای برچسب‌گذاری توکن‌ها است. این کلاس در نقش یک wrapper برای کتابخانهٔ [Wapiti](https://wapiti.limsi.fr/) است.

    Args:
            patterns (List, optional): الگوهای لازم برای ساخت مدل.
            **options (Dict, optional): آرگومان‌های نامدارِ اختیاری.

    """

    def __init__(self, patterns=[], **options):
        from wapiti import Model

        self.model = Model(patterns="\n".join(patterns), **options)

    def train(self, sentences):
        """لیستی از جملات را می‌گیرد و بر اساس آن مدل را آموزش می‌دهد.

        هر جمله، لیستی از `(توکن، برچسب)`هاست.

        Examples:
                >>> tagger = SequenceTagger(patterns=['*', 'u:word-%x[0,0]'])
                >>> tagger.train([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])

        Args:
                sentences (List[List[Tuple[str,str]]]): جملاتی که مدل از روی آن‌ها آموزش می‌بیند.
        """
        self.model.train(
            ["\n".join([" ".join(word) for word in sentence]) for sentence in sentences]
        )

    def save_model(self, filename):
        """مدل تهیه‌شده توسط تابع [train()][hazm.SequenceTagger.SequenceTagger.train] را ذخیره می‌کند.

        Examples:
                >>> tagger = SequenceTagger(patterns=['*', 'u:word-%x[0,0]'])
                >>> tagger.train([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
                >>> tagger.save_model('resources/test.model')

        Args:
                filename (str): نام و مسیر فایلی که می‌خواهید مدل در آن ذخیره شود.
        """
        self.model.save(filename)

    def tag(self, tokens):
        """یک جمله را در قالب لیستی از توکن‌ها دریافت می‌کند و در خروجی لیستی از `(توکن، برچسب)`ها برمی‌گرداند.

        Examples:
                >>> tagger = SequenceTagger(patterns=['*', 'u:word-%x[0,0]'])
                >>> tagger.tag(['من', 'به', 'مدرسه', 'رفته_بودم', '.'])
                [('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]

        Args:
                tokens (List[str]): لیستی از توکن‌های یک جمله که باید برچسب‌گذاری شود.

        Returns:
                (List[Tuple[str,str]]): ‌لیستی از `(توکن، برچسب)`ها.
        """
        return self.tag_sents([tokens])[0]

    def tag_sents(self, sentences):
        """جملات را در قالب لیستی از توکن‌ها دریافت می‌کند
        و در خروجی، لیستی از لیستی از `(توکن، برچسب)`ها برمی‌گرداند.

        هر لیست از `(توکن، برچسب)`ها مربوط به یک جمله است.

        Examples:
                >>> tagger = SequenceTagger(patterns=['*', 'u:word-%x[0,0]'])
                >>> tagger.tag_sents([['من', 'به', 'مدرسه', 'رفته_بودم', '.']])
                [[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]]

        Args:
                sentences (List[List[str]]): لیستی از جملات که باید برچسب‌گذاری شود.

        Returns:
                (List[List[Tuple[str,str]]]): لیستی از لیستی از `(توکن، برچسب)`ها.

                        هر لیست از `(توکن،برچسب)`ها مربوط به یک جمله است.
        """
        sentences = list(sentences)
        lines = "\n\n".join(["\n".join(sentence) for sentence in sentences]).replace(
            " ", "_"
        )
        results = self.model.label_sequence(lines).decode("utf8")
        tags = iter(results.strip().split("\n"))
        return [[(word, next(tags)) for word in sentence] for sentence in sentences]


class IOBTagger(SequenceTagger):
    """ """

    def tag_sents(self, sentences):
        """
        Examples:
                >>> tagger = IOBTagger(patterns=['*', 'U:word-%x[0,0]', 'U:word-%x[0,1]'])
                >>> tagger.train([[('من', 'PRO', 'B-NP'), ('به', 'P', 'B-PP'), ('مدرسه', 'N', 'B-NP'), ('رفته_بودم', 'V', 'B-VP'), ('.', 'PUNC', 'O')]])
                >>> tagger.tag_sents([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
                [[('من', 'PRO', 'B-NP'), ('به', 'P', 'B-PP'), ('مدرسه', 'N', 'B-NP'), ('رفته_بودم', 'V', 'B-VP'), ('.', 'PUNC', 'O')]]
        """
        sentences = list(sentences)
        lines = "\n\n".join(
            [
                "\n".join(["\t".join(word) for word in sentence])
                for sentence in sentences
            ]
        ).replace(" ", "_")
        results = self.model.label_sequence(lines).decode("utf8")
        tags = iter(results.strip().split("\n"))
        return [[word + (next(tags),) for word in sentence] for sentence in sentences]

    def evaluate(self, gold):
        """
        Examples:
                >>> tagger = IOBTagger(patterns=['*', 'U:word-%x[0,0]', 'U:word-%x[0,1]'])
                >>> tagger.evaluate([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
        """
        tagged_sents = self.tag_sents(
            ([word[:-1] for word in sentence] for sentence in gold)
        )
        return accuracy(sum(gold, []), sum(tagged_sents, []))
