import pytest

from hazm import UniversalDadeganReader
from hazm import tree2brackets


@pytest.fixture(scope="module")
def universal_dadegan_reader():
    return UniversalDadeganReader("corpora/dadegan.conll")

def test_sents(dadegan_reader: UniversalDadeganReader):
    sents = dadegan_reader.sents()
    actual1 = next(sents)
    expected1 = [('هر', 'DET,PREM_AMBAJ'), ('جسمی', 'NOUN,N_IANM'), ('با', 'ADP,PREP'), ('دمای', 'NOUN,N_IANM'), ('بالاتر', 'ADJ,ADJ_AJCM'), ('از', 'ADP,PREP'), ('صفر', 'NOUN,N_IANM'), ('مطلق', 'ADJ,ADJ_AJP'), ('انرژی', 'NOUN,N_IANM'), ('تابش', 'NOUN,N_IANM'), ('خواهد', 'AUX,AUX'), ('کرد', 'VERB,V_ACT'), ('.', 'PUNCT,PUNC')]
    assert actual1 == expected1


