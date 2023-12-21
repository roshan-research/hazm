"""این ماژول شامل کلاس‌ها و توابعی برای شناساییِ وابستگی‌های دستوری متن است.
برای استفاده از این ماژول، ابتدا [پیش‌نیازهای `dependecy_parser` را با حجمی حدود ۱۳ مگابایت دانلود کنید](https://github.com/roshan-research/hazm#pretrained-models) و در ریشهٔ پروژه یا مسیر دلخواه اکسترکت کنید.

"""


import os
import tempfile
from pathlib import Path
from typing import Type

from nltk.parse import DependencyGraph
from nltk.parse.api import ParserI
from nltk.parse.malt import MaltParser as NLTKMaltParser

from tqdm import tqdm
from typing import List, Tuple
import os

class MaltParser(NLTKMaltParser):
    """این کلاس شامل توابعی برای شناسایی وابستگی‌های دستوری است.

    Args:
        tagger: نام تابع `POS Tagger`.
        lemmatizer: نام کلاس ریشه‌یاب.
        working_dir: مسیر فولدر حاوی پیش‌نیازهای اجرایی این ماژول.
        model_file: آدرس مدلِ از پیش آموزش دیده با پسوند `mco`.

    """

    def __init__(
        self: "MaltParser",
        tagger: str,
        lemmatizer: str,
        working_dir: str = "universal_dependency_parser",
        model_file: str = "langModel.mco",  # Don't rename this file
    ) -> None:
        self.tagger = tagger
        self.working_dir = working_dir
        self.mco = model_file
        self._malt_bin = os.path.join(working_dir, "malt.jar") # noqa: PTH118
        self.lemmatize = (
            lemmatizer.lemmatize if lemmatizer else lambda w, t: "_" # noqa: ARG005
        )

    def parse_sents(self: "MaltParser", sentences: str, verbose: bool = False) -> str:
        """گراف وابستگی را برمی‌گرداند.

        Args:
            sentences: جملاتی که باید گراف وابستگی آن‌ها استخراج شود.
            verbose: اگر `True` باشد وابستگی‌های بیشتری را برمی‌گرداند.

        Returns:
            گراف وابستگی.

        """
        tagged_sentences = self.tagger.tag_sents(sentences)
        return self.parse_tagged_sents(tagged_sentences, verbose)

    def parse_tagged_sents(
        self: "MaltParser",
        sentences: List[List[Tuple[str, str]]],
        verbose: bool = False,
    ) -> str:
        """گراف وابستگی‌ها را برای جملات ورودی برمی‌گرداند.

        Args:
            sentences: جملاتی که باید گراف وابستگی‌های آن استخراج شود.
            verbose: اگر `True` باشد وابستگی‌های بیشتری را برمی‌گرداند..

        Returns:
            گراف وابستگی جملات.

        Raises:
            Exception: در صورت بروز خطا یک اکسپشن عمومی صادر می‌شود.

        """
        input_file = tempfile.NamedTemporaryFile(
            prefix="malt_input.conll",
            dir=self.working_dir,
            delete=False,
        )
        output_file = tempfile.NamedTemporaryFile(
            prefix="malt_output.conll",
            dir=self.working_dir,
            delete=False,
        )

        try:
            for sentence in sentences:
                for i, (word, tag) in enumerate(sentence, start=1):
                    word = word.strip()
                    if not word:
                        word = "_"
                    input_file.write(
                        (
                            "\t".join(
                                [
                                    str(i),
                                    word.replace(" ", "_"),
                                    self.lemmatize(word, tag).replace(" ", "_"),
                                    tag,
                                    tag,
                                    "_",
                                    "0",
                                    "ROOT",
                                    "_",
                                    "_",
                                    "\n",
                                ],
                            )
                        ).encode("utf8"),
                    )
                input_file.write(b"\n\n")
            input_file.close()

            cmd = [
                "java",
                "-jar",
                self._malt_bin,
                "-w",
                self.working_dir,
                "-c",
                self.mco,
                "-i",
                input_file.name,
                "-o",
                output_file.name,
                "-m",
                "parse",
            ]
            if self._execute(cmd, verbose) != 0:
                raise Exception("MaltParser parsing failed: %s" % " ".join(cmd))

            return (
                DependencyGraph(item)
                for item in open(output_file.name, encoding="utf8").read().split("\n\n") # noqa: SIM115, PTH123
                if item.strip()
            )

        finally:
            input_file.close()
            os.remove(input_file.name) # noqa: PTH107
            output_file.close()
            os.remove(output_file.name) # noqa: PTH107


class TurboParser(ParserI):
    """interfaces [TurboParser](http://www.ark.cs.cmu.edu/TurboParser/) which you must
    manually install.

    """

    def __init__(self: "TurboParser", tagger, lemmatizer: str, model_file: str) -> None:
        self.tagger = tagger
        self.lemmatize = (
            lemmatizer.lemmatize if lemmatizer else lambda w, t: "_" # noqa: ARG005
        )

        import turboparser

        self._pturboparser = turboparser.PTurboParser()
        self.interface = self._pturboparser.create_parser()
        self.interface.load_parser_model(model_file)

    def parse_sents(
        self: "TurboParser",
        sentences: List[List[Tuple[str, str]]],
    ) -> Type[DependencyGraph]:
        """parse_sents."""
        tagged_sentences = self.tagger.tag_sents(sentences)
        return self.tagged_parse_sents(tagged_sentences)

    def tagged_parse_sents(
        self: "TurboParser",
        sentences: List[List[Tuple[str, str]]],
    ) -> Type[DependencyGraph]:
        """tagged_parse_sents."""
        input_file = tempfile.NamedTemporaryFile(
            prefix="turbo_input.conll",
            dir="dependency_parser",
            delete=False,
        )
        output_file = tempfile.NamedTemporaryFile(
            prefix="turbo_output.conll",
            dir="dependency_parser",
            delete=False,
        )

        try:
            for sentence in sentences:
                for i, (word, tag) in enumerate(sentence, start=1):
                    word = word.strip()
                    if not word:
                        word = "_"
                    input_file.write(
                        (
                            "\t".join(
                                [
                                    str(i),
                                    word.replace(" ", "_"),
                                    self.lemmatize(word, tag).replace(" ", "_"),
                                    tag,
                                    tag,
                                    "_",
                                    "0",
                                    "ROOT",
                                    "_",
                                    "_",
                                    "\n",
                                ],
                            )
                        ).encode("utf8"),
                    )
                input_file.write(b"\n")
            input_file.close()

            self.interface.parse(input_file.name, output_file.name)

            return (
                DependencyGraph(item, cell_extractor=lambda cells: cells[1:8])
                for item in open(output_file.name, encoding="utf8").read().split("\n\n") # noqa: SIM115, PTH123
                if item.strip()
            )

        finally:
            input_file.close()
            os.remove(input_file.name) # noqa: PTH107
            output_file.close()
            os.remove(output_file.name) # noqa: PTH107


class DependencyParser(MaltParser):
    """این کلاس شامل توابعی برای شناسایی وابستگی‌های دستوری است.

    این کلاس تمام توابع خود را از کلاس
    [MaltParser][hazm.dependency_parser.MaltParser] به ارث می‌برد.

    Examples:
        >>> from hazm import POSTagger, Lemmatizer, DependencyParser
        >>> parser = DependencyParser(tagger=POSTagger(model='pos_tagger.model'), lemmatizer=Lemmatizer())
        >>> parser.parse(['من', 'به', 'مدرسه', 'رفته بودم', '.']).tree().pprint()
        (من (به (مدرسه (رفته_بودم .))))
    """



class SpacyDependencyParser(MaltParser):
    def __init__(
        self: "SpacyDependencyParser",
        tagger: object,
        lemmatizer: object,
        working_dir: str = "universal_dependency_parser",
        model_file: str = "dependency_parser/ParsbertChangeTag/model-best"
    ) -> None:
        import spacy
        from spacy.tokens import Doc
        from tqdm import tqdm
        from typing import List, Tuple


        """
        Initialize the SpacyDependencyParser object.

        Parameters:
        - tagger: An object responsible for part-of-speech tagging.
        - lemmatizer: An object responsible for lemmatization.
        - working_dir: The directory where temporary files are stored.
        - model_file: The path to the Spacy dependency parser model file.
        """
        self.tagger = tagger
        self.working_dir = working_dir
        self.mco = model_file
        self.lemmatize = (
            lemmatizer.lemmatize if lemmatizer else lambda w, t: "_" # noqa: ARG005
        )
        self.peykare_dict = {}
        self._setup_model()

    def _setup_model(self:"SpacyDependencyParser"):
        """
        Load the Spacy dependency parser model and set up a custom tokenizer.
        """
        try:
            self.model = spacy.load(self.mco)
            self.model.tokenizer = self._custom_tokenizer
        except:
            raise ValueError("Something wrong loading the dependencyParser . Checkout for correctness or existence of path")

    def _add_sentence2dict(self:"SpacyDependencyParser", sent):
        """
        Add a sentence to the dictionary for later use in custom tokenization.

        Parameters:
        - sent: The sentence to be added to the dictionary.
        """
        self.peykare_dict[' '.join([w for w in sent])] = [w for w in sent]

    def _custom_tokenizer(self:"SpacyDependencyParser", text):
        """
        Custom tokenizer function for Spacy, using a pre-built dictionary.

        Parameters:
        - text: The input text to be tokenized.
        """
        if text not in self.peykare_dict:
            self._add_sentence2dict(text)
        return Doc(self.model.vocab, self.peykare_dict[text])

    def parse_sents(self: MaltParser, sentences: str, verbose: bool = False) -> str:
        """
        Parse a list of sentences and return the dependency graphs.

        Parameters:
        - sentences: List of sentences to be parsed.
        - verbose: Whether to print additional information during parsing.
        """
        for sentence in sentences:
            self._add_sentence2dict(sentence)

        tagged_sentences = self.tagger.tag_sents(sentences,universal_tag=True)
        return self.parse_tagged_sents(tagged_sentences, verbose)


    def _spacy_to_conll(self,doc):
        conll_lines = []
        for token in doc:
            head_id = token.head.i + 1

            conll_lines.append(
                "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                    token.i + 1,
                    token.text.replace(" ", "_"),
                    self.lemmatize(token.text, token.pos_).replace(" ", "_"),
                    token.pos_,
                    token.pos_,
                    "_",
                    head_id,
                    token.dep_, 
                    "_",
                    "_",
                )
            )
        return "\n".join(conll_lines)

    def parse_tagged_sents(self: "SpacyDependencyParser", sentences: List[List[Tuple[str, str]]], verbose: bool = False) -> str:
        """
        Parse a list of tagged sentences and return the dependency graphs.

        Parameters:
        - sentences: List of tagged sentences to be parsed.
        - verbose: Whether to print additional information during parsing.
        """
        texts = [' '.join([w for w , _ in sentence]) for sentence in sentences]
        docs = list(self.model.pipe(texts))
        conll_list = []
        for doc_id , doc in enumerate(docs):
            pos_tags = [tag for w , tag in sentences[doc_id]]
            for i in range(len(doc)):
                docs[doc_id][i].pos_ = pos_tags[i]
            conll_sample = self._spacy_to_conll(docs[doc_id])
            conll_list.append(conll_sample)

        return (
            DependencyGraph(item)
            for item in conll_list
            if item.strip()
        )