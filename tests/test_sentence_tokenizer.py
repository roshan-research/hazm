class TestSentenceTokenizer:
    
    def test_sentence_tokenizer(self, sentence_tokenizer):
        actual = sentence_tokenizer.tokenize('جدا کردن ساده است. تقریبا البته!')
        expected = ['جدا کردن ساده است.', 'تقریبا البته!']
        assert actual == expected