import conllu
import pytest

from hazm import DadeganReader
from hazm import tree2brackets


@pytest.fixture(scope="module")
def dadegan_reader():
    return DadeganReader("corpora/dadegan.conllu")

def test_sents(dadegan_reader: DadeganReader):
    actual = next(dadegan_reader.sents())
    expected = [("هر", "DET,PREM_AMBAJ"), ("جسمی", "NOUN,N_IANM"), ("با", "ADP,PREP"), ("دمای", "NOUN,N_IANM"), ("بالاتر", "ADJ,ADJ_AJCM"), ("از", "ADP,PREP"), ("صفر", "NOUN,N_IANM"), ("مطلق", "ADJ,ADJ_AJP"), ("انرژی", "NOUN,N_IANM"), ("تابش", "NOUN,N_IANM"), ("خواهد", "AUX,AUX"), ("کرد", "VERB,V_ACT"), (".", "PUNCT,PUNC")]
    assert actual == expected

def test_trees(dadegan_reader: DadeganReader):
    actual = str(next(dadegan_reader.trees()))
    expected = "TokenTree<token={id=12, form=کرد}, children=[...]>"
    assert actual == expected
