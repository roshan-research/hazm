import pytest
from numpy import ndarray

class TestWordEmbedding:   
    

    #def test_train(self, word_embedding):        
    #    assert word_embedding.train(dataset_path = 'dataset.txt', workers = 4, vector_size = 300, epochs = 30, fasttext_type = 'cbow', dest_path = 'fasttext_model') == None

    def test_doesnt_match(self, word_embedding):    
        assert word_embedding.doesnt_match(['سلام', 'درود', 'خداحافظ', 'پنجره']) == 'پنجره'
        assert word_embedding.doesnt_match(['ساعت', 'پلنگ', 'شیر']) == 'ساعت'

    def test_similarity(self, word_embedding):    
        assert word_embedding.similarity('ایران', 'آلمان') == 0.72231203
        assert word_embedding.similarity('ایران', 'پنجره') ==  0.04535884

    def test_get_vocab(self, word_embedding):    
        assert len(word_embedding.get_vocab()) == 186659

    def test_nearest_words(self, word_embedding):    
        assert word_embedding.nearest_words('ایران', topn = 5) == [('ایران،', 0.8742443919181824), ('کشور', 0.8735059499740601), ('کشورمان', 0.8443885445594788), ('ایران\u200cبه', 0.8271722197532654), ('خاورمیانه', 0.8266966342926025)]


    def test_normal_vector(self, word_embedding):    
        assert isinstance(word_embedding.get_normal_vector('سرباز'), ndarray) == True
        

class TestSentEmbedding:    
    

    #def test_train(self, sent_embedding):        
    #    assert sent_embedding.train(dataset_path = 'dataset.txt', min_count = 10, workers = 6, windows = 3, vector_size = 250, epochs = 35, dest_path = 'doc2vec_model') == None

    def test_get_sentence_vector(self, sent_embedding):        
        assert isinstance(sent_embedding.get_sentence_vector('این متن به برداری متناظر با خودش تبدیل خواهد شد'),ndarray) == True        
        

    def test_get_sentence_vector(self, sent_embedding):        
        assert isinstance(sent_embedding.similarity('شیر حیوانی وحشی است', 'پلنگ از دیگر جانوران درنده است'),float) == True
        assert isinstance(sent_embedding.similarity('هضم یک محصول پردازش متن فارسی است', 'شیر حیوانی وحشی است'),float) == True
        

    

