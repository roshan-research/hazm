"""این ماژول شامل کلاس‌ها و توابعی برای برچسب‌گذاری توکن‌هاست."""

import time
from typing import List
from typing import Tuple

import numpy as np
from pycrfsuite import Tagger
from pycrfsuite import Trainer
from sklearn.metrics import accuracy_score


def features(sent, index):
    """فهرست فیچرها را برمی‌گرداند."""
    return {
        "word": sent[index],
        "is_first": index == 0,
        "is_last": index == len(sent),
        "is_num": sent[index].isdigit(),
        "prev_word": sent[index - 1] if index != 0 else "",
        "next_word": sent[index + 1] if index != len(sent) - 1 else "",
    }


def data_maker(tokens):
    """تابع دیتا میکر."""
    return [[features(sent, index) for index in range(len(sent))] for sent in tokens]


def iob_features(words, pos_tags, index):
    """تابع iob_features."""
    word_features = features(words, index)
    word_features.update(
        {
            "pos": pos_tags[index],
            "prev_pos": "" if index == 0 else pos_tags[index - 1],
            "next_pos": "" if index == len(pos_tags) - 1 else pos_tags[index + 1],
        },
    )
    return word_features


def iob_data_maker(tokens):
    """تابع iob_data_maker."""
    words = [[word for word, _ in token] for token in tokens]
    tags = [[tag for _, tag in token] for token in tokens]
    return [
        [
            iob_features(words=word_tokens, pos_taggs=tag_tokens, index=index)
            for index in range(len(word_tokens))
        ]
        for word_tokens, tag_tokens in zip(words, tags)
    ]


class SequenceTagger:
    """این کلاس شامل توابعی برای برچسب‌گذاری توکن‌ها است. این کلاس در نقش یک
    wrapper برای کتابخانهٔ [python-crfsuite](https://python-crfsuite.readthedocs.io/en/latest/) است.

    Args:
        model (str, optional): مسیر فایل tagger.
        data_maker (function, optional): تابعی که لیستی دو بعدی از کلمات توکنایز شده را گرفته و لیست دو بعدی از از دیکشنری‌هایی که تعیین‌کننده ویژگی‌ها هر کلمه هستند را برمی‌گرداند.
    """

    def __init__(self: "SequenceTagger", model=None, data_maker=data_maker) -> None:
        if model is not None:
            self.load_model(model)
        else:
            self.model = None
        self.data_maker = data_maker

    def __add_label(self: "SequenceTagger", sentence, tags):
        return [(word, tag) for word, tag in zip(sentence, tags)]

    def __tag(self: "SequenceTagger", tokens):
        return self.__add_label(tokens, self.model.tag(self.data_maker([tokens])[0]))

    def __train(
        self: "SequenceTagger", x, y, args, verbose, file_name, report_duration,
    ):
        trainer = Trainer(verbose=verbose)
        trainer.set_params(args)

        for xseq, yseq in zip(x, y):
            trainer.append(xseq, yseq)

        start_time = time.time()
        trainer.train(file_name)
        end_time = time.time()

        if report_duration:
            print(f"training time: {(end_time - start_time):.2f} sec")

        self.load_model(file_name)

    def __evaluate(self: "SequenceTagger", gold_labels, predicted_labels):
        gold_labels = np.concatenate(gold_labels)
        predicted_labels = np.concatenate(predicted_labels)
        return float(accuracy_score(gold_labels, predicted_labels))

    def load_model(self: "SequenceTagger", model):
        """فایل تگر را بارگزاری می‌کند.

        Examples:
            >>> tagger = SequenceTagger()
            >>> tagger.load_model(model = 'tagger.model')

        Args:
            model (str): مسیر فایل تگر.

        """
        tagger = Tagger()
        tagger.open(model)
        self.model = tagger

    def tag(self: "SequenceTagger", tokens):
        """یک جمله را در قالب لیستی از توکن‌ها دریافت می‌کند و در خروجی لیستی از
        `(توکن، برچسب)`ها برمی‌گرداند.

        Examples:
            >>> tagger = SequenceTagger(model = 'tagger.model')
            >>> tagger.tag(tokens = ['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.'])
            [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]

        Args:
            tokens (List[str]): لیستی از توکن‌های یک جمله که باید برچسب‌گذاری شود.

        Returns:
            (List[Tuple[str,str]]): ‌لیستی از `(توکن، برچسب)`ها.

        """
        if self.model is None:
            msg = "you should load model first..."
            raise ValueError(msg)

        return self.__tag(tokens)

    def tag_sents(self: "SequenceTagger", sentences):
        """جملات را در قالب لیستی از توکن‌ها دریافت می‌کند
        و در خروجی، لیستی از لیستی از `(توکن، برچسب)`ها برمی‌گرداند.

        هر لیست از `(توکن، برچسب)`ها مربوط به یک جمله است.

        Examples:
            >>> tagger = SequenceTagger(model = 'tagger.model')
            >>> tagger.tag_sents(sentences = [['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.']])
            [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]]

        Args:
            sentences (List[List[str]]): لیستی از جملات که باید برچسب‌گذاری شود.

        Returns:
            (List[List[Tuple[str,str]]]): لیستی از لیستی از `(توکن، برچسب)`ها.
                    هر لیست از `(توکن،برچسب)`ها مربوط به یک جمله است.

        """
        if self.model is None:
            msg = "you should load model first..."
            raise ValueError(msg)

        return [self.__tag(tokens) for tokens in sentences]

    def train(
        self: "SequenceTagger",
        tagged_list,
        c1=0.4,
        c2=0.04,
        max_iteration=400,
        verbose=True,
        file_name="crf.model",
        report_duration=True,
    ):
        """لیستی از جملات را می‌گیرد و بر اساس آن مدل را آموزش می‌دهد.

        هر جمله، لیستی از `(توکن، برچسب)`هاست.

        Examples:
            >>> tagger = SequenceTagger()
            >>> tagger.train(tagged_list = [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]], c1 = 0.5, c2 = 0.5, max_iteration = 100, verbose = True, file_name = 'tagger.model', report_duration = True)
            Feature generation
            type: CRF1d
            feature.minfreq: 0.000000
            feature.possible_states: 0
            feature.possible_transitions: 1
            0....1....2....3....4....5....6....7....8....9....10
            Number of features: 150
            Seconds required: 0.001
            ...
            Writing feature references for attributes
            Seconds required: 0.000

            training time: 0.01 sec

        Args:
            tagged_list (List[{List[Tuple[str,str]]]): جملاتی که مدل از روی آن‌ها آموزش می‌بیند.
            c1 (float): مقدار L1 regularization.
            c2 (float): مقدار L2 regularization.
            max_iteration (int): تعداد تکرار آموزش بر کل دیتا.
            verbose (boolean): نمایش اطلاعات مربوط به آموزش.
            file_name (str): نام و مسیر فایلی که می‌خواهید مدل در آن ذخیره شود.
            report_duration (boolean): نمایش گزارشات مربوط به زمان.

        """
        x = self.data_maker(
            [[x for x, _ in tagged_sent] for tagged_sent in tagged_list],
        )
        y = [[y for _, y in tagged_sent] for tagged_sent in tagged_list]

        args = {
            "c1": c1,
            "c2": c2,
            "max_iterations": max_iteration,
            "feature.possible_transitions": True,
        }

        self.__train(x, y, args, verbose, file_name, report_duration)

    def save_model(self: "SequenceTagger", filename):
        """مدل تهیه‌شده توسط تابع [train()][hazm.sequence_tagger.SequenceTagger.train]
        را ذخیره می‌کند.

        Examples:
            >>> tagger = SequenceTagger()
            >>> tagger.train(tagged_list = [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]], c1 = 0.5, c2 = 0.5, max_iteration = 100, verbose = True, file_name = 'tagger.model', report_duration = True)
            >>> tagger.save_model(file_name = 'new_tagger.model')

        Args:
            filename (str): نام و مسیر فایلی که می‌خواهید مدل در آن ذخیره شود.

        """
        if self.model is None:
            msg = "you should load model first..."
            raise ValueError(msg)

        self.model.dump(filename)

    def evaluate(
        self: "SequenceTagger", tagged_sent: List[List[Tuple[str, str]]],
    ) -> float:
        """داده صحیح دریافت شده را با استفاده از مدل لیبل می‌زند و دقت مدل را برمی‌گرداند.

        Examples:
            >>> tagger = SequenceTagger(model = 'tagger.model')
            >>> tagger.evaluate([[('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')]])
            1.0


        Args:
            tagged_sent: جملات لیبل‌داری که با استفاده از آن مدل را ارزیابی می‌کنیم.

        Returns:
            دقت مدل

        """
        if self.model is None:
            msg = "you should load model first..."
            raise ValueError(msg)

        def extract_labels(tagged_list):
            return [[label for _, label in sent] for sent in tagged_list]

        tokens = [[word for word, _ in sent] for sent in tagged_sent]
        predicted_tagged_sent = self.tag_sents(tokens)
        return self.__evaluate(
            extract_labels(tagged_sent),
            extract_labels(predicted_tagged_sent),
        )


class IOBTagger(SequenceTagger):
    """IOBTagger."""

    def __init__(self: "SequenceTagger", model=None, data_maker=iob_data_maker) -> None:
        super().__init__(model, data_maker)

    def __iob_format(self: "SequenceTagger", tagged_data, chunk_tags):
        return [
            (token[0], token[1], chunk_tag[1])
            for token, chunk_tag in zip(tagged_data, chunk_tags)
        ]

    def tag(self: "SequenceTagger", tagged_data):
        """یک جمله را در قالب لیستی از توکن‌ها و تگ‌ها دریافت می‌کند و در خروجی لیستی از
        `(توکن، تگ، برچسب)`ها برمی‌گرداند.

        Examples:
            >>> iobTagger = IOBTagger(model = 'tagger.model')
            >>> iobTagger.tag(tagged_data = [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')])
            [('من', 'PRON', 'B-NP'), ('به', 'ADP', 'B-PP'), ('مدرسه', 'NOUN,EZ', 'B-NP'), ('ایران', 'NOUN', 'I-NP'), ('رفته_بودم', 'VERB', 'B-VP'), ('.', 'PUNCT', 'O')]

        Args:
            tagged_data (List[Tuple[str, str]]): لیستی از توکن‌های یک جمله که باید برچسب‌گذاری شود.

        Returns:
            (List[Tuple[str, str, str]]): ‌لیستی از `(توکن، تگ، برچسب)`ها.

        """
        chunk_tags = super().tag(tagged_data)
        return self.__iob_format(tagged_data, chunk_tags)

    def tag_sents(self: "SequenceTagger", sentences):
        """جملات را در قالب لیستی لیستی از توکن‌ها و تگ‌ها دریافت می‌کند
        و در خروجی، لیستی از لیستی از `(توکن، تگ، برچسب)`ها برمی‌گرداند.

        هر لیست از `(توکن، برچسب)`ها مربوط به یک جمله است.

        Examples:
            >>> iobTagger = IOBTagger(model = 'tagger.model')
            >>> iobTagger.tag_sents(tagged_data = [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]])
            [[('من', 'PRON', 'B-NP'), ('به', 'ADP', 'B-PP'), ('مدرسه', 'NOUN,EZ', 'B-NP'), ('ایران', 'NOUN', 'I-NP'), ('رفته_بودم', 'VERB', 'B-VP'), ('.', 'PUNCT', 'O')]]

        Args:
            sentences (List[List[str]]): لیستی از جملات که باید برچسب‌گذاری شود.

        Returns:
            (List[List[Tuple[str,str]]]): لیستی از لیستی از `(توکن، تگ، برچسب)`ها.
                    هر لیست از `(توکن، تگ، برچسب)`ها مربوط به یک جمله است.

        """
        chunk_tags = super().tag_sents(sentences)
        return [
            self.__iob_format(tagged_data, chunks)
            for tagged_data, chunks in zip(sentences, chunk_tags)
        ]

    def train(
        self: "SequenceTagger",
        tagged_list: List[List[Tuple[str, str, str]]],
        c1: float = 0.4,
        c2: float = 0.04,
        max_iteration: int = 400,
        verbose: True = True,
        file_name: str = "crf.model",
        report_duration=True,
    ):
        """لیستی از جملات را می‌گیرد و بر اساس آن مدل را آموزش می‌دهد.

        هر جمله، لیستی از `(توکن، تگ، برچسب)`هاست.

        Examples:
            >>> iobTagger = IOBTagger()
            >>> iobTagger.train(tagged_list = [[('من', 'PRON', 'B-NP'), ('به', 'ADP', 'B-PP'), ('مدرسه', 'NOUN,EZ', 'B-NP'), ('ایران', 'NOUN', 'I-NP'), ('رفته_بودم', 'VERB', 'B-VP'), ('.', 'PUNCT', 'O')]], c1 = 0.5, c2 = 0.5, max_iteration = 100, verbose = True, file_name = 'newIOBTagger.model', report_duration = True)
            Feature generation
            type: CRF1d
            feature.minfreq: 0.000000
            feature.possible_states: 0
            feature.possible_transitions: 1
            0....1....2....3....4....5....6....7....8....9....10
            Number of features: 150
            Seconds required: 0.001
            ...
            Writing feature references for attributes
            Seconds required: 0.000

            training time: 0.01 sec

        Args:
            tagged_list: جملاتی که مدل از روی آن‌ها آموزش می‌بیند.
            c1: مقدار L1 regularization.
            c2: مقدار L2 regularization.
            max_iteration: تعداد تکرار آموزش بر کل دیتا.
            verbose: نمایش اطلاعات مربوط به آموزش.
            file_name: نام و مسیر فایلی که می‌خواهید مدل در آن ذخیره شود.
            report_duration: نمایش گزارشات مربوط به زمان.

        """
        tagged_list = [
            [((word, tag), chunk) for word, tag, chunk in tagged_sent]
            for tagged_sent in tagged_list
        ]
        return super().train(
            tagged_list,
            c1,
            c2,
            max_iteration,
            verbose,
            file_name,
            report_duration,
        )

    def evaluate(
        self: "SequenceTagger", tagged_sent: List[List[Tuple[str, str, str]]],
    ) -> float:
        """داده صحیح دریافت شده را با استفاده از مدل لیبل می‌زند و دقت مدل را برمی‌گرداند.

        Examples:
            >>> iobTagger = IOBTagger(model = 'tagger.model')
            >>> iobTagger.evaluate([[('نامه', 'NOUN,EZ', 'B-NP'), ('ایشان', 'PRON', 'I-NP'), ('را', 'ADP', 'B-POSTP'), ('دریافت', 'NOUN', 'B-VP'), ('داشتم', 'VERB', 'I-VP'), ('.', 'PUNCT', 'O')]])
            1.0


        Args:
            tagged_sent: جملات لیبل‌داری که با استفاده از آن مدل را ارزیابی می‌کنیم.

        Returns:
            دقت مدل

        """
        if self.model is None:
            msg = "you should load model first..."
            raise ValueError(msg)

        def extract_labels(tagged_list):
            return [[token[-1] for token in sent] for sent in tagged_list]

        tokens = [[token[:-1] for token in sent] for sent in tagged_sent]
        predicted_tagged_sent = self.tag_sents(tokens)
        return super()._SequenceTagger__evaluate(
            extract_labels(tagged_sent),
            extract_labels(predicted_tagged_sent),
        )
