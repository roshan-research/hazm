import pytest
from numpy import ndarray


class TestWordEmbedding:


    #def test_train(self, word_embedding):

    def test_doesnt_match(self: "TestWordEmbedding", word_embedding):
        assert word_embedding.doesnt_match(["سلام", "درود", "خداحافظ", "پنجره"]) == "پنجره"
        assert word_embedding.doesnt_match(["ساعت", "پلنگ", "شیر"]) == "ساعت"

    def test_similarity(self: "TestWordEmbedding", word_embedding):
        assert word_embedding.similarity("ایران", "آلمان") == 0.94321066
        assert word_embedding.similarity("ایران", "پنجره") ==  0.19852939

    def test_get_vocab(self: "TestWordEmbedding", word_embedding):
        assert len(word_embedding.get_vocab()) == 186659

    def test_nearest_words(self: "TestWordEmbedding", word_embedding):
        assert word_embedding.nearest_words("ایران", topn = 5) == [('تاریخی.', 0.9997861385345459), ('نام\u200cگذاری', 0.9993206858634949), ('پناه\u200cجو', 0.9992603063583374), ('قرارگرفت', 0.9990856647491455), ('امدادگری', 0.998709499835968)]


    def test_normal_vector(self: "TestWordEmbedding", word_embedding):
        assert isinstance(word_embedding.get_normal_vector("سرباز"), ndarray) is True


class TestSentEmbedding:


    #def test_train(self, sent_embedding):

    def test_get_sentence_vector(self: "TestSentEmbedding", sent_embedding):
        assert isinstance(sent_embedding.get_sentence_vector("این متن به برداری متناظر با خودش تبدیل خواهد شد"), ndarray) is True


    def test_similarity(self: "TestSentEmbedding", sent_embedding):
        assert isinstance(sent_embedding.similarity("شیر حیوانی وحشی است", "پلنگ از دیگر جانوران درنده است"), float) is True
        assert isinstance(sent_embedding.similarity("هضم یک محصول پردازش متن فارسی است", "شیر حیوانی وحشی است"), float) is True




