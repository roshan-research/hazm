# coding: utf-8


from __future__ import unicode_literals
from hazm import word_tokenize
from gensim.models import KeyedVectors, Doc2Vec, fasttext
from gensim.scripts.glove2word2vec import glove2word2vec
import os

supported_embeddings = ['fasttext', 'keyedvector', 'glove']


class WordEmbedding:
    """.این کلاس شامل توابعی مرتبط با تبدیل کلمه به برداری از اعداد، یا همان امبدینگ کلمه است

    Args:
		model_type (str): باشد ['fasttext', 'keyedvector', 'glove']  نام امبدینگ مورد نیاز که می‌تواند یکی از مقادیر
        model_path (str, optional): مسیر فایل امبدینگ
    """


    def __init__(self, model_type, model_path=None):
        if model_type not in supported_embeddings:
            raise KeyError(f'Model type "{model_type}" is not supported! Please choose from {supported_embeddings}')
        self.model_type = model_type
        if model_path:
            self.load_model(model_path)           


    def load_model(self, model_path):
        """.فایل امبدینگ را بارگذاری می‌کند

		Examples:
			>>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
			>>> wordEmbedding.load_model('resources/cc.fa.300.bin')

		Args:
			model_path (str): مسیر فایل امبدینگ
        
        """

        if self.model_type == 'fasttext':
            self.model = fasttext.load_facebook_model(model_path).wv
        elif self.model_type == 'keyedvector':
            if model_path.endswith('bin'):
                self.model = KeyedVectors.load_word2vec_format(model_path, binary=True)
            else:
                self.model = KeyedVectors.load_word2vec_format(model_path)
        elif self.model_type == 'glove':
            word2vec_addr = str(model_path) + '_word2vec_format.vec'
            if not os.path.exists(word2vec_addr):
                _ = glove2word2vec(model_path, word2vec_addr)
            self.model = KeyedVectors.load_word2vec_format(word2vec_addr)
            self.model_type = 'keyedvector'
        else:
            raise KeyError(f'{self.model_type} not supported! Please choose from {supported_embeddings}')

    
    def __getitem__(self, word):
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return self.model[word]
    

    def doesnt_match(self, words):
        '''.کلمه‌ نامرتبط را پیدا می‌کند

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.doesnt_match(['سلام' ,'درود' ,'خداحافظ' ,'پنجره'])
            'پنجره'

        Args:
            words (list[str]): لیستی از کلمات مورد نظر

		Returns:
			(str): کلمه نامرتبط با سایر کلمات در لیست
        '''

        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return self.model.doesnt_match(words)

    
    def similarity(self, word1, word2):
        '''.میزان شباهت دو کلمه را گزارش می‌کند
        
        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.similarity('ایران', 'آلمان')
            0.44988164

            >>> wordEmbedding.similarity('ایران', 'پنجره')
            0.08837362

        Args:
            word1 (str): کلمه اول
            word2 (str): کلمه دوم

        Returns:
            (float): میزان شباهت دو کلمه
        '''

        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return float(str(self.model.similarity(word1, word2)))
    

    def get_vocab(self):
        '''.تمامی کلمات موجود در امبدینگ را گزارش می‌دهد
        
        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.get_vocab()
            ['،', 'در', '.', 'و', ...]

        Returns:
            (list[str]): تمام کلمات موجود در امبدینگ
        '''

        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return self.model.index_to_key
        
    

    def nearest_words(self, word, topn=5):
        '''.مرتبط‌ترین کلمات را با کلمه ورودی گزارش می‌دهد
        
        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.nearest_words('ایران', topn = 5)
            [('ايران', 0.657148540019989), ('جمهوری', 0.6470394134521484), ('آمریکا', 0.635792076587677), ('اسلامی', 0.6354473233222961), ('کشور', 0.6339613795280457)]
        Args:
            word (str): کلمه‌ای که می‌خواهیم کلمات مرتبط با آن را بدانیم
            topn (int): تعداد کلمات مرتبط با ورودی قبلی

        Returns:
            (list[tuple]):  لیستی حاوی کلمات مرتبط با کلمه ورودی و میزان شباهتشان
        '''
        
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return self.model.most_similar(word, topn=topn)
    

    def get_normal_vector(self, word):
        '''.بردار امبدینگ نرمال‌شده کلمه ورودی را گزارش می‌دهد.
        
        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'resources/cc.fa.300.bin')
            >>> wordEmbedding.get_normal_vector('سرباز')
            array([ 8.99544358e-03,  2.76231226e-02, -1.06164828e-01, ..., -9.45233554e-02, -7.59726465e-02, -8.96625668e-02], dtype=float32)

        Args:
            word (str): کلمه‌ای که می‌خواهیم بردار نرمال متناظر با آن را بدانیم

        Returns:
            (numpy.ndarray(float32)): لیست بردار نرمال‌شده‌ مرتبط با کلمه ورودی
        '''

        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        
        return self.model.get_vector(word=word, norm=True)



class SentEmbedding:
        ''' .این کلاس شامل توابعی مرتبط با تبدیل جمله به برداری از اعداد، یا همان امبدینگ جمله است

        Args:
            model_path (str, optional): مسیر فایل امبدینگ
        '''


        def __init__(self, model_path=None):
            if model_path:
                self.load_model(model_path)


        def load_model(self, model_path):
            '''.فایل امبدینگ را بارگذاری می‌کند

            Examples:
                >>> sentEmbedding = SentEmbedding()
                >>> sentEmbedding.load_model('sent2vec_model_path')

            Args:
                model_path (str): مسیر فایل امبدینگ
            
            '''            

            self.model = Doc2Vec.load(model_path)


        def __getitem__(self, sent):
            if not self.model:
                raise AttributeError('Model must not be None! Please load model first.')
            return self.get_sentence_vector(sent)


        def get_sentence_vector(self, sent):
            '''.جمله مورد نظر را دریافت و بردار امبدینگ متناظر با آن را گزارش می‌دهد

            Examples:
                >>> sentEmbedding = SentEmbedding(sent_embedding_file)
                >>> sentEmbedding.get_sentence_vector('این متن به برداری متناظر با خودش تبدیل خواهد شد')
                array([-0.28460968,  0.04566888, -0.00979532, ..., -0.4701098 , -0.3010612 , -0.18577948], dtype=float32)

            Args:
                sent (str): جمله‌ای که می‌خواهیم بردار مرتبط با آن را بدانیم

            Returns:
                (numpy.ndarray(float32)): لیست بردار مرتبط با جمله ورودی
            '''

            if not self.model:
                raise AttributeError('Model must not be None! Please load model first.')
            else:
                tokenized_sent = word_tokenize(sent)
                return self.model.infer_vector(tokenized_sent)


        def similarity(self, sent1, sent2):
            '''.میزان شباهت دو جمله را گزارش می‌دهد
            
            Examples:
                >>> sentEmbedding = SentEmbedding(sent_embedding_file)
                >>> sentEmbedding.similarity('شیر حیوانی وحشی است', 'پلنگ از دیگر حیوانات درنده است')
                0.8748713

                >>> sentEmbedding.similarity('هضم یک محصول پردازش متن فارسی است', 'شیر حیوانی وحشی است')
                0.2379288

            Args:
                sent1 (str): جمله اول
                sent2 (str): جمله دوم

            Returns:
                (float): میزان شباهت دو جمله
            '''

            if not self.model:
                raise AttributeError('Model must not be None! Please load model first.')
            else:
                tokenized_sent1 = word_tokenize(sent1)
                tokenized_sent2 = word_tokenize(sent2)
                return float(str(self.model.similarity_unseen_docs(tokenized_sent1, tokenized_sent2)))
            
            
            