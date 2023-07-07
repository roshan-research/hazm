import pytest

from hazm import UniversalDadeganReader
from hazm import tree2brackets


@pytest.fixture(scope="module")
def universal_dadegan_reader():
    return UniversalDadeganReader("tests/files/dadegan.conllu")

def test_sents(universal_dadegan_reader: UniversalDadeganReader):
    sents = universal_dadegan_reader.sents()
    actual = next(sents)
    expected = [("هر", "DET,PREM_AMBAJ"), ("جسمی", "NOUN,N_IANM"), ("با", "ADP,PREP"), ("دمای", "NOUN,N_IANM"), ("بالاتر", "ADJ,ADJ_AJCM"), ("از", "ADP,PREP"), ("صفر", "NOUN,N_IANM"), ("مطلق", "ADJ,ADJ_AJP"), ("انرژی", "NOUN,N_IANM"), ("تابش", "NOUN,N_IANM"), ("خواهد", "AUX,AUX"), ("کرد", "VERB,V_ACT"), (".", "PUNCT,PUNC")]
    assert actual == expected

def test_trees(universal_dadegan_reader: UniversalDadeganReader):
    trees = universal_dadegan_reader.trees()
    actual = next(trees).to_conll(10).split("\n")[0]
    expected = "1	هر	هر	DET	PREM_AMBAJ	_	2	det	_	_"
    assert actual == expected

