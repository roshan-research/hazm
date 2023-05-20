"""این ماژول شامل کلاس‌ها و توابعی برای تبدیل کلمه یا متن به برداری از اعداد است."""
import multiprocessing
import os
import warnings
from pathlib import Path
from typing import Any
from typing import Iterator
from typing import List
from typing import Tuple
from typing import Type

from gensim.models import Doc2Vec
from gensim.models import KeyedVectors
from gensim.models import fasttext
from gensim.models.doc2vec import TaggedDocument
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import datapath
from numpy import ndarray

from hazm import Normalizer

from hazm import word_tokenize

supported_embeddings = ["fasttext", "keyedvector", "glove"]


class WordEmbedding:
    """این کلاس شامل توابعی برای تبدیل کلمه به برداری از اعداد است.

    Args:
        model_type: نوع امبدینگ که می‌تواند یکی از مقادیر ‍`fasttext`, `keyedvector`, `glove` باشد.
        model_path: مسیر فایل امبدینگ.

    """

    def __init__(
        self: "WordEmbedding",
        model_type: str,
        model_path: str = None,
    ) -> None:
        if model_type not in supported_embeddings:
            msg = (
                f'Model type "{model_type}" is not supported! Please choose from'
                f" {supported_embeddings}"
            )
            raise KeyError(
                msg,
            )
        self.model_type = model_type
        if model_path:
            self.load_model(model_path)

    def load_model(self: "WordEmbedding", model_path: str) -> None:
        """فایل امبدینگ را بارگزاری می‌کند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.load_model('resources/cc.fa.300.bin')

        Args:
            model_path: مسیر فایل امبدینگ.

        """
        if self.model_type == "fasttext":
            self.model = fasttext.load_facebook_model(model_path).wv
        elif self.model_type == "keyedvector":
            if model_path.endswith("bin"):
                self.model = KeyedVectors.load_word2vec_format(model_path, binary=True)
            else:
                self.model = KeyedVectors.load_word2vec_format(model_path)
        elif self.model_type == "glove":
            word2vec_addr = str(model_path) + "_word2vec_format.vec"
            if not Path.exists(word2vec_addr):
                _ = glove2word2vec(model_path, word2vec_addr)
            self.model = KeyedVectors.load_word2vec_format(word2vec_addr)
            self.model_type = "keyedvector"
        else:
            msg = (
                f"{self.model_type} not supported! Please choose from"
                f" {supported_embeddings}"
            )
            raise KeyError(
                msg,
            )

    def train(
        self: "WordEmbedding",
        dataset_path: str,
        workers: int = multiprocessing.cpu_count() - 1,  # noqa: B008
        vector_size: int = 200,
        epochs: int = 10,
        fasttext_type: str = "skipgram",
        dest_path: str = None,
    ) -> None:
        """یک فایل امبدینگ از نوع fasttext ترین می‌کند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.train(dataset_path = 'dataset.txt', worker = 4, vector_size = 300, epochs = 30, fasttext_type = 'cbow', dest_path = 'fasttext_model')

        Args:
            dataset_path: مسیر فایل متنی.
            workers: تعداد هسته درگیر برای ترین مدل.
            vector_size: طول وکتور خروجی به ازای هر کلمه.
            epochs: تعداد تکرار ترین بر روی کل دیتا.
            fasttext_type: نوع fasttext مورد نظر برای ترین که میتواند یکی از مقادیر skipgram یا cbow را داشته باشد.
            dest_path: مسیر مورد نظر برای ذخیره فایل امبدینگ.

        """
        if self.model_type != "fasttext":
            self.model = "fasttext"
            warnings.warn(
                (
                    "this function is for training fasttext models only and"
                    f" {self.model_type} is not supported"
                ),
                stacklevel=2,
            )

        fasttext_model_types = ["cbow", "skipgram"]
        if fasttext_type not in fasttext_model_types:
            msg = (
                f'Model type "{fasttext_type}" is not supported! Please choose from'
                f" {fasttext_model_types}"
            )
            raise KeyError(
                msg,
            )

        workers = 1 if workers == 0 else workers

        model = fasttext.train_unsupervised(
            dataset_path,
            model=fasttext_type,
            dim=vector_size,
            epoch=epochs,
            thread=workers,
        )

        self.model = model.wv

        print("Model trained.")

        if dest_path is not None:
            model.save_model(dest_path)
            print("Model saved.")

    def __getitem__(self: "WordEmbedding", word: str) -> str:
        """__getitem__."""
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)
        return self.model[word]

    def doesnt_match(self: "WordEmbedding", words: List[str]) -> str:
        """لیستی از کلمات را دریافت می‌کند و کلمهٔ نامرتبط را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.doesnt_match(['سلام' ,'درود' ,'خداحافظ' ,'پنجره'])
            'پنجره'
            >>> wordEmbedding.doesnt_match(['ساعت' ,'پلنگ' ,'شیر'])
            'ساعت'

        Args:
            words: لیست کلمات.

        Returns:
            کلمهٔ نامرتبط.

        """
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)
        return self.model.doesnt_match(words)

    def similarity(self: "WordEmbedding", word1: str, word2: str) -> float:
        """میزان شباهت دو کلمه را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.similarity('ایران', 'آلمان')
            0.44988164
            >>> wordEmbedding.similarity('ایران', 'پنجره')
            0.08837362

        Args:
            word1: کلمهٔ اول
            word2: کلمهٔ دوم

        Returns:
            میزان شباهت دو کلمه.

        """
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)
        return float(str(self.model.similarity(word1, word2)))

    def get_vocab(self: "WordEmbedding") -> List[str]:
        """لیستی از کلمات موجود در فایل امبدینگ را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.get_vocab()
            ['،', 'در', '.', 'و', ...]

        Returns:
            لیست کلمات موجود در فایل امبدینگ.

        """
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)
        return self.model.index_to_key

    def nearest_words(
        self: "WordEmbedding",
        word: str,
        topn: int = 5,
    ) -> List[Tuple[str, str]]:
        """کلمات مرتبط با یک واژه را به همراه میزان ارتباط آن برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.nearest_words('ایران', topn = 5)
            [('ايران', 0.657148540019989'), (جمهوری', 0.6470394134521484'), (آمریکا', 0.635792076587677'), (اسلامی', 0.6354473233222961'), (کشور', 0.6339613795280457')]

        Args:
            word: کلمه‌ای که می‌خواهید واژگان مرتبط با آن را بدانید.
            topn: تعداد کلمات مرتبطی که می‌خواهید برگردانده شود.

        Returns:
            لیستی از تاپل‌های [`کلمهٔ مرتبط`, `میزان ارتباط`].

        """
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)
        return self.model.most_similar(word, topn=topn)

    def get_normal_vector(self: "WordEmbedding", word: str) -> Type[ndarray]:
        """بردار امبدینگ نرمالایزشدهٔ کلمه ورودی را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.get_normal_vector('سرباز')
            array([ 8.99544358e-03,  2.76231226e-02, -1.06164828e-01, ..., -9.45233554e-02, -7.59726465e-02, -8.96625668e-02], dtype=float32)

        Args:
            word: کلمه‌ای که می‌خواهید بردار متناظر با آن را بدانید.

        Returns:
            لیست بردار نرمالایزشدهٔ مرتبط با کلمهٔ ورودی.

        """
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)

        return self.model.get_vector(word=word, norm=True)


class SentEmbedding:
    """این کلاس شامل توابعی برای تبدیل جمله به برداری از اعداد است.

    Args:
        model_path: مسیر فایل امبدینگ.

    """

    def __init__(self: "SentEmbedding", model_path: str = None) -> None:
        if model_path:
            self.load_model(model_path)

    def load_model(self: "SentEmbedding", model_path: str) -> None:
        """فایل امبدینگ را بارگذاری می‌کند.

        Examples:
            >>> sentEmbedding = SentEmbedding()
            >>> sentEmbedding.load_model('sent2vec_model_path')

        Args:
            model_path: مسیر فایل امبدینگ.

        """
        self.model = Doc2Vec.load(model_path)

    def train(
        self: "SentEmbedding",
        dataset_path: str,
        min_count: int = 5,
        workers: int = multiprocessing.cpu_count() - 1,  # noqa: B008
        windows: int = 5,
        vector_size: int = 300,
        epochs: int = 10,
        dest_path: str = None,
    ) -> None:
        """یک فایل امبدینگ doc2vec ترین می‌کند.

        Examples:
            >>> sentEmbedding = SentEmbedding()
            >>> sentEmbedding.train(dataset_path = 'dataset.txt', min_count = 10, worker = 6, windows = 3, vector_size = 250, epochs = 35, dest_path = 'doc2vec_model')

        Args:
            dataset_path: مسیر فایل متنی.
            min_count: مینیموم دفعات تکرار یک کلمه برای حضور آن در لیست کلمات امبدینگ.
            workers: تعداد هسته درگیر برای ترین مدل.
            windows: طول پنجره برای لحاظ کلمات اطراف یک کلمه در ترین آن.
            vector_size: طول وکتور خروجی به ازای هر جمله.
            epochs: تعداد تکرار ترین بر روی کل دیتا.
            dest_path: مسیر مورد نظر برای ذخیره فایل امبدینگ.

        """
        workers = 1 if workers == 0 else workers

        doc = SentenceEmbeddingCorpus(dataset_path)

        model = Doc2Vec(
            min_count=min_count,
            window=windows,
            vector_size=vector_size,
            workers=workers,
        )
        model.build_vocab(doc)
        model.train(doc, total_examples=model.corpus_count, epochs=epochs)

        self.model = model

        print("Model trained.")

        if dest_path is not None:
            model.save(dest_path)
            print("Model saved.")

    def __getitem__(self: "SentEmbedding", sent: str) -> Type[ndarray]:
        """__getitem__."""
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)
        return self.get_sentence_vector(sent)

    def get_sentence_vector(self: "SentEmbedding", sent: str) -> str:
        """جمله‌ای را دریافت می‌کند و بردار امبدینگ متناظر با آن را برمی‌گرداند.

        Examples:
            >>> sentEmbedding = SentEmbedding(sent_embedding_file)
            >>> sentEmbedding.get_sentence_vector('این متن به برداری متناظر با خودش تبدیل خواهد شد')
            array([-0.28460968,  0.04566888, -0.00979532, ..., -0.4701098 , -0.3010612 , -0.18577948], dtype=float32)

        Args:
            sent: جمله‌ای که می‌خواهید بردار امبیدنگ آن را دریافت کنید.

        Returns:
            لیست بردار مرتبط با جملهٔ ورودی.

        """
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)

        tokenized_sent = word_tokenize(sent)
        return self.model.infer_vector(tokenized_sent)

    def similarity(self: "SentEmbedding", sent1: str, sent2: str) -> float:
        """میزان شباهت دو جمله را برمی‌گرداند.

        Examples:
            >>> sentEmbedding = SentEmbedding(sent_embedding_file)
            >>> sentEmbedding.similarity('شیر حیوانی وحشی است', 'پلنگ از دیگر جانوران درنده است')
            0.8748713
            >>> sentEmbedding.similarity('هضم یک محصول پردازش متن فارسی است', 'شیر حیوانی وحشی است')
            0.2379288

        Args:
            sent1: جملهٔ اول.
            sent2: جملهٔ دوم.

        Returns:
            میزان شباهت دو جمله که عددی بین `0` و`1` است.

        """
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)

        return float(
            str(
                self.model.similarity_unseen_docs(
                    word_tokenize(sent1),
                    word_tokenize(sent2),
                ),
            ),
        )


class SentenceEmbeddingCorpus:
    """SentenceEmbeddingCorpus."""

    def __init__(self: "SentenceEmbeddingCorpus", data_path: str) -> None:
        """__init__."""
        self.data_path = data_path

    def __iter__(self: "SentenceEmbeddingCorpus") -> Iterator[TaggedDocument]:
        """__iter__."""
        corpus_path = datapath(self.data_path)
        
        for i, list_of_words in enumerate(Path.open(corpus_path)):
            yield TaggedDocument(
                word_tokenize(Normalizer().normalize(list_of_words)),
                [i],
            )
