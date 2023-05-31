class TestDependencyParser:

    def test_parse(self:"TestDependencyParser", dependency_parser):
        actual = str(dependency_parser.parse(["من", "به", "مدرسه", "رفته بودم", "."]).tree())
        expected = "(من (به (مدرسه (رفته_بودم .))))"
        assert actual == expected
