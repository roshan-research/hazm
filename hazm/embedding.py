"""این ماژول شامل کلاس‌ها و توابعی برای تبدیل کلمه یا متن به برداری از اعداد است."""
import multiprocessing
import os
import warnings
from pathlib import Path
from typing import Any
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type

import fasttext as fstxt
import numpy as np
import smart_open
from gensim.models import Doc2Vec
from gensim.models import KeyedVectors
from gensim.models import fasttext
from gensim.models.callbacks import CallbackAny2Vec
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
        model_path: Optional[str] = None,
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
            >>> wordEmbedding.load_model('word2vec.bin') # doctest: +ELLIPSIS
            ...

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
        min_count: int = 5,
        fasttext_type: str = "skipgram",
        dest_path: str = "fasttext_word2vec_model.bin",
    ) -> None:
        """یک فایل امبدینگ از نوع fasttext ترین می‌کند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.train(dataset_path = 'dataset.txt', workers = 4, vector_size = 300, epochs = 30, fasttext_type = 'cbow', dest_path = 'fasttext_model') # doctest: +ELLIPSIS
            ...

        Args:
            dataset_path: مسیر فایل متنی.
            workers: تعداد هسته درگیر برای ترین مدل.
            vector_size: طول وکتور خروجی به ازای هر کلمه.
            epochs: تعداد تکرار ترین بر روی کل دیتا.
            min_count:  حداقل تعداد تکرار یک کلمه برای قرارگیری آن در مدل امبدینگ.
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

        print("training model...")
        model = fstxt.train_unsupervised(
            dataset_path,
            model=fasttext_type,
            dim=vector_size,
            epoch=epochs,
            thread=workers,
            min_count = min_count,
        )

        print("Model trained.")

        print("saving model...")
        model.save_model(dest_path)
        print("Model saved.")

        print("loading model...")
        self.load_model(model_path=dest_path)
        print("model loaded.")

    def __getitem__(self: "WordEmbedding", word: str) -> Type[ndarray]:
        """__getitem__."""
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)
        return self.model[word]

    def doesnt_match(self: "WordEmbedding", words: List[str]) -> str:
        """لیستی از کلمات را دریافت می‌کند و کلمهٔ نامرتبط را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.load_model('word2vec.bin')
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
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.load_model('word2vec.bin')
            >>> wordEmbedding.similarity('ایران', 'آلمان')
            0.72231203
            >>> wordEmbedding.similarity('ایران', 'پنجره')
            0.04535884

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

    def nearest_words(
        self: "WordEmbedding",
        word: str,
        topn: int = 5,
    ) -> List[Tuple[str, str]]:
        """کلمات مرتبط با یک واژه را به همراه میزان ارتباط آن برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.load_model('word2vec.bin')
            >>> wordEmbedding.nearest_words('ایران', topn = 5)
            [('ایران،', 0.8742443919181824), ('کشور', 0.8735059499740601), ('کشورمان', 0.8443885445594788), ('ایران\u200cبه', 0.8271722197532654), ('خاورمیانه', 0.8266966342926025)]


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
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.load_model('word2vec.bin')
            >>> result = wordEmbedding.get_normal_vector('سرباز')
            >>> isinstance(result, ndarray)
            True

        Args:
            word: کلمه‌ای که می‌خواهید بردار متناظر با آن را بدانید.

        Returns:
            لیست بردار نرمالایزشدهٔ مرتبط با کلمهٔ ورودی.

        """
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)

        return self.model.get_vector(word=word, norm=True)

    def get_vocabs(self: "WordEmbedding") -> List[str]:
        """لیستی از کلمات موجود در فایل امبدینگ را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.load_model('word2vec.bin')
            >>> wordEmbedding.get_vocabs() # doctest: +ELLIPSIS
            ['و', '.', 'در', '،', ...]

        Returns:
            لیست کلمات موجود در فایل امبدینگ.

        """
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)
        return self.model.index_to_key

    def get_vocab_to_index(self: "WordEmbedding") -> dict:
        """دیکشنری برمی‌گرداند که هر کلمه موجود در فایل امبدینگ را به ایندکس آن کلمه در لیست بردارها مپ می‌کند.


        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.load_model('word2vec.bin)
            >>> vocab_to_index = wordEmbedding.get_vocab_to_index()
            >>> index = vocab_to_index['سلام']
            >>> vocabs = wordEmbedding.get_vocabs()
            >>> vocabs[index]
            'سلام'

        Returns:
            دیکشنری که هر کلمه را به ایندکس آن مپ می‌کند.
        """
        return self.model.key_to_index

    def get_vectors(self: "WordEmbedding") -> Type[ndarray]:
        """وکتورهای توصیف کننده کلمات را برمیگرداند.(عناصر این وکتور با وکتور کلمات تابع  get_vocabs هم‌اندیس هستند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.load_model('resorces/word2vec.bin')
            >>> vectors = wordEmbedding.get_vectors()
            >>> all(vectors[wordEmbedding.get_vocab_to_index()['سلام']] == wordEmbedding['سلام'])
            True

        Returns:
            تمامی وکتور بیان‌کننده کلمات.
        """
        return self.model.vectors

    def get_vector_size(self: "WordEmbedding") -> int:
        """طول وکتور بیان‌کننده هر کلمه در مدل را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.load_model('resorces/word2vec.bin')
            >>> wordEmbedding.get_vector_size()
            300


        Returns:
            طول وکتور بیان‌کننده کلمات.

        """
        return self.model.vector_size


class SentenceEmbeddingCorpus:
    """SentenceEmbeddingCorpus."""

    def __init__(self: "SentenceEmbeddingCorpus", data_path: str) -> None:
        """__init__."""
        self.data_path = data_path

    def __iter__(self: "SentenceEmbeddingCorpus") -> Iterator[TaggedDocument]:
        """__iter__."""
        for i, list_of_words in enumerate(smart_open.open(self.data_path)):
            yield TaggedDocument(
                word_tokenize(Normalizer().normalize(list_of_words)),
                [i],
            )

class CallbackSentEmbedding(CallbackAny2Vec):
    def __init__(self: "CallbackSentEmbedding") -> None:
        self.epoch = 0

    def on_epoch_end(self: "CallbackSentEmbedding", model: Doc2Vec):
        print(f"Epoch {self.epoch+1} of {model.epochs}...")
        self.epoch += 1


class SentEmbedding:
    """این کلاس شامل توابعی برای تبدیل جمله به برداری از اعداد است.

    Args:
        model_path: مسیر فایل امبدینگ.

    """

    def __init__(self: "SentEmbedding", model_path: Optional[str] = None) -> None:
        if model_path:
            self.load_model(model_path)
            self.__load_word_embedding_model()

    def __load_word_embedding_model(self: "SentEmbedding") -> None:
        self.word_embedding = WordEmbedding(model_type="keyedvector")
        self.word_embedding.model = self.model.wv

    def load_model(self: "SentEmbedding", model_path: str) -> None:
        """فایل امبدینگ را بارگذاری می‌کند.

        Examples:
            >>> sentEmbedding = SentEmbedding()
            >>> sentEmbedding.load_model('sent2vec.model') # doctest: +ELLIPSIS
            ...

        Args:
            model_path: مسیر فایل امبدینگ.

        """
        self.model = Doc2Vec.load(model_path)
        self.__load_word_embedding_model()

    def train(
        self: "SentEmbedding",
        dataset_path: str,
        min_count: int = 5,
        workers: int = multiprocessing.cpu_count() - 1,  # noqa: B008
        windows: int = 5,
        vector_size: int = 300,
        epochs: int = 10,
        dest_path: str = "gensim_sent2vec.model",
    ) -> None:
        """یک فایل امبدینگ doc2vec ترین می‌کند.

        Examples:
            >>> sentEmbedding = SentEmbedding()
            >>> sentEmbedding.train(dataset_path = 'dataset.txt', min_count = 10, workers = 6, windows = 3, vector_size = 250, epochs = 35, dest_path = 'doc2vec_model') # doctest: +ELLIPSIS
            ...

        Args:
            dataset_path: مسیر فایل متنی.
            min_count: حداقل تعداد تکرار یک کلمه برای قرارگیری آن در مدل امبدینگ.
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
        print("building vocab...")
        model.build_vocab(doc)
        print("training model...")
        callbacks = [CallbackSentEmbedding()]
        model.train(doc, total_examples=model.corpus_count, epochs=epochs, callbacks=callbacks)

        model.dv.vectors = np.array([[]])
        self.model = model
        self.__load_word_embedding_model()
        print("Model trained.")

        print("saving model...")
        model.save(dest_path)
        print("Model saved.")

    def __getitem__(self: "SentEmbedding", sent: str) -> Type[ndarray]:
        """__getitem__."""
        if not self.model:
            msg = "Model must not be None! Please load model first."
            raise AttributeError(msg)
        return self.get_sentence_vector(sent)

    def get_sentence_vector(self: "SentEmbedding", sent: str) -> ndarray:
        """جمله‌ای را دریافت می‌کند و بردار امبدینگ متناظر با آن را برمی‌گرداند.

        Examples:
            >>> sentEmbedding = SentEmbedding()
            >>> sentEmbedding.load_model("sent2vec.model")
            >>> result = sentEmbedding.get_sentence_vector('این متن به برداری متناظر با خودش تبدیل خواهد شد')
            >>> isinstance(result, ndarray)
            True

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
            >>> sentEmbedding = SentEmbedding()
            >>> sentEmbedding.load_model("sent2vec.model")
            >>> result = sentEmbedding.similarity('شیر حیوانی وحشی است', 'پلنگ از دیگر جانوران درنده است')
            >>> isinstance(result, float)
            True
            >>> result = sentEmbedding.similarity('هضم یک محصول پردازش متن فارسی است', 'شیر حیوانی وحشی است')
            >>> isinstance(result, float)
            True

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

    def get_vector_size(self: "WordEmbedding") -> int:
        """طول وکتور بیان‌کننده هر جمله در مدل را برمی‌گرداند.

        Examples:
            >>> sentEmbedding = SentEmbedding()
            >>> sentEmbedding.load_model("sent2vec.model")
            >>> sentEmbedding.get_vector_size()
            300


        Returns:
            طول وکتور بیان‌کننده جملات.

        """
        return self.model.vector_size
