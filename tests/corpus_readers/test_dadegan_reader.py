import pytest
from hazm import DadeganReader
from hazm import tree2brackets

@pytest.fixture(scope='module')
def dadegan_reader():
    return DadeganReader('corpora/dadegan.conll')

def test_sents(dadegan_reader):    
    actual = next(dadegan_reader.sents())
    expected = [('این', 'DET'), ('میهمانی', 'N'), ('به', 'P'), ('منظور', 'Ne'), ('آشنایی', 'Ne'), ('هم‌تیمی‌های', 'Ne'), ('او', 'PRO'), ('با', 'P'), ('غذاهای', 'Ne'), ('ایرانی', 'AJ'), ('ترتیب', 'N'), ('داده_شد', 'V'), ('.', 'PUNC')]
    assert actual == expected

def test_chunked_trees(dadegan_reader): 
    actual = tree2brackets(next(dadegan_reader.chunked_trees()))
    expected = '[این میهمانی NP] [به PP] [منظور آشنایی هم‌تیمی‌های او NP] [با PP] [غذاهای ایرانی NP] [ترتیب داده_شد VP] .'
    assert actual == expected