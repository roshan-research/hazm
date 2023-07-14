import pytest

from hazm import WikipediaReader


@pytest.fixture(scope="module")
def wikipedia_reader():
    return WikipediaReader("tests/files/wiki.xml.bz2")

def test_docs(wikipedia_reader):
    actual = next(wikipedia_reader.docs())["id"]
    expected = "1"
    assert actual == expected

def test_texts(wikipedia_reader):
    actual = next(wikipedia_reader.texts()).startswith("This is the first page of the Wikipedia")
    expected = True
    assert actual == expected