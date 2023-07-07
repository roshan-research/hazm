import pytest

from hazm import TreebankReader
from hazm import tree2brackets


@pytest.fixture(scope="module")
def treebank_reader():
    return TreebankReader(root="tests/files/treebank")

def test_trees(treebank_reader):
    actual = str(next(treebank_reader.trees()))
    expected = """(S
  (VPS
    (NPC (N دنیای/Ne) (MN (N آدولف/N) (N بورن/N)))
    (VPC
      (NPC (N دنیای/Ne) (NPA (N اتفاقات/Ne) (ADJ رویایی/AJ)))
      (V است/V)))
  (PUNC ./PUNC))"""
    assert actual == expected

def test_sents(treebank_reader):
    actual = next(treebank_reader.sents())
    expected = [("دنیای", "Ne"), ("آدولف", "N"), ("بورن", "N"), ("دنیای", "Ne"), ("اتفاقات", "Ne"), ("رویایی", "AJ"), ("است", "V"), (".", "PUNC")]
    assert actual == expected

def test_chunked_trees(treebank_reader):
    actual = tree2brackets(next(treebank_reader.chunked_trees()))
    expected = "[دنیای آدولف بورن NP] [دنیای اتفاقات رویایی NP] [است VP] ."
    assert actual == expected
