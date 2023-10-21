from hazm import ArmanReader


def test_sents():
    arman = ArmanReader(corpus_folder="tests/files/arman", subset="test")
    sentence = next(arman.sents())
    assert sentence == [("همین", "O"), ("فکر", "O"), ("،", "O"), ("این", "O"), ("احساس", "O"), ("را", "O"), ("به", "O"), ("من", "O"), ("می\u200cداد", "O"), ("که", "O"), ("آزاد", "O"), ("هستم", "O"), (".", "O")]
