import pytest
import sys

from hazm import WikipediaReader


@pytest.fixture(scope="module")
def wikipedia_reader():
    return WikipediaReader("tests/files/wiki.xml.bz2")

@pytest.mark.xfail(sys.version_info >= (3,11), reason="StopIteration issue on Python 3.11")
def test_docs(wikipedia_reader):
    actual = next(wikipedia_reader.docs())["id"]
    expected = "1"
    assert actual == expected

@pytest.mark.xfail(sys.version_info >= (3,11), reason="StopIteration issue on Python 3.11")
def test_texts(wikipedia_reader):
    actual = next(wikipedia_reader.texts()).startswith("This is the first page of the Wikipedia")
    expected = True
    assert actual == expected