"""This module includes classes and functions for reading the pn-summary corpus.

The [pn-summary](https://github.com/hooshvare/pn-summary) corpus was prepared to
help deep learning systems and build better models for more accurate Persian
text summarization. This corpus includes 93,207 cleaned news texts extracted
from 6 Persian news agencies out of approximately 200,000 news items.
"""
import csv
from collections.abc import Iterator
from pathlib import Path


class PnSummaryReader:
    """This class includes functions for reading the pn-summary corpus.

    Args:
        corpus_folder: Path to the folder containing the corpus files.
        subset: The dataset subset; can be `test`, `train`, or `dev`.
    """

    def __init__(self: "PnSummaryReader", corpus_folder: str, subset: str="train") -> None:
        """Initializes the PnSummaryReader.

        Args:
            corpus_folder: Path to the folder containing the corpus files.
            subset: The dataset subset; can be `test`, `train`, or `dev`.
        """
        # Materialize the glob into a list so docs() can be iterated more than
        # once (a bare glob() is a one-shot iterator).
        self._file_paths = sorted(Path(corpus_folder).glob(f"{subset}*.csv"))

    def docs(self: "PnSummaryReader") -> Iterator[tuple[str, str, str, str, str, list[str], str, str]]:
        """Yields news articles one by one.

        Examples:
            >>> pn_summary = PnSummaryReader("pn-summary", "test")
            >>> next(pn_summary.docs())
            (
                'ff49386698b87be4fc3943bd3cf88987157e1d47',
                'کاهش ۵۸ درصدی مصرف نفت کوره منطقه سبزوار',
                'مدیر شرکت ملی پخش فرآورده‌های نفتی منطقه سبزوار به خبرنگار شانا، گفت...,
                'مصرف نفت کوره منطقه سبزوار در بهار امسال، نسبت به مدت مشابه پارسال، ۵۸ درصد کاهش یافت.',
                'Oil-Energy',
                ['پالایش و پخش'],
                'Shana',
                'https://www.shana.ir/news/243726/%DA%A9%D8%A7%D9%87%D8...'
            )

        Yields:
           The next news entry in the format `(id, title, article, summary, category_en, [category_fa1, category_fa2, ...], source, link)`.
        """
        for file_path in self._file_paths:
                with Path(file_path).open("r", encoding="utf-8") as file:
                    reader = csv.reader(file, delimiter="\t")
                    next(reader)  # Skip the header row

                    for row in reader:
                        _id, title, article, summary, category, categories, network, link = (field.strip() for field in row)
                        categories = categories.split("+")
                        yield (_id, title, article, summary, category, categories, network, link)
