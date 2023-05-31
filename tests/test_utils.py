from hazm import words_list
from hazm import stopwords_list

def test_words_list():
    assert words_list()[1] == ('آب', 549005877, ('N', 'AJ'))

def test_stopwords_list():
    assert stopwords_list()[:4] == ['آخرین', 'آقای', 'آمد', 'آمده']


