#from . import word_tokenize
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import fasttext, os

supported_embeddings = ['fasttext', 'keyedvector', 'glove']


class WordEmbedding:
    """ .این کلاس شامل توابعی مرتبط با تبدیل کلمه به بردار اعداد یا همان امبدینگ است

    Args:
		model_type (str): باشد ['fasttext', 'keyedvector', 'glove']  نام امبدینگ مورد نیاز که می‌تواند یکی از مقادیر
        model_path (str, optional): مسیر فایل امبدینگ
    """

    def __init__(self, model_type, model_path=None):
        if model_type not in supported_embeddings:
            raise KeyError(f'Model type "{model_type}" is not supported! Please choose from {supported_embeddings}')
        self.model_type = model_type
        if model_path:
            self.model = self.load_model(model_path)           


    def load_model(self, model_file):
        """فایل امبدینگ را بارگذاری می‌کند

		Examples:
			>>> wordEmbedding = WordEmbedding()
			>>> wordEmbedding.load_model('fasttext')

			>>> wordEmbedding.load_model('keyedvector')

			>>> wordEmbedding.load_model('glove')

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
    

    # def doesnt_match(self, txt):
    #     ''' کلمه‌ نامرتبط را پیدا می‌کند


    #     Args:
    #         txt (str): متنی شامل کلمات 

	# 	Returns:
	# 		(str): کلمه نامرتبط با سایر کلمات در متن
    #     '''
    #     if not self.model:
    #         raise AttributeError('Model must not be None! Please load model first.')
    #     return self.model.doesnt_match(word_tokenize(txt))

    
    def similarity(self, word1, word2):
        ''' میزان شباهت دو کلمه را با عددی بین ۰ تا ۱ گزارش می‌کند
        

        Args:
            word1 (str): کلمه اول
            word2 (str): کلمه دوم

        Returns:
            (List[str]): میزان شباهت دو کلمه
        '''

        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return self.model.similarity(word1, word2)
    


    def get_vocab(self):
        ''' تمامی کلمات موجود در امبدینگ را گزارش می‌دهد
        

        Returns:
            (): تمام کلمات موجود در امبدینگ
        '''

        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        if self.model_type == 'fasttext':
            return self.model.get_words(include_freq=False)
        else:
            return self.model.index_to_key
        
    

    def nearest_words(self, word, topn):
        ''' مرتبط‌ترین کلمات را با کلمه ورودی گزارش می‌دهد
        
        Args:
            word (str): کلمه‌ای که می‌خواهیم کلمات مرتبط با آن را بدانیم
            topn (int): تعداد کلمات مرتبط با ورودی قبلی


        Returns:
            (list[str]): لیستی حاوی کلمات مرتبط با کلمه ورودی
        '''
        
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        if self.model_type == 'fasttext':
            return self.model.get_nearest_neighbors(word, 10)
        else:
            return self.model.most_similar(word, topn=topn)
    

    def get_normal_vector(self, word):
        ''' مرتبط‌ترین کلمات را با کلمه ورودی گزارش می‌دهد
        
        Args:
            word (str): کلمه‌ای که می‌خواهیم کلمات مرتبط با آن را بدانیم

        Returns:
            (list[str]): لیستی حاوی کلمات مرتبط با کلمه ورودی
        '''
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        
        return self.model.get_vector(key=word, norm=True)



if __name__ == '__main__':
    embedding = WordEmbedding(model_type='keyedvector', model_path='/home/sobhe/baaz/myWord2vec/resources/downloading/skipgram/model.txt')
    print(type(embedding.get_vocab()))





