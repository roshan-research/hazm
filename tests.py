import doctest
import inspect
import sys
import unittest

from hazm import (BijankhanReader, Chunker, DadeganReader, DegarbayanReader,
                  DependencyParser, HamshahriReader, InformalNormalizer,
                  Lemmatizer, MirasTextReader, Normalizer, PersicaReader,
                  PeykareReader, POSTagger, QuranCorpusReader,
                  SentenceTokenizer, SentiPersReader, SequenceTagger, Stemmer,
                  TNewsReader, TokenSplitter, TreebankReader,
                  VerbValencyReader, WordTokenizer, utils)

modules = {
    "normalizer": Normalizer,
    "informal_normalizer": InformalNormalizer,
    "lemmatizer": Lemmatizer,
    "stemmer": Stemmer,
    "sentence_tokenizer": SentenceTokenizer,
    "word_tokenizer": WordTokenizer,
    "splitter": TokenSplitter,
    "postagger": POSTagger,
    "parser": DependencyParser,
    "chunker": Chunker,
    "tagger": SequenceTagger,
    "persica": PersicaReader,
    "hamshahri": HamshahriReader,
    "bijankhan": BijankhanReader,
    "peykare": PeykareReader,
    "dadegan": DadeganReader,
    "valency": VerbValencyReader,
    "sentipers": SentiPersReader,
    "degarbayan": DegarbayanReader,
    "tnews": TNewsReader,
    "quran": QuranCorpusReader,
    "miras_text": MirasTextReader,
    "treebank": TreebankReader,
}


class UnicodeOutputChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        try:
            want, got = eval(want), eval(got)
        except:
            pass

        try:
            got = got.decode("unicode-escape")
            want = want.replace("آ", "ا")  # decode issue
        except:
            pass

        if type(want) == str:
            want = want.replace("٫", ".")  # eval issue

        return want == got


if __name__ == "__main__":
    # test all modules if no one specified
    all_modules = len(sys.argv) < 2

    suites = []
    checker = UnicodeOutputChecker() if utils.PY2 else None
    for name, obj in list(modules.items()):
        if all_modules or name in sys.argv:
            suites.append(doctest.DocTestSuite(inspect.getmodule(obj), checker=checker))

    failure = False
    runner = unittest.TextTestRunner(verbosity=2)
    for suite in suites:
        if not runner.run(suite).wasSuccessful():
            failure = True

    if failure:
        exit(1)
