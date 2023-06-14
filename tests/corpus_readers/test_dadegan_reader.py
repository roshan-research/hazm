import conllu
import pytest

from hazm import DadeganReader
from hazm import tree2brackets


@pytest.fixture(scope="module")
def dadegan_reader():
    return DadeganReader("corpora/dadegan.conllu")

def test_sents(dadegan_reader: DadeganReader):
    sents = dadegan_reader.sents()
    actual1 = next(sents)
    expected1 = [("هر", "DET,PREM_AMBAJ"), ("جسمی", "NOUN,N_IANM"), ("با", "ADP,PREP"), ("دمای", "NOUN,N_IANM"), ("بالاتر", "ADJ,ADJ_AJCM"), ("از", "ADP,PREP"), ("صفر", "NOUN,N_IANM"), ("مطلق", "ADJ,ADJ_AJP"), ("انرژی", "NOUN,N_IANM"), ("تابش", "NOUN,N_IANM"), ("خواهد", "AUX,AUX"), ("کرد", "VERB,V_ACT"), (".", "PUNCT,PUNC")]
    assert actual1 == expected1

    actual2 = next(sents)
    expected2 = [("دست", "NOUN,N_IANM"), ("فاطمه\u200c", "PROPN,N_ANM"), ("ام", "PRON,PR_JOPER"), ("پینه", "NOUN,N_IANM"), ("بسته", "VERB,V_ACT"), ("است", "AUX,AUX"), (".", "PUNCT,PUNC")]
    assert actual2 == expected2

def test_trees(dadegan_reader: DadeganReader):
    trees = dadegan_reader.trees()
    actual1 = str(next(trees))
    expected1 = "TokenTree<token={id=12, form=کرد}, children=[...]>"
    assert actual1 == expected1

    actual2 = str(next(trees))
    expected2 = "TokenTree<token={id=5, form=بسته}, children=[...]>"
    assert actual2 == expected2
