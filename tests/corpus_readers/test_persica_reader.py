import pytest
from hazm import PersicaReader

@pytest.fixture(scope='module')
def persica_reader():
    return PersicaReader('corpora/persica.csv')

def test_docs(persica_reader):    
    actual = next(persica_reader.docs())['id']
    expected = 843656
    assert actual == expected

def test_texts(persica_reader):    
    actual = next(persica_reader.texts()).startswith('وزير علوم در جمع استادان نمونه كشور گفت')
    expected = True
    assert actual == expected