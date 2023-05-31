from hazm import DegarbayanReader


def test_pairs():
    degarbayan = DegarbayanReader(root="corpora/degarbayan")
    actual = next(degarbayan.pairs())
    expected = ("24 نفر نهایی تیم ملی بدون تغییری خاص معرفی شد", "کی روش 24 بازیکن را به تیم ملی فوتبال دعوت کرد", "Paraphrase")
    assert actual == expected
