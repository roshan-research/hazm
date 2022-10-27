from . import word_tokenize
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
import fasttext, os

supported_embeddings = ['fasttext', 'keyedvector', 'glove']


class WordEmbedding:
    def __init__(self, model_type, model_path=None):
        if model_type not in supported_embeddings:
            raise KeyError(f'Model type "{model_type}" is not supported! Please choose from {supported_embeddings}')
        if model_path:
            self.model = self.load_model(model_path)       
        self.model_type = model_type    


    def load_model(self, model_file):
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
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return self.model.doesnt_match(word_tokenize(txt))

    
    def similarity(self, word1, word2):
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        return self.model.similarity(word1, word2)
    


    def get_vocab(self):
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        if self.model_type == 'fasttext':
            return self.model.get_words(include_freq=False)
        else:
            return self.model.index_to_key
        
    

    def nearest_words(self, word, topn):
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        if self.model_type == 'fasttext':
            return self.model.get_nearest_neighbors(word, 10)
        else:
            return self.model.most_similar(word, topn=topn)
    

    def get_normal_vector(self, word):
        if not self.model:
            raise AttributeError('Model must not be None! Please load model first.')
        
        return self.model.get_vector(key=word, norm=True)

    


