from hazm import HamshahriReader


def test_docs():
    hamshahri = HamshahriReader(root="tests/files/hamshahri")
    actual = next(hamshahri.docs())["id"]
    expected = "HAM2-750403-001"
    assert actual == expected
