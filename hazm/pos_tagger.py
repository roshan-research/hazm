"""This module contains classes and functions for POS tagging."""

import logging
import subprocess
from pathlib import Path
from typing import Any

from nltk.tag import stanford

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

from hazm.api import TaggerProtocol
from hazm.sequence_tagger import SequenceTagger
from hazm.types import Sentence
from hazm.types import TaggedSentence
from hazm.types import Token

logger = logging.getLogger(__name__)

PUNCTUATION_LIST = [
    '"', "#", "(", ")", "*", ",", "-", ".", "/", ":", "[", "]",
    "«", "»", "،", ";", "?", "!",
]


class POSTagger(SequenceTagger, TaggerProtocol):
    """Class for POS tagging.

    Examples:
        >>> # Load from Hugging Face Hub
        >>> tagger = POSTagger(repo_id="roshan-research/hazm-postagger", model_filename="pos_tagger.model")
        >>> # Or load from a local model file
        >>> # tagger = POSTagger(model="pos_tagger.model")
    """

    def __init__(
        self,
        model: str | Path | None = None,
        data_maker: Any = None,
        universal_tag: bool = False,
        repo_id: str | None = None,
        model_filename: str | None = None,
    ) -> None:
        """Constructor.

        Examples:
            >>> # Loading from Hugging Face Hub
            >>> tagger = POSTagger(repo_id="roshan-research/hazm-postagger", model_filename="pos_tagger.model")
            >>> # Loading from a local model file
            >>> # tagger = POSTagger(model="resources/pos_tagger.model")

        Args:
            model: Path to the local model file.
            data_maker: Custom data maker function.
            universal_tag: Whether to use universal POS tags.
            repo_id: Hugging Face repository ID (e.g., "roshan-research/hazm-postagger").
            model_filename: Filename inside the repository (e.g., "pos_tagger.model").
        """
        final_data_maker = data_maker if data_maker is not None else self.data_maker
        self.__is_universal = universal_tag

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

    def __universal_converter(self, tagged_list: TaggedSentence) -> TaggedSentence:
        """Converts POS tags to universal tags."""
        return [(word, tag.split(",")[0]) for word, tag in tagged_list]

    def __is_punc(self, word: str) -> bool:
        """Checks if a word is punctuation."""
        return word in PUNCTUATION_LIST

    def data_maker(self, tokens: list[Sentence]) -> list[list[dict[str, Any]]]:
        """Converts tokens into features.

        Examples:
            >>> tokens = [['دلم', 'اینجا', 'مانده‌است', '.']]
            >>> features = tagger.data_maker(tokens)
            >>> features[0][0]['word']
            'دلم'

        Args:
            tokens: A list of sentences, where each sentence is a list of tokens.

        Returns:
            A list of lists of feature dictionaries.
        """
        return [
            [self.features(token, index) for index in range(len(token))]
            for token in tokens
        ]

    def features(self, sentence: Sentence, index: int) -> dict[str, Any]:
        """Extracts features for a word at a given index.

        Args:
            sentence: The sentence containing the word.
            index: The index of the word.

        Returns:
            A dictionary of features.
        """
        word = sentence[index]
        return {
            "word": word,
            "is_first": index == 0,
            "is_last": index == len(sentence) - 1,
            # *ix
            "prefix-1": word[0],
            "prefix-2": word[:2],
            "prefix-3": word[:3],
            "suffix-1": word[-1],
            "suffix-2": word[-2:],
            "suffix-3": word[-3:],
            # word
            "prev_word": "" if index == 0 else sentence[index - 1],
            "two_prev_word": "" if index <= 1 else sentence[index - 2],
            "next_word": "" if index == len(sentence) - 1 else sentence[index + 1],
            "two_next_word": (
                ""
                if index >= len(sentence) - 2
                else sentence[index + 2]
            ),
            # digit
            "is_numeric": word.isdigit(),
            "prev_is_numeric": "" if index == 0 else sentence[index - 1].isdigit(),
            "next_is_numeric": (
                "" if index == len(sentence) - 1 else sentence[index + 1].isdigit()
            ),
            # punc
            "is_punc": self.__is_punc(word),
            "prev_is_punc": "" if index == 0 else self.__is_punc(sentence[index - 1]),
            "next_is_punc": (
                ""
                if index == len(sentence) - 1
                else self.__is_punc(sentence[index + 1])
            ),
        }

    def tag(self, tokens: Sentence) -> TaggedSentence:
        """Tags a single sentence.

        Examples:
            >>> tagger.tag(['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.'])
            [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]

        Args:
            tokens: A list of tokens representing a sentence.

        Returns:
            A tagged sentence (list of (word, tag) tuples).
        """
        tagged_token = super().tag(tokens)
        return (
            self.__universal_converter(tagged_token)
            if self.__is_universal
            else tagged_token
        )

    def tag_sents(self, sentences: list[Sentence]) -> list[TaggedSentence]:
        """Tags multiple sentences.

        Examples:
            >>> tagger.tag_sents([['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.']])
            [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]]

        Args:
            sentences: A list of sentences to tag.

        Returns:
            A list of tagged sentences.
        """
        tagged_sents = super().tag_sents(sentences)
        return (
            [self.__universal_converter(tagged_sent) for tagged_sent in tagged_sents]
            if self.__is_universal
            else tagged_sents
        )


class StanfordPOSTagger(stanford.StanfordPOSTagger):
    """Wrapper for Stanford POS Tagger."""

    def __init__(
        self,
        model_filename: str,
        path_to_jar: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Constructor.

        Args:
            model_filename: Path to the model file.
            path_to_jar: Path to the Stanford POS Tagger JAR file.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self._SEPARATOR = "/"
        super().__init__(
            model_filename,
            path_to_jar,
            *args,
            **kwargs,
        )

    def tag(self, tokens: Sentence) -> TaggedSentence:
        """Tags a single sentence.

        Args:
            tokens: A list of tokens representing a sentence.

        Returns:
            A tagged sentence.
        """
        return self.tag_sents([tokens])[0]

    def tag_sents(self, sentences: list[Sentence]) -> list[TaggedSentence]:
        """Tags multiple sentences.

        Args:
            sentences: A list of sentences to tag.

        Returns:
            A list of tagged sentences.
        """
        refined = ([w.replace(" ", "_") for w in s] for s in sentences)
        return super().tag_sents(list(refined))


class SpacyPOSTagger(POSTagger):
    """POS Tagger based on spaCy."""

    def __init__(
        self,
        model_path: str | Path | None = None,
        using_gpu: bool = False,
        gpu_id: int = 0,
        repo_id: str | None = None,
        model_filename: str | None = None, # noqa: ARG002
    ) -> None:
        """Constructor.

        Args:
            model_path: Path to the local model directory.
            using_gpu: Whether to use GPU.
            gpu_id: The ID of the GPU to use.
            repo_id: Hugging Face repository ID.
            model_filename: Filename (unused for spaCy models).
        """
        if not SPACY_AVAILABLE:
            msg = "To use SpacyPOSTagger, install hazm with the command: pip install hazm[all]"
            raise ImportError(msg)

        super().__init__(universal_tag=True)
        self.model_path = str(model_path) if model_path else None
        self.using_gpu = using_gpu
        self.gpu_id = gpu_id
        self.tagger = None
        self.gpu_availability = False

        if repo_id:
            try:
                from huggingface_hub import snapshot_download
                # spaCy models are usually a directory, so we download the whole repo
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
        """Sets up the spaCy model and GPU if requested."""
        if self.using_gpu:
            self._setup_gpu()
        else:
            logger.info("Using CPU for SpacyPOSTagger.")

        if self.model_path and Path(self.model_path).exists():
             self.tagger = spacy.load(self.model_path)
             self.tagger.tokenizer = self._custom_tokenizer

    def _setup_gpu(self) -> None:
        """Checks and sets up GPU availability."""
        logger.info("GPU Setup Process Started...")
        if spacy.prefer_gpu(gpu_id=self.gpu_id):
            logger.info("GPU is available and ready for use.")
            spacy.require_gpu(gpu_id=self.gpu_id)
            self.gpu_availability = True
        else:
            logger.warning("GPU is not available; spaCy will use CPU.")
            self.gpu_availability = False

    def _custom_tokenizer(self, text: str) -> Doc:
        """Custom tokenizer for spaCy."""
        if self.tagger and text in self.peykare_dict:
            return Doc(self.tagger.vocab, self.peykare_dict[text])
        msg = "No tokenization available for input."
        raise ValueError(msg)

    def _update_dictionary(self, sents: list[Sentence]) -> None:
        """Adds sentences to the dictionary for custom tokenization.

        Args:
            sents: A list of sentences.
        """
        for sent in sents:
            key = " ".join(sent)
            if key not in self.peykare_dict:
                self.peykare_dict[key] = sent

    def _setup_dataset(
        self,
        dataset: list[TaggedSentence],
        saved_directory: str,
        data_type: str = "train",
    ) -> None:
        """Prepares dataset for spaCy training.

        Args:
            dataset: The dataset to prepare.
            saved_directory: Directory to save the prepared data.
            data_type: 'train' or 'test'.
        """
        assert data_type in ["train", "test"]
        db = DocBin()
        for sent in tqdm(dataset):
            words = [word for word, _ in sent]
            tags = [tag for _, tag in sent]
            doc = Doc(Vocab(strings=words), words=words)
            for d, tag in zip(doc, tags, strict=False):
                d.tag_ = tag
            db.add(doc)

        path = Path(saved_directory)
        if not path.exists():
            path.mkdir(parents=True)

        db.to_disk(f"{saved_directory}/{data_type}.spacy")

    def tag(self, tokens: Sentence, universal_tag: bool = True) -> TaggedSentence:
        """Tags a single sentence.

        Args:
            tokens: A list of tokens representing a sentence.
            universal_tag: Whether to use universal POS tags.

        Returns:
            A tagged sentence.
        """
        if self.tagger is None:
             msg = "Model is not loaded. Please provide model_path in init."
             raise ValueError(msg)

        self._update_dictionary([tokens])

        text = " ".join(tokens)
        doc = self.tagger(text)

        if universal_tag:
            tags = [tok.tag_.replace(",EZ", "") for tok in doc]
        else:
            tags = [tok.tag_ for tok in doc]

        return list(zip(tokens, tags, strict=False))

    def tag_sents(
        self,
        sents: list[Sentence],
        universal_tag: bool = True,
        batch_size: int = 128,
    ) -> list[TaggedSentence]:
        """Tags multiple sentences.

        Args:
            sents: A list of sentences to tag.
            universal_tag: Whether to use universal POS tags.
            batch_size: Batch size for processing.

        Returns:
            A list of tagged sentences.
        """
        if self.tagger is None:
             msg = "Model is not loaded."
             raise ValueError(msg)

        self._update_dictionary(sents)

        docs = list(
            self.tagger.pipe(
                (" ".join(sent) for sent in sents),
                batch_size=batch_size,
            ),
        )

        result = []
        for sent, doc in zip(sents, docs, strict=False):
            if universal_tag:
                tags = [tok.tag_.replace(",EZ", "") for tok in doc]
            else:
                tags = [tok.tag_ for tok in doc]
            result.append(list(zip(sent, tags, strict=False)))

        return result

    def train(
        self,
        train_dataset: list[TaggedSentence],
        test_dataset: list[TaggedSentence],
        data_directory: str,
        base_config_file: str,
        train_config_path: str,
        output_dir: str,
        use_direct_config: bool = False,
    ) -> None:
        """Trains the spaCy model.

        Args:
            train_dataset: The training dataset.
            test_dataset: The testing dataset.
            data_directory: Directory to save processed data.
            base_config_file: Path to the base configuration file.
            train_config_path: Path to the training configuration file.
            output_dir: Directory to save the trained model.
            use_direct_config: Whether to use the configuration file directly.
        """
        self.spacy_train_directory = data_directory

        if train_dataset:
            self._setup_dataset(
                dataset=train_dataset,
                saved_directory=data_directory,
                data_type="train",
            )

        if test_dataset:
            self._setup_dataset(
                dataset=test_dataset,
                saved_directory=data_directory,
                data_type="test",
            )

        train_data = f"{data_directory}/train.spacy"
        test_data = f"{data_directory}/test.spacy"

        if not use_direct_config:
            logger.info("Setting up training configuration...")
            subprocess.run(
                ["python", "-m", "spacy", "init", "fill-config", str(base_config_file), str(train_config_path)],
                check=False,
            )

        cmd = ["python", "-m", "spacy", "train", str(train_config_path),
               "--output", f"./{output_dir}", "--paths.train", f"./{train_data}", "--paths.dev", f"./{test_data}"]
        if self.gpu_availability:
            cmd.extend(["--gpu-id", str(self.gpu_id)])

        subprocess.run(cmd, check=False)
        self.model_path = f"{output_dir}/model-last"

        if test_dataset:
            tokens_list = [[w for w, _ in sent] for sent in test_dataset]
            self._update_dictionary(tokens_list)
            self.tagger = spacy.load(self.model_path)
            self.tagger.tokenizer = self._custom_tokenizer

    def evaluate(self, test_sents: list[TaggedSentence], batch_size: int = 128) -> None:
        """Evaluates the model.

        Args:
            test_sents: A list of tagged sentences for testing.
            batch_size: Batch size for processing.
        """
        tokens_list = [[w for w, _ in sent] for sent in test_sents]
        self._update_dictionary(tokens_list)

        if not self.tagger:
            msg = "Model does not exist."
            raise ValueError(msg)

        gold_labels = [[tag for _, tag in sent] for sent in test_sents]
        prediction_labels = self.tag_sents(tokens_list, batch_size=batch_size, universal_tag=False) # Get raw tags first
        prediction_tags = [[tag for _, tag in sent] for sent in prediction_labels]

        print("-----------------------------------------")
        self._evaluate_tags(gold_labels, prediction_tags, use_ez_tags=True)
        print("-----------------------------------------")
        self._evaluate_tags(gold_labels, prediction_tags, use_ez_tags=False)

    def _evaluate_tags(
        self,
        golds: list[list[str]],
        predictions: list[list[str]],
        use_ez_tags: bool,
    ) -> None:
        """Helper function to evaluate tags."""
        try:
            from sklearn.metrics import classification_report
        except ImportError:
            msg = "To evaluate the model, please install hazm with the command: pip install hazm[all]."
            raise ImportError(msg) from None

        predictions_cleaned = []
        golds_cleaned = []

        def clean_tag(tag: str) -> str:
            if use_ez_tags:
                return "EZ" if "EZ" in tag else "-"
            return tag.replace(",EZ", "")

        for preds, gold_labels in zip(predictions, golds, strict=False):
            for pred in preds:
                predictions_cleaned.append(clean_tag(pred))
            for gold in gold_labels:
                golds_cleaned.append(clean_tag(gold))

        print(classification_report(golds_cleaned, predictions_cleaned))
