from hazm import PeykareReader


def test_sents():
    peykare = PeykareReader(root="corpora/peykare")
    actual = next(peykare.sents())
    expected = [("دیرزمانی", "N"), ("از", "P"), ("راه\u200cاندازی", "N,EZ"), ("شبکه\u200cی", "N,EZ"), ("خبر", "N,EZ"), ("الجزیره", "N"), ("نمی\u200cگذرد", "V"), ("،", "PUNC"), ("اما", "CONJ"), ("این", "DET"), ("شبکه\u200cی", "N,EZ"), ("خبری", "AJ,EZ"), ("عربی", "N"), ("بسیار", "ADV"), ("سریع", "ADV"), ("توانسته", "V"), ("در", "P"), ("میان", "N,EZ"), ("شبکه\u200cهای", "N,EZ"), ("عظیم", "AJ,EZ"), ("خبری", "AJ"), ("و", "CONJ"), ("بنگاه\u200cهای", "N,EZ"), ("چندرسانه\u200cای", "AJ,EZ"), ("دنیا", "N"), ("خودی", "N"), ("نشان", "N"), ("دهد", "V"), (".", "PUNC")]
    assert actual == expected
