"""This module includes classes and functions for reading the Degarbayan corpus.

The [Degarbayan corpus](https://www.peykaregan.ir/dataset/%D9%BE%DB%8C%DA%A9%D8%B1%D9%87-%D8%AF%DA%AF%D8%B1%D8%A8%DB%8C%D8%A7%D9%86)
contains 1,523 instances labeled as paraphrases. Paraphrase sentences and
phrases are different expressions of the same concept. Data in this corpus is
collected from news agencies and presented in three categories: 'Paraphrase',
'Semi-Paraphrase', and 'Not Paraphrase'. This data was tagged using
crowdsourcing on Telegram.
"""


import os
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from xml.dom import minidom


class DegarbayanReader:
    """This class includes methods for reading the Degarbayan corpus.

    Args:
        root: Path to the folder containing the corpus files.
        corpus_file: The corpus information file. No need to change this if
            using the standard version.
        judge_type: Determines the labeling scheme. Can be 'three_class' or
            'two_class'. In 'three_class', labels are 'Paraphrase',
            'SemiParaphrase', and 'NotParaphrase'. In 'two_class',
            'SemiParaphrase' is also labeled as 'Paraphrase'.
    """

    def __init__(
        self: "DegarbayanReader",
        root: str,
        corpus_file: str = "corpus_pair.xml",
        judge_type: str = "three_class",
    ) -> None:
        """Initializes the DegarbayanReader with the root folder and settings.

        Args:
            root: Path to the folder containing the corpus files.
            corpus_file: The corpus data file. Defaults to 'corpus_pair.xml'.
            judge_type: The classification mode ('three_class' or 'two_class').
                Defaults to 'three_class'.
        """
        self._root = root
        self._corpus_file = corpus_file
        self._judge_type = judge_type
        if judge_type not in {"three_class", "two_class"}:
            self._judge_type = "three_class"

    def docs(self: "DegarbayanReader") -> Iterator[dict[str, Any]]:
        """Returns the documents available in the corpus.

        Yields:
            The next document as a dictionary containing pair information.
        """

        def judge_number_to_text(judge: str) -> str:
            """Converts numeric judge labels to their corresponding text representation.

            Args:
                judge: The numeric judge label as a string.

            Returns:
                The textual representation of the label based on `judge_type`.
            """
            if judge == "1" or (self._judge_type == "two_class" and judge == "0"):
                return "Paraphrase"

            if judge == "0":
                return "SemiParaphrase"

            return "NotParaphrase"

        filename = os.path.join(self._root, self._corpus_file) # noqa: PTH118
        if os.path.exists(filename): # noqa: PTH110
            try:
                elements = minidom.parse(filename)
                for element in elements.getElementsByTagName("Pair"):
                    pair = {
                        "id": (
                            element.getElementsByTagName("PairId")[0]
                            .childNodes[0]
                            .data.strip()
                        ),
                        "news_source1": (
                            element.getElementsByTagName("NewsSource1")[0]
                            .childNodes[0]
                            .data.strip()
                        ),
                        "news_source2": (
                            element.getElementsByTagName("NewsSource2")[0]
                            .childNodes[0]
                            .data.strip()
                        ),
                        "news_id1": (
                            element.getElementsByTagName("NewsId1")[0]
                            .childNodes[0]
                            .data.strip()
                        ),
                        "news_id2": (
                            element.getElementsByTagName("NewsId2")[0]
                            .childNodes[0]
                            .data.strip()
                        ),
                        "sentence1": (
                            element.getElementsByTagName("Sentence1")[0]
                            .childNodes[0]
                            .data.strip()
                        ),
                        "sentence2": (
                            element.getElementsByTagName("Sentence2")[0]
                            .childNodes[0]
                            .data.strip()
                        ),
                        "method_type": (
                            element.getElementsByTagName("MethodType")[0]
                            .childNodes[0]
                            .data.strip()
                        ),
                        "judge": judge_number_to_text(
                            element.getElementsByTagName("judge")[0]
                            .childNodes[0]
                            .data.strip(),
                        ),
                    }
                    yield pair

            except Exception as e:
                print("error in reading", filename, e, file=sys.stderr)
        else:
            print("error in reading file", filename, file=sys.stderr)
            msg = "error in reading file"
            raise FileNotFoundError(msg, filename)

    def pairs(self: "DegarbayanReader") -> Iterator[tuple[str, str, str]]:
        """Returns paraphrase pairs in the form of (original_text, paraphrase_text, label).

        Examples:
            >>> degarbayan = DegarbayanReader(root='degarbayan')
            >>> next(degarbayan.pairs())
            ('24 نفر نهایی تیم ملی بدون تغییری خاص معرفی شد', 'کی روش 24 بازیکن را به تیم ملی فوتبال دعوت کرد', 'Paraphrase')

        Yields:
            The next paraphrase pair as a tuple of (sentence1, sentence2, judge).
        """
        for pair in self.docs():
            yield pair["sentence1"], pair["sentence2"], pair["judge"]
