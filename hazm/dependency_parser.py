"""This module includes classes and functions for identifying grammatical dependencies in text."""

import logging
import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from nltk.parse import DependencyGraph
from nltk.parse.malt import MaltParser as NLTKMaltParser

try:
    import spacy
    from spacy.tokens import Doc
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    Doc = Any

from hazm.types import Sentence
from hazm.types import TaggedSentence

logger = logging.getLogger(__name__)


class MaltParser(NLTKMaltParser):
    """This class includes functions for identifying grammatical dependencies using MaltParser."""

    def __init__(
        self,
        tagger: Any,
        lemmatizer: Any,
        working_dir: str = "universal_dependency_parser",
        model_file: str = "langModel.mco",
        repo_id: str | None = None,
        model_filename: str | None = None,
    ) -> None:
        """Constructor for MaltParser."""
        self.tagger = tagger
        self.lemmatize = (
            lemmatizer.lemmatize if lemmatizer else lambda _w, _t: "_"
        )

        self._final_working_dir = working_dir
        self._model_base_name = model_file.replace(".mco", "")

        if repo_id and model_filename:
            try:
                from huggingface_hub import snapshot_download

                cache_dir = snapshot_download(repo_id=repo_id)

                self._final_working_dir = cache_dir
                self._model_base_name = model_filename.replace(".mco", "")

            except ImportError as e:
                msg = "Please install `huggingface-hub` to use pretrained models from Hub."
                raise ImportError(msg) from e
            except Exception as e:
                msg = f"Failed to download model from {repo_id}: {e}"
                raise ValueError(msg) from e

    def parse_sents(self, sentences: list[Sentence], verbose: bool = False) -> Iterator[DependencyGraph]:
        """Returns the dependency graph for a list of sentences."""
        tagged_sentences = self.tagger.tag_sents(sentences)
        return self.parse_tagged_sents(tagged_sentences, verbose)

    def parse_tagged_sents(
        self,
        sentences: list[TaggedSentence],
        verbose: bool = False, # noqa: ARG002
    ) -> Iterator[DependencyGraph]:
        """Returns dependency graphs for input sentences by executing MaltParser."""
        # Check if Java is installed
        try:
            subprocess.run(["java", "-version"], capture_output=True, check=True)
        except Exception as e:
            msg = "Java is not installed. Please install JRE/JDK (e.g., !apt-get install default-jre)."
            raise RuntimeError(msg) from e

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            input_path = temp_path / "malt_input.conll"
            output_path = temp_path / "malt_output.conll"

            source_dir = Path(self._final_working_dir)

            # 1. Copy Model File (.mco)
            model_source = source_dir / f"{self._model_base_name}.mco"
            if not model_source.exists():
                msg = f"Model file not found at {model_source}"
                raise FileNotFoundError(msg)
            shutil.copy(str(model_source), str(temp_path))

            # 2. Copy ALL .jar files (Flattening structure)
            jars = list(source_dir.rglob("*.jar"))
            if not jars:
                msg = f"No .jar files found in {source_dir}. MaltParser requires malt.jar and dependencies."
                raise FileNotFoundError(msg)

            for jar in jars:
                shutil.copy(str(jar), str(temp_path))

            # 3. Create input CoNLL file
            with input_path.open("w", encoding="utf8") as input_file:
                for sentence in sentences:
                    for i, (word, tag) in enumerate(sentence, start=1):
                        word = word.strip() or "_"
                        lemma = self.lemmatize(word, tag) or "_"
                        input_file.write(
                            f"{i}\t{word.replace(' ', '_')}\t{lemma.replace(' ', '_')}\t{tag}\t{tag}\t_\t0\tROOT\t_\t_\n",
                        )
                    input_file.write("\n\n")

            # 4. Command execution
            cmd = [
                "java",
                "-Xmx512m",
                "-cp", "*",
                "org.maltparser.Malt",
                "-w", ".",
                "-c", str(self._model_base_name),
                "-i", "malt_input.conll",
                "-o", "malt_output.conll",
                "-m", "parse",
            ]

            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(temp_path),
            )
            try:
                stdout, stderr = process.communicate()
            finally:
                if process.poll() is None:
                    process.terminate()
                    process.wait()

            if process.returncode != 0:
                msg = f"MaltParser execution failed.\nCMD: {' '.join(cmd)}\nSTDOUT: {stdout}\nSTDERR: {stderr}"
                raise RuntimeError(msg)

            # 5. Parse results
            if not output_path.exists():
                 msg = f"MaltParser failed to generate output file.\nSTDERR: {stderr}"
                 raise RuntimeError(msg)

            with output_path.open(encoding="utf8") as output_file:
                content = output_file.read()
                for item in content.split("\n\n"):
                    if item.strip():
                        yield DependencyGraph(item, top_relation_label="root")


class SpacyDependencyParser(MaltParser):
    """A Dependency Parser based on the Spacy library."""

    def __init__(
        self,
        tagger: Any,
        lemmatizer: Any,
        model_path: str | Path | None = None,
        using_gpu: bool = False,
        gpu_id: int = 0,
        repo_id: str | None = None,
    ) -> None:
        """Initialize Spacy-based parser."""
        if not SPACY_AVAILABLE:
            msg = "To use Spacy-based models, please install hazm: pip install hazm[all]"
            raise ImportError(msg)

        self.tagger = tagger
        self.lemmatize = (
            lemmatizer.lemmatize if lemmatizer else lambda _w, _t: "_"
        )

        self.model_path = str(model_path) if model_path else None
        self.using_gpu = using_gpu
        self.gpu_id = gpu_id
        self.model = None
        self.gpu_availability = False

        if repo_id:
            try:
                from huggingface_hub import snapshot_download
                self.model_path = snapshot_download(repo_id=repo_id)
            except ImportError as e:
                msg = "Please install `huggingface-hub` to use pretrained models from Hub."
                raise ImportError(msg) from e
            except Exception as e:
                msg = f"Failed to download model from {repo_id}: {e}"
                raise ValueError(msg) from e

        self.peykare_dict: dict[str, list[str]] = {}

        if self.model_path:
            self._setup()

    def _setup(self) -> None:
        if self.using_gpu:
            self._setup_gpu()
        else:
            logger.info("Using CPU for SpacyDependencyParser.")

        if self.model_path and Path(self.model_path).exists():
             self.model = spacy.load(self.model_path)
             self.model.tokenizer = self._custom_tokenizer

    def _setup_gpu(self) -> None:
        logger.info("GPU Setup Process Started...")
        if spacy.prefer_gpu(self.gpu_id):
            logger.info("GPU is available and ready for use.")
            spacy.require_gpu(self.gpu_id)
            self.gpu_availability = True
        else:
            logger.warning("GPU is not available; spaCy will use CPU.")
            self.gpu_availability = False

    def _custom_tokenizer(self, text: str) -> Doc:
        if self.model and text in self.peykare_dict:
            return Doc(self.model.vocab, self.peykare_dict[text])
        msg = "No tokenization available for input."
        raise ValueError(msg)

    def _update_dictionary(self, sents: list[list[str]]) -> None:
        """Add sentences to dictionary."""
        for sent in sents:
            key = " ".join(sent)
            if key not in self.peykare_dict:
                self.peykare_dict[key] = sent

    def parse(self, sentence: list[str]) -> DependencyGraph:
        """Parse a single sentence."""
        return next(self.parse_sents([sentence]))

    def parse_sents(self, sentences: list[list[str]]) -> Iterator[DependencyGraph]:
        """Parse multiple sentences using Spacy pipeline."""
        if self.model is None:
             msg = "Model not loaded."
             raise ValueError(msg)

        cleaned_sentences = []
        for sent in sentences:
            if sent and isinstance(sent[0], tuple):
                cleaned_sentences.append([word for word, _ in sent])
            else:
                cleaned_sentences.append(sent)

        docs = []
        for tokens in cleaned_sentences:
            doc = Doc(self.model.vocab, words=tokens)
            for _name, proc in self.model.pipeline:
                doc = proc(doc)
            docs.append(doc)

        for doc in docs:
            conll_lines = []
            for token in doc:
                head_index = token.head.i + 1
                if token.i == token.head.i:
                    head_index = 0

                lemma = token.lemma_ if token.lemma_ else "_"
                pos = token.pos_ if token.pos_ else "_"
                tag = token.tag_ if token.tag_ else "_"
                dep = token.dep_ if token.dep_ else "_"

                line = f"{token.i + 1}\t{token.text}\t{lemma}\t{pos}\t{tag}\t_\t{head_index}\t{dep}\t_\t_"
                conll_lines.append(line)

            conll_str = "\n".join(conll_lines)
            yield DependencyGraph(conll_str, top_relation_label="root")
