import pytest

from hazm import DadeganReader
from hazm import tree2brackets


@pytest.fixture(scope="module")
def dadegan_reader():
    return DadeganReader("corpora/dadegan.conll")

def test_sents(dadegan_reader: DadeganReader):
    sents = dadegan_reader.sents()
    actual = next(sents)
    expected = [("این", "DET"), ("میهمانی", "N"), ("به", "P"), ("منظور", "Ne"), ("آشنایی", "Ne"), ("هم\u200cتیمی\u200cهای", "Ne"), ("او", "PRO"), ("با", "P"), ("غذاهای", "Ne"), ("ایرانی", "AJ"), ("ترتیب", "N"), ("داده_شد", "V"), (".", "PUNC")]
    assert actual == expected


def test_trees(dadegan_reader: DadeganReader):
    trees = dadegan_reader.trees()
    actual = next(trees).to_conll(10).split("\n")[0]
    expected = "1\tاین\tاین\tPREM\tDEMAJ\tattachment=ISO|senID=23485\t2\tNPREMOD\t_\t_"
    assert actual == expected

