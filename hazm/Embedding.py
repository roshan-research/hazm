# coding: utf-8
"""
این ماژول شامل کلاس‌ها و توابعی برای تبدیل کلمه یا متن به برداری از اعداد است.
"""
from . import word_tokenize, Normalizer
import multiprocessing
import warnings
from gensim.test.utils import datapath
from gensim.models.doc2vec import TaggedDocument
from gensim.models import KeyedVectors, Doc2Vec, fasttext
from gensim.scripts.glove2word2vec import glove2word2vec
import os

supported_embeddings = ["fasttext", "keyedvector", "glove"]


class WordEmbedding:
    """این کلاس شامل توابعی برای تبدیل کلمه به برداری از اعداد است.

    Args:
        model_type (str): نوع امبدینگ که می‌تواند یکی از مقادیر ‍`fasttext`, `keyedvector`, `glove` باشد.
        model_path (str, optional): مسیر فایل امبدینگ.
    """

    def __init__(self, model_type, model_path=None):
        if model_type not in supported_embeddings:
            raise KeyError(
                f'Model type "{model_type}" is not supported! Please choose from {supported_embeddings}'
            )
        self.model_type = model_type
        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path):
        """فایل امبدینگ را بارگزاری می‌کند.

        Examples:
                >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
                >>> wordEmbedding.load_model('resources/cc.fa.300.bin')

        Args:
                model_path (str): مسیر فایل امبدینگ.

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
            if not os.path.exists(word2vec_addr):
                _ = glove2word2vec(model_path, word2vec_addr)
            self.model = KeyedVectors.load_word2vec_format(word2vec_addr)
            self.model_type = "keyedvector"
        else:
            raise KeyError(
                f"{self.model_type} not supported! Please choose from {supported_embeddings}"
            )

    def train(
        self,
        dataset_path,
        workers=multiprocessing.cpu_count() - 1,
        vector_size=200,
        epochs=10,
        fasttext_type="skipgram",
        dest_path=None,
    ):
        """یک فایل امبدینگ از نوع fasttext ترین می‌کند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
            >>> wordEmbedding.train(dataset_path = 'dataset.txt', worker = 4, vector_size = 300, epochs = 30, fasttext_type = 'cbow', dest_path = 'fasttext_model')

        Args:
            dataset_path (str): مسیر فایل متنی.
            worker (int, optional): تعداد هسته درگیر برای ترین مدل.
            vector_size (int, optional): طول وکتور خروجی به ازای هر کلمه.
            epochs (int, optional): تعداد تکرار ترین بر روی کل دیتا.
            fasttext_type (str, optional): نوع fasttext مورد نظر برای ترین که میتواند یکی از مقادیر skipgram یا cbow را داشته باشد.
            dest_path (str, optional): مسیر مورد نظر برای ذخیره فایل امبدینگ.

        """

        if self.model_type is not "fasttext":
            self.model = "fasttext"
            warnings.warn(
                f"this function is for training fasttext models only and {self.model_type} is not supported"
            )

        fasttext_model_types = ["cbow", "skipgram"]
        if fasttext_type not in fasttext_model_types:
            raise KeyError(
                f'Model type "{fasttext_type}" is not supported! Please choose from {fasttext_model_types}'
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

    def __getitem__(self, word):
        if not self.model:
            raise AttributeError("Model must not be None! Please load model first.")
        return self.model[word]

    def doesnt_match(self, words):
        """لیستی از کلمات را دریافت می‌کند و کلمهٔ نامرتبط را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.doesnt_match(['سلام' ,'درود' ,'خداحافظ' ,'پنجره'])
            'پنجره'
            >>> wordEmbedding.doesnt_match(['ساعت' ,'پلنگ' ,'شیر'])
            'ساعت'

        Args:
            words (list[str]): لیست کلمات.

        Returns:
            (str): کلمهٔ نامرتبط.
        """

        if not self.model:
            raise AttributeError("Model must not be None! Please load model first.")
        return self.model.doesnt_match(words)

    def similarity(self, word1, word2):
        """میزان شباهت دو کلمه را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.similarity('ایران', 'آلمان')
            0.44988164
            >>> wordEmbedding.similarity('ایران', 'پنجره')
            0.08837362

        Args:
            word1 (str): کلمهٔ اول
            word2 (str): کلمهٔ دوم

        Returns:
            (float): میزان شباهت دو کلمه.
        """

        if not self.model:
            raise AttributeError("Model must not be None! Please load model first.")
        return float(str(self.model.similarity(word1, word2)))

    def get_vocab(self):
        """لیستی از کلمات موجود در فایل امبدینگ را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.get_vocab()
            ['،', 'در', '.', 'و', ...]

        Returns:
            (list[str]): لیست کلمات موجود در فایل امبدینگ.
        """

        if not self.model:
            raise AttributeError("Model must not be None! Please load model first.")
        return self.model.index_to_key

    def nearest_words(self, word, topn=5):
        """کلمات مرتبط با یک واژه را به همراه میزان ارتباط آن برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.nearest_words('ایران', topn = 5)
            [('ايران', 0.657148540019989'), (جمهوری', 0.6470394134521484'), (آمریکا', 0.635792076587677'), (اسلامی', 0.6354473233222961'), (کشور', 0.6339613795280457')]

        Args:
            word (str): کلمه‌ای که می‌خواهید واژگان مرتبط با آن را بدانید.
            topn (int): تعداد کلمات مرتبطی که می‌خواهید برگردانده شود.
        Returns:
            (list[tuple]): لیستی از تاپل‌های [`کلمهٔ مرتبط`, `میزان ارتباط`].
        """

        if not self.model:
            raise AttributeError("Model must not be None! Please load model first.")
        return self.model.most_similar(word, topn=topn)

    def get_normal_vector(self, word):
        """بردار امبدینگ نرمالایزشدهٔ کلمه ورودی را برمی‌گرداند.

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.get_normal_vector('سرباز')
            array([ 8.99544358e-03,  2.76231226e-02, -1.06164828e-01, ..., -9.45233554e-02, -7.59726465e-02, -8.96625668e-02], dtype=float32)

        Args:
            word (str): کلمه‌ای که می‌خواهید بردار متناظر با آن را بدانید.

        Returns:
            (numpy.ndarray(float32)): لیست بردار نرمالایزشدهٔ مرتبط با کلمهٔ ورودی.
        """

        if not self.model:
            raise AttributeError("Model must not be None! Please load model first.")

        return self.model.get_vector(word=word, norm=True)


class SentEmbedding:
    """این کلاس شامل توابعی برای تبدیل جمله به برداری از اعداد است.

    Args:
        model_path (str, optional): مسیر فایل امبدینگ.
    """

    def __init__(self, model_path=None):
        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path):
        """فایل امبدینگ را بارگذاری می‌کند.
        Examples:
            >>> sentEmbedding = SentEmbedding()
            >>> sentEmbedding.load_model('sent2vec_model_path')
        Args:
            model_path (str): مسیر فایل امبدینگ.

        """

        self.model = Doc2Vec.load(model_path)

    def train(
        self,
        dataset_path,
        min_count=5,
        workers=multiprocessing.cpu_count() - 1,
        windows=5,
        vector_size=300,
        epochs=10,
        dest_path=None,
    ):
        """یک فایل امبدینگ doc2vec ترین می‌کند.

        Examples:
            >>> sentEmbedding = SentEmbedding()
            >>> sentEmbedding.train(dataset_path = 'dataset.txt', min_count = 10, worker = 6, windows = 3, vector_size = 250, epochs = 35, dest_path = 'doc2vec_model')

        Args:
            dataset_path (str): مسیر فایل متنی.
            min_count (int, optional): مینیموم دفعات تکرار یک کلمه برای حضور آن در لیست کلمات امبدینگ.
            worker (int, optional): تعداد هسته درگیر برای ترین مدل.
            wondows (int, optional): طول پنجره برای لحاظ کلمات اطراف یک کلمه در ترین آن.
            vector_size (int, optional): طول وکتور خروجی به ازای هر جمله.
            epochs (int, optional): تعداد تکرار ترین بر روی کل دیتا.
            dest_path (str, optional): مسیر مورد نظر برای ذخیره فایل امبدینگ.

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

    def __getitem__(self, sent):
        if not self.model:
            raise AttributeError("Model must not be None! Please load model first.")
        return self.get_sentence_vector(sent)

    def get_sentence_vector(self, sent):
        """جمله‌ای را دریافت می‌کند و بردار امبدینگ متناظر با آن را برمی‌گرداند.

        Examples:
            >>> sentEmbedding = SentEmbedding(sent_embedding_file)
            >>> sentEmbedding.get_sentence_vector('این متن به برداری متناظر با خودش تبدیل خواهد شد')
            array([-0.28460968,  0.04566888, -0.00979532, ..., -0.4701098 , -0.3010612 , -0.18577948], dtype=float32)

        Args:
            sent (str): جمله‌ای که می‌خواهید بردار امبیدنگ آن را دریافت کنید.

        Returns:
            (numpy.ndarray(float32)): لیست بردار مرتبط با جملهٔ ورودی.
        """

        if not self.model:
            raise AttributeError("Model must not be None! Please load model first.")
        else:
            tokenized_sent = word_tokenize(sent)
            return self.model.infer_vector(tokenized_sent)

    def similarity(self, sent1, sent2):
        """میزان شباهت دو جمله را برمی‌گرداند.

        Examples:
            >>> sentEmbedding = SentEmbedding(sent_embedding_file)
            >>> sentEmbedding.similarity('شیر حیوانی وحشی است', 'پلنگ از دیگر جانوران درنده است')
            0.8748713
            >>> sentEmbedding.similarity('هضم یک محصول پردازش متن فارسی است', 'شیر حیوانی وحشی است')
            0.2379288

        Args:
            sent1 (str): جملهٔ اول.
            sent2 (str): جملهٔ دوم.

        Returns:
            (float): میزان شباهت دو جمله که عددی بین `0` و`1` است.
        """

        if not self.model:
            raise AttributeError("Model must not be None! Please load model first.")
        else:
            return float(
                str(
                    self.model.similarity_unseen_docs(
                        word_tokenize(sent1), word_tokenize(sent2)
                    )
                )
            )


class SentenceEmbeddingCorpus:
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        corpus_path = datapath(self.data_path)
        normalizer = Normalizer()
        for i, list_of_words in enumerate(open(corpus_path)):
            yield TaggedDocument(
                word_tokenize(normalizer.normalize(list_of_words)), [i]
            )
