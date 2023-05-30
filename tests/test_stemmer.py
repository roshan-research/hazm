import pytest

class TestStemmer:
    
    @pytest.mark.parametrize("word,expected", [        
        
        ("کتابی", "کتاب"),             
        ("کتاب‌ها", "کتاب"),             
        ("کتاب‌هایی", "کتاب"),             
        ("کتابهایشان", "کتاب"),             
        ("اندیشه‌اش", "اندیشه"),             
        ("خانهٔ", "خانه"),             
        ("محبوب‌ترین‌ها", "محبوب"),             
        ("  ", "  "),        
        ("", ""),
    ])

    def test_stem(self, stemmer, word, expected):       
        assert stemmer.stem(word) == expected