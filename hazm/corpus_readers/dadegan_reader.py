"""این ماژول شامل کلاس‌ها و توابعی برای خواندن پیکرهٔ PerDT است.

PerDT حاوی تعداد قابل‌توجهی جملۀ برچسب‌خورده با اطلاعات نحوی و ساخت‌واژی است.

"""
from typing import Iterator
from typing import List
from typing import Tuple
from typing import Type

from conllu import TokenTree
from conllu import parse
from conllu import parse_tree
from nltk.tree import Tree


class DadeganReader:
    """این کلاس شامل توابعی برای خواندن پیکرهٔ PerDT است.

    Args:
        conllu_file: مسیر فایلِ پیکره.

    """

    def __init__(
        self: "DadeganReader",
        conllu_file: str,
    ) -> None:

        with open(conllu_file, encoding="utf-8") as conllu: # noqa: PTH123
            self._conllu_content = conllu.read()


    def trees(self: "DadeganReader") ->  Iterator[TokenTree]:
        """ساختار درختی جملات را برمی‌گرداند.

        Yields:
            ساختار درختی جملهٔ بعدی.

        """
        yield from parse_tree(self._conllu_content) # .print_tree()

    def sents(self: "DadeganReader") -> Iterator[List[Tuple[str, str]]]:
        """لیستی از جملات را برمی‌گرداند.

        هر جمله لیستی از `(توکن، برچسب)`ها است.

        Examples:
            >>> dadegan = DadeganReader(conllu_file='corpora/dadegan.conll')
            >>> next(dadegan.sents())
            [('این', 'DET'), ('میهمانی', 'N'), ('به', 'P'), ('منظور', 'Ne'), ('آشنایی', 'Ne'), ('هم‌تیمی‌های', 'Ne'), ('او', 'PRO'), ('با', 'P'), ('غذاهای', 'Ne'), ('ایرانی', 'AJ'), ('ترتیب', 'N'), ('داده_شد', 'V'), ('.', 'PUNC')]

        Yields:
            جملهٔ بعدی.

        """
        for sent in parse(self._conllu_content):
            sents = list(sent)
            for sent in sents:
                sent["mtag"] = ",".join([sent["upos"], sent["xpos"]])
                if sent["feats"] is not None and "ezafe" in sent["feats"]:
                    sent["mtag"] += ",EZ"

            yield [(sent["form"], sent["mtag"]) for sent in sents]

