from . import word_tokenize
from gensim.models import KeyedVectors, doc2vec
from gensim.scripts.glove2word2vec import glove2word2vec
import fasttext, os

supported_embeddings = ['fasttext', 'keyedvector', 'glove']


class WordEmbedding:
    """ .این کلاس شامل توابعی مرتبط با تبدیل کلمه به برداری از اعداد یا همان امبدینگ است

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


    def load_model(self, model_file):
        """فایل امبدینگ را بارگذاری می‌کند

		Examples:
			>>> wordEmbedding = WordEmbedding(model_type = 'fasttext')
			>>> wordEmbedding.load_model('fasttext_embedding_path')

            >>> wordEmbedding = WordEmbedding(model_type = 'keyedvector')
			>>> wordEmbedding.load_model('keyedvector_embedding_path')

            >>> wordEmbedding = WordEmbedding(model_type = 'glove')
			>>> wordEmbedding.load_model('glove_embedding_path')

		Args:
			model_file (str): مسیر فایل امبدینگ
        
        """

        if self.model_type == 'fasttext':
            self.model = fasttext.load_model(model_file)
        elif self.model_type == 'keyedvector':
            if model_file.endswith('bin'):
                self.model = KeyedVectors.load_word2vec_format(model_file, binary=True)
            else:
                self.model = KeyedVectors.load_word2vec_format(model_file)
        elif self.model_type == 'glove':
            word2vec_addr = str(model_file) + '_word2vec_format.vec'
            if not os.path.exists(word2vec_addr):
                _ = glove2word2vec(model_file, word2vec_addr)
            self.model = KeyedVectors.load_word2vec_format(word2vec_addr)
            self.model_type = 'keyedvector'
        else:
            raise KeyError(f'{self.model_type} not supported! Please choose from {supported_embeddings}')

    
    def __getitem__(self, word):
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return self.model[word]
    

    def doesnt_match(self, txt):
        ''' کلمه‌ نامرتبط را پیدا می‌کند

        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'model_path')
            >>> wordEmbedding.doesnt_match('سلام درود خداحافظ پنجره')
            'پنجره'

        Args:
            txt (str): متنی شامل کلمات 

		Returns:
			(str): کلمه نامرتبط با سایر کلمات در متن
        '''
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return self.model.doesnt_match(word_tokenize(txt))

    
    def similarity(self, word1, word2):
        ''' میزان شباهت دو کلمه را با عددی بین ۱- تا ۱ گزارش می‌کند
        
        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'model_path')
            >>> wordEmbedding.similarity('ایران', 'آلمان')
            0.42917365

            >>> wordEmbedding.similarity('ایران', 'پنجره')
            -0.050690148

        Args:
            word1 (str): کلمه اول
            word2 (str): کلمه دوم

        Returns:
            (numpy.float32): میزان شباهت دو کلمه
        '''

        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return self.model.similarity(word1, word2)
    


    def get_vocab(self):
        ''' تمامی کلمات موجود در امبدینگ را گزارش می‌دهد
        
        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'model_path')
            >>> wordEmbedding.get_vocab()
            ['در', 'به', 'از', 'که', 'این', 'the', 'می', ...]

        Returns:
            (list[str]): تمام کلمات موجود در امبدینگ
        '''

        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        if self.model_type == 'fasttext':
            return self.model.get_words(include_freq=False)
        else:
            return self.model.index_to_key
        
    

    def nearest_words(self, word, topn=10):
        ''' مرتبط‌ترین کلمات را با کلمه ورودی گزارش می‌دهد
        
        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'model_path')
            >>> wordEmbedding.nearest_words('ایران', topn = 5)
            [('کشور', 0.6297125220298767), ('کشورمان', 0.6277097463607788), ('آمریکا', 0.6062831878662109), ('روسیه', 0.5703828930854797), ('ایرانی', 0.541590690612793)]

        Args:
            word (str): کلمه‌ای که می‌خواهیم کلمات مرتبط با آن را بدانیم
            topn (int): تعداد کلمات مرتبط با ورودی قبلی

        Returns:
            (list[tuple]):  لیستی حاوی کلمات مرتبط با کلمه ورودی و میزان شباهتشان
        '''
        
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        if self.model_type == 'fasttext':
            return self.model.get_nearest_neighbors(word, topn)
        else:
            return self.model.most_similar(word, topn=topn)
    

    def get_normal_vector(self, word):
        ''' بردار امبدینگ نرمال‌شده کلمه ورودی را گزارش می‌دهد.
        
        Examples:
            >>> wordEmbedding = WordEmbedding(model_type = 'model_type', model_path = 'model_path')
            >>> wordEmbedding.get_normal_vector('سرباز')
            [ 7.71598741e-02,  4.07299027e-02,  3.12963873e-02, ..., -3.78610939e-02, -9.01247039e-02,  8.66614655e-02]     

        Args:
            word (str): کلمه‌ای که می‌خواهیم بردار نرمال متناظر با آن را بدانیم

        Returns:
            (numpy.ndarray(float32)): لیستی حاوی کلمات مرتبط با کلمه ورودی
        '''
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        
        return self.model.get_vector(key=word, norm=True)



class SentEmbedding:

        def __init__(self, model_path=None):
            if model_path:
                self.load_model(model_path)


        def load_model(self, model_path):
            self.model = doc2vec.load(model_path)


        def __getitem__(self, sent):
            if not self.model:
                raise AttributeError('Model must not be None! Please load model first.')
            return self.sent_to_vec(sent)


        def sent_to_vec(self, sent):
            if not self.model:
                raise AttributeError('Model must not be None! Please load model first.')
            else:
                tokenized_sent = word_tokenize(sent)
                return self.model.infer_vector(tokenized_sent)


        def similarity(self, sent1, sent2):
            if not self.model:
                raise AttributeError('Model must not be None! Please load model first.')
            else:
                tokenized_sent1 = word_tokenize(sent1)
                tokenized_sent2 = word_tokenize(sent2)
                return self.model.similarity_unseen_docs(tokenized_sent1, tokenized_sent2)


        
        


        


    





