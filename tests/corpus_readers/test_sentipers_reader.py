from hazm import SentiPersReader


def test_comments():
    sentipers = SentiPersReader(root="tests/files/sentipers")
    actual = next(sentipers.comments())[0][1]
    expected = "بيشتر مناسب است براي کساني که به دنبال تنوع هستند و در همه چيز نو گرايي دارند ."
    assert actual == expected
