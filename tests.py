import doctest
import inspect
import sys
import unittest

from hazm import BijankhanReader
from hazm import Chunker
from hazm import DadeganReader
from hazm import DegarbayanReader
from hazm import DependencyParser
from hazm import HamshahriReader
from hazm import InformalNormalizer
from hazm import Lemmatizer
from hazm import MirasTextReader
from hazm import Normalizer
from hazm import PersicaReader
from hazm import PeykareReader
from hazm import POSTagger
from hazm import QuranCorpusReader
from hazm import SentenceTokenizer
from hazm import SentiPersReader
from hazm import SequenceTagger
from hazm import Stemmer
from hazm import TNewsReader
from hazm import TokenSplitter
from hazm import TreebankReader
from hazm import VerbValencyReader
from hazm import WordTokenizer
from hazm import utils

modules = {
    # "normalizer": Normalizer,
    # "informal_normalizer": InformalNormalizer,
    # "lemmatizer": Lemmatizer,
    # "stemmer": Stemmer,
    # "sentence_tokenizer": SentenceTokenizer,
    # "word_tokenizer": WordTokenizer,
    # "splitter": TokenSplitter,
    "postagger": POSTagger,
    # "parser": DependencyParser,
    "chunker": Chunker,
    # "persica": PersicaReader,
    # "hamshahri": HamshahriReader,
    # "bijankhan": BijankhanReader,
    # "peykare": PeykareReader,
    # "dadegan": DadeganReader,
    # "valency": VerbValencyReader,
    # "sentipers": SentiPersReader,
    # "degarbayan": DegarbayanReader,
    # "tnews": TNewsReader,
    # "quran": QuranCorpusReader,
    # "miras_text": MirasTextReader,

    "tagger": SequenceTagger,
    # "treebank": TreebankReader,
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