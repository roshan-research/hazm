import pytest

from hazm import TNewsReader


@pytest.fixture(scope="module")
def tnews_reader():
    return TNewsReader(root="corpora/tnews")

def test_docs(tnews_reader):
    actual = next(tnews_reader.docs())["id"]
    expected = "14092303482300013653"
    assert actual == expected

def test_texts(tnews_reader):
    actual = next(tnews_reader.texts()).startswith("به گزارش ”  شبکه اطلاع رسانی اینترنتی بوتیا  ” به نقل از ارگ نیوز")
    expected = True
    assert actual == expected
