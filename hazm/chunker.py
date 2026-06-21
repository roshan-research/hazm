# hazm/chunker.py
"""This module contains classes and functions for shallow parsing (chunking) of text into noun, verb, and prepositional phrases."""

import logging
import subprocess
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from nltk.chunk import RegexpParser
from nltk.chunk import conlltags2tree
from nltk.chunk import tree2conlltags
from nltk.chunk.util import ChunkScore
from nltk.tree import Tree

try:
    import spacy
    from spacy.tokens import Doc
    from spacy.tokens import DocBin
    from spacy.vocab import Vocab
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    Doc = DocBin = Vocab = Any

from tqdm import tqdm

from hazm.pos_tagger import POSTagger
from hazm.sequence_tagger import IOBTagger
from hazm.types import ChunkedSentence
from hazm.types import Sentence
from hazm.types import TaggedSentence
from hazm.types import Token

logger = logging.getLogger(__name__)


def tree2brackets(tree: Tree) -> str:
    """Converts a tree object to a bracketed string representation.

    Examples:
        >>> chunker = Chunker(repo_id="roshan-research/hazm-chunker", model_filename="chunker.model")
        >>> tree = chunker.parse([('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')])
        >>> tree2brackets(tree)
        '[نامه ایشان NP] [را POSTP] [دریافت داشتم VP] .'

    Args:
        tree: The parse tree to be converted.

    Returns:
        A bracketed string representation of the tree.
    """
    s, tag = "", ""
    for item in tree2conlltags(tree):
        word, _, chunk = item
        if chunk[0] in {"B", "O"} and tag:
            s += tag + "] "
            tag = ""

        if chunk[0] == "B":
            tag = chunk.split("-")[1]
            s += "["
        s += word + " "

    if tag:
        s += tag + "] "

    return s.strip()


class Chunker(IOBTagger):
    """Class for chunking text, training, and evaluating chunker models."""

    def __init__(
        self,
        model: str | Path | None = None,
        data_maker: Any = None,
        repo_id: str | None = None,
        model_filename: str | None = None,
    ) -> None:
        """Constructor.

        Examples:
            >>> # Loading from Hugging Face Hub
            >>> chunker = Chunker(repo_id="roshan-research/hazm-chunker", model_filename="chunker.model")
            >>> # Loading from a local model file
            >>> # chunker = Chunker(model='resources/chunker.model')

        Args:
            model: Path to the local model file.
            data_maker: Custom data maker function.
            repo_id: Hugging Face repository ID (e.g., "roshan-research/hazm-chunker").
            model_filename: Filename inside the repository (e.g., "chunker.model").
        """
        final_data_maker = data_maker if data_maker is not None else self.data_maker
        self.posTagger = POSTagger()

        # Resolve model path logic
        final_model_path = model

        if repo_id and model_filename:
            try:
                from huggingface_hub import hf_hub_download
                final_model_path = hf_hub_download(repo_id=repo_id, filename=model_filename)
            except ImportError as e:
                msg = "Please install `huggingface-hub` to use pretrained models from Hub."
                raise ImportError(msg) from e
            except Exception as e:
                msg = f"Failed to download model from {repo_id}: {e}"
                raise ValueError(msg) from e

        super().__init__(final_model_path, final_data_maker)

    def data_maker(self, tokens: list[TaggedSentence]) -> list[list[dict[str, Any]]]:
        """Converts tokens into features.

        Examples:
            >>> tokens = [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]]
            >>> features = chunker.data_maker(tokens)
            >>> features[0][0]['pos']
            'PRON'

        Args:
            tokens: A list of tagged sentences.

        Returns:
            A list of lists of feature dictionaries.
        """
        words = [[word for word, _ in token] for token in tokens]
        tags = [[tag for _, tag in token] for token in tokens]
        return [
            [
                self.features(words=word_tokens, pos_tags=tag_tokens, index=index)
                for index in range(len(word_tokens))
            ]
            for word_tokens, tag_tokens in zip(words, tags, strict=False)
        ]

    def features(
        self,
        words: list[str],
        pos_tags: list[str],
        index: int,
    ) -> dict[str, Any]:
        """Extracts features for a word at a given index.

        Args:
            words: List of words in the sentence.
            pos_tags: List of POS tags for the words.
            index: The index of the word to extract features for.

        Returns:
            A dictionary of features.
        """
        word_features = self.posTagger.features(words, index)
        word_features.update(
            {
                "pos": pos_tags[index],
                "prev_pos": "" if index == 0 else pos_tags[index - 1],
                "next_pos": "" if index == len(pos_tags) - 1 else pos_tags[index + 1],
            },
        )
        return word_features

    def train(
        self,
        trees: list[Tree],
        c1: float = 0.4,
        c2: float = 0.04,
        max_iteration: int = 400,
        verbose: bool = True,
        file_name: str = "chunker_crf.model",
        report_duration: bool = True,
    ) -> None:
        """Trains the chunker model.

        Args:
            trees: A list of parse trees for training.
            c1: Coefficient for L1 regularization.
            c2: Coefficient for L2 regularization.
            max_iteration: Maximum number of iterations for training.
            verbose: Whether to print verbose output.
            file_name: The name of the file to save the trained model.
            report_duration: Whether to report the training duration.
        """
        tagged_list = [tree2conlltags(tree) for tree in trees]
        return super().train(
            tagged_list,
            c1,
            c2,
            max_iteration,
            verbose,
            file_name,
            report_duration,
        )

    def parse(self, sentence: TaggedSentence) -> Tree:
        """Parses a tagged sentence into a chunk tree.

        Examples:
            >>> tree = chunker.parse([('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')])
            >>> print(tree)
            (S
              (NP نامه/NOUN,EZ ایشان/PRON)
              (POSTP را/ADP)
              (VP دریافت/NOUN داشتم/VERB)
              ./PUNCT)

        Args:
            sentence: A tagged sentence.

        Returns:
            The parsed chunk tree.
        """
        tagged = super().tag(sentence)
        return conlltags2tree(tagged)

    def parse_sents(self, sentences: list[TaggedSentence]) -> Iterator[Tree]:
        """Parses a list of tagged sentences into chunk trees.

        Examples:
            >>> sentences = [[('نامه', 'NOUN,EZ'), ('ایشان', 'PRON')], [('من', 'PRON'), ('رفتم', 'VERB')]]
            >>> trees = list(chunker.parse_sents(sentences))

        Args:
            sentences: A list of tagged sentences.

        Yields:
            The parsed chunk tree for each sentence.
        """
        for conlltagged in super().tag_sents(sentences):
            yield conlltags2tree(conlltagged)

    def evaluate(self, trees: list[Tree]) -> float:
        """Evaluates the accuracy of the chunker.

        Examples:
            >>> trees = [chunker.parse([('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')])]
            >>> chunker.evaluate(trees)
            1.0

        Args:
            trees: A list of gold standard parse trees.

        Returns:
            The accuracy of the chunker.
        """
        tagged_sents = [tree2conlltags(tree) for tree in trees]
        return super().evaluate(tagged_sents)


class RuleBasedChunker(RegexpParser):
    """Rule-based chunker using regular expressions."""

    def __init__(self) -> None:
        """Constructor."""
        grammar = r"""
            NP:
                <P>{<N>}<V>

            VP:
                <.*[^e]>{<N>?<V>}
                {<V>}

            ADVP:
                {<ADVe?><AJ>?}

            ADJP:
                <.*[^e]>{<AJe?>}

            NP:
                {<DETe?|Ne?|NUMe?|AJe|PRO|CL|RESe?><DETe?|Ne?|NUMe?|AJe?|PRO|CL|RESe?>*}
                <N>}{<.*e?>

            ADJP:
                {<AJe?>}

            POSTP:
                {<POSTP>}

            PP:
                {<Pe?>+}
        """
        super().__init__(grammar=grammar)


class SpacyChunker(Chunker):
    """Chunker based on the Spacy library."""

    def __init__(
        self,
        model_path: str | Path | None = None,
        using_gpu: bool = False,
        gpu_id: int = 0,
        repo_id: str | None = None,
    ) -> None:
        """Constructor.

        Args:
            model_path: Path to the local Spacy model.
            using_gpu: Whether to use GPU.
            gpu_id: The ID of the GPU to use.
            repo_id: Hugging Face repository ID.
        """
        if not SPACY_AVAILABLE:
            msg = "To use Spacy-based models, please install hazm: pip install hazm[all]"
            raise ImportError(msg)

        super().__init__()
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
            logger.info("Using CPU for SpacyChunker.")

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
        """Adds sentences to the dictionary for custom tokenization.

        Args:
            sents: A list of sentences, where each sentence is a list of words.
        """
        for sent in sents:
            key = " ".join(sent)
            if key not in self.peykare_dict:
                self.peykare_dict[key] = sent

    def _setup_dataset(
        self,
        sents: list[ChunkedSentence],
        saved_directory: str,
        dataset_type: str,
    ) -> None:
        assert dataset_type in ["train", "dev", "test"]
        db = DocBin()
        for sent in tqdm(sents):
            words = [word[0] for word in sent]
            tags = [word[2] for word in sent] # Chunk tags
            # Note: Spacy usually expects POS tags in tag_ and NER/Chunk in ents or specific attributes.
            # Here we map chunk tags to tag_ attribute as per original code logic for simplicity,
            # though standard way is using ents for chunks.
            doc = Doc(Vocab(strings=words), words=words)
            for d, tag in zip(doc, tags, strict=False):
                d.tag_ = tag
            db.add(doc)

        path = Path(saved_directory)
        if not path.exists():
            path.mkdir(parents=True)

        db.to_disk(f"{saved_directory}/{dataset_type}.spacy")

    def train(
        self,
        train_dataset: list[ChunkedSentence],
        test_dataset: list[ChunkedSentence],
        data_directory: str,
        base_config_file: str,
        train_config_path: str,
        output_dir: str,
        use_direct_config: bool = False,
    ) -> None:
        """Trains the spaCy chunker model.

        Args:
            train_dataset: The training dataset.
            test_dataset: The testing dataset.
            data_directory: Directory to save processed data.
            base_config_file: Path to the base configuration file.
            train_config_path: Path to the training configuration file.
            output_dir: Directory to save the trained model.
            use_direct_config: Whether to use the configuration file directly.
        """
        if not use_direct_config:
            logger.info("Setting up training configuration...")
            self.train_config_file = train_config_path
            subprocess.run(
                ["python", "-m", "spacy", "init", "fill-config", str(base_config_file), str(train_config_path)],
                check=False,
            )
        else:
            self.train_config_file = train_config_path

        if train_dataset:
            self._setup_dataset(
                sents=train_dataset,
                saved_directory=data_directory,
                dataset_type="train",
            )

        if test_dataset:
            self._setup_dataset(
                sents=test_dataset,
                saved_directory=data_directory,
                dataset_type="test",
            )

        train_data = f"{data_directory}/train.spacy"
        test_data = f"{data_directory}/test.spacy"

        cmd = ["python", "-m", "spacy", "train", str(self.train_config_file),
               "--output", f"./{output_dir}", "--paths.train", f"./{train_data}", "--paths.dev", f"./{test_data}"]
        if self.gpu_availability:
            cmd.extend(["--gpu-id", str(self.gpu_id)])

        subprocess.run(cmd, check=False)
        self.model_path = f"{output_dir}/model-last"

        if test_dataset:
            tokens_list = [[w for w, _, _ in sent] for sent in test_dataset]
            self._update_dictionary(tokens_list)
            self.model = spacy.load(self.model_path)
            self.model.tokenizer = self._custom_tokenizer

    def evaluate(self, test_sents: list[ChunkedSentence]) -> ChunkScore:
        """Evaluates the accuracy of the chunker.

        Args:
            test_sents: A list of chunked sentences for testing.

        Returns:
            The chunk score.
        """
        golds = test_sents
        # Extract sentence tuples for parsing
        test_inp = [
            [(word, tag) for word, tag, _ in sent]
            for sent in golds
        ]

        parsed = self.parse_sents(test_inp)
        preds_tree = list(parsed)
        golds_tree = [conlltags2tree(sent) for sent in golds]

        chunkscore = ChunkScore()
        for pred, correct in zip(preds_tree, golds_tree, strict=False):
            chunkscore.score(correct, pred)

        print("Accuracy:", chunkscore.accuracy())
        print("Precision:", chunkscore.precision())
        print("Recall:", chunkscore.recall())
        print("F_Score:", chunkscore.f_measure())

        return chunkscore

    def parse(self, sentence: TaggedSentence) -> Tree:
        """Parses a single sentence.

        Args:
            sentence: A tagged sentence.

        Returns:
            The parsed tree.
        """
        tokens = [w for w, _ in sentence]
        if self.model is None:
             msg = "Model not loaded."
             raise ValueError(msg)

        self._update_dictionary([tokens])

        doc = self.model(" ".join(tokens))
        words = [w for w, _ in sentence]
        tags = [tag for _, tag in sentence]
        preds = [w.tag_ for w in doc] # Assuming model predicts chunks in tag_

        chunk = list(zip(words, tags, preds, strict=False))
        return conlltags2tree(chunk)

    def parse_sents(
        self,
        sentences: list[TaggedSentence],
        batch_size: int = 128,
    ) -> Iterator[Tree]:
        """Parses multiple sentences.

        Args:
            sentences: A list of tagged sentences.
            batch_size: Batch size for processing.

        Yields:
            The parsed tree for each sentence.
        """
        tokens_list = [[w for w, _ in sent] for sent in sentences]
        if self.model is None:
             msg = "Model not loaded."
             raise ValueError(msg)

        self._update_dictionary(tokens_list)

        docs = list(
            self.model.pipe(
                (" ".join(sent) for sent in tokens_list),
                batch_size=batch_size,
            ),
        )

        for i, doc in enumerate(docs):
            words = [w for w, _ in sentences[i]]
            tags = [tag for _, tag in sentences[i]]
            preds = [w.tag_ for w in doc]
            chunk = list(zip(words, tags, preds, strict=False))
            yield conlltags2tree(chunk)
