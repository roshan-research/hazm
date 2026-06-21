"""This module contains classes and functions for converting words or text into numerical vectors."""
import logging
import multiprocessing
import warnings
from collections.abc import Iterator
from pathlib import Path
from typing import Any

try:
    import numpy as np
    import smart_open
    from gensim.models import Doc2Vec
    from gensim.models import FastText
    from gensim.models import KeyedVectors
    from gensim.models.callbacks import CallbackAny2Vec
    from gensim.models.doc2vec import TaggedDocument
    from gensim.models.fasttext import load_facebook_model
    from gensim.scripts.glove2word2vec import glove2word2vec
    from numpy import ndarray
    EMBEDDINGS_AVAILABLE = True

except ImportError:
    EMBEDDINGS_AVAILABLE = False
    CallbackAny2Vec = object
    Doc2Vec = FastText = KeyedVectors = TaggedDocument = ndarray = Any

from hazm.normalizer import Normalizer
from hazm.word_tokenizer import word_tokenize


def _check_embeddings_deps():
    if not EMBEDDINGS_AVAILABLE:
        msg = "To use Embedding, please install hazm with the command: pip install hazm[all]."
        raise ImportError(msg)


logger = logging.getLogger(__name__)

SUPPORTED_EMBEDDINGS = ["fasttext", "keyedvector", "glove"]


class WordEmbedding:
    """This class includes functions for converting words into numerical vectors.

    Examples:
        >>> # Load from Hugging Face Hub
        >>> wordEmbedding = WordEmbedding.load(repo_id='roshan-research/hazm-word-embedding', model_filename='fasttext_skipgram_300.bin', model_type='fasttext')
        >>> # Or load from a local model file
        >>> # wordEmbedding = WordEmbedding.load(model_path='fasttext_skipgram_300.bin', model_type='fasttext')
    """

    def __init__(self, model: Any, model_type: str) -> None:
        """Constructor."""
        _check_embeddings_deps()
        self.model = model
        self.model_type = model_type

    @classmethod
    def load(
        cls,
        model_path: str | Path | None = None,
        model_type: str = "fasttext",
        repo_id: str | None = None,
        model_filename: str | None = None,
    ) -> "WordEmbedding":
        """Factory method to load the model.

        Args:
            model_path: Path to the model file.
            model_type: Type of the model ('fasttext', 'keyedvector', or 'glove').
            repo_id: Hugging Face repository ID.
            model_filename: Filename in the Hugging Face repository.

        Returns:
            An instance of WordEmbedding.
        """
        _check_embeddings_deps()
        final_model_path = model_path

        if repo_id and model_filename:
            try:
                from huggingface_hub import hf_hub_download
                from huggingface_hub import snapshot_download

                if model_type == "fasttext":
                     final_model_path = hf_hub_download(repo_id=repo_id, filename=model_filename)
                else:
                     cache_dir = snapshot_download(repo_id=repo_id)
                     final_model_path = Path(cache_dir) / model_filename

            except ImportError as e:
                msg = f"Failed to import huggingface-hub: {e}"
                raise ImportError(msg) from e
            except Exception as e:
                msg = f"Failed to download from {repo_id}: {e}"
                raise ValueError(msg) from e

        if not final_model_path:
             msg = "Either 'model_path' or 'repo_id' + 'model_filename' must be provided."
             raise ValueError(msg)

        if model_type not in SUPPORTED_EMBEDDINGS:
            msg = f'Model type "{model_type}" is not supported! Choose from {SUPPORTED_EMBEDDINGS}'
            raise KeyError(msg)

        final_model_path = str(final_model_path)
        model = None

        if model_type == "fasttext":
            try:
                model = load_facebook_model(final_model_path).wv
            except Exception:
                model = FastText.load(final_model_path).wv

        elif model_type == "keyedvector":
            binary = final_model_path.endswith("bin")
            model = KeyedVectors.load_word2vec_format(final_model_path, binary=binary)

        elif model_type == "glove":
            word2vec_addr = str(final_model_path) + "_word2vec_format.vec"
            if not Path(word2vec_addr).exists():
                logger.info("Converting Glove to Word2Vec format...")
                glove2word2vec(final_model_path, word2vec_addr)
            model = KeyedVectors.load_word2vec_format(word2vec_addr)
            model_type = "keyedvector"

        return cls(model, model_type)

    def train(
        self,
        dataset_path: str,
        workers: int = multiprocessing.cpu_count() - 1,
        vector_size: int = 200,
        epochs: int = 10,
        min_count: int = 5,
        fasttext_type: str = "skipgram",
        dest_path: str = "fasttext_word2vec_model.model",
    ) -> None:
        """Trains the model using Gensim FastText.

        Examples:
            >>> wordEmbedding.train(dataset_path='dataset.txt', workers=4, vector_size=300, epochs=30, fasttext_type='cbow')
        """
        sg = 1 if fasttext_type == "skipgram" else 0
        workers = max(1, workers)
        corpus = SentenceEmbeddingCorpus(dataset_path)
        sentences = (doc.words for doc in corpus)

        model = FastText(
            vector_size=vector_size,
            window=5,
            min_count=min_count,
            workers=workers,
            sg=sg,
            epochs=epochs,
        )

        model.build_vocab(corpus_iterable=sentences)
        model.train(corpus_iterable=sentences, total_examples=model.corpus_count, epochs=epochs)
        model.save(dest_path)
        self.model = model.wv

    def doesnt_match(self, words: list[str]) -> str:
        """Finds the word that does not match the others in the list.

        Examples:
            >>> wordEmbedding.doesnt_match(['سلام', 'درود', 'خداحافظ', 'پنجره'])
            'پنجره'
        """
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return self.model.doesnt_match(words)

    def similarity(self, word1: str, word2: str) -> float:
        """Calculates the similarity between two words.

        Examples:
            >>> wordEmbedding.similarity('ایران', 'آلمان')
            0.72231203
        """
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return float(self.model.similarity(word1, word2))

    def nearest_words(self, word: str, topn: int = 5) -> list[tuple[str, float]]:
        """Finds the nearest words to the given word.

        Examples:
            >>> wordEmbedding.nearest_words('ایران', topn=5)
            [('کشور', 0.8735059499740601), ...]
        """
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return self.model.most_similar(word, topn=topn)

    def get_normal_vector(self, word: str) -> ndarray:
        """Returns the normalized vector for the given word."""
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return self.model.get_vector(word=word, norm=True)

    def get_vocabs(self) -> list[str]:
        """Returns the list of vocabulary words."""
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return self.model.index_to_key

    def get_vocab_to_index(self) -> dict[str, int]:
        """Returns a dictionary mapping words to their indices."""
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return self.model.key_to_index

    def get_vectors(self) -> ndarray:
        """Returns the matrix of word vectors."""
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return self.model.vectors

    def get_vector_size(self) -> int:
        """Returns the size of the word vectors."""
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return self.model.vector_size

    def __getitem__(self, word: str) -> ndarray:
        """Returns the vector for the given word."""
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return self.model[word]


class SentenceEmbeddingCorpus:
    """Iterate over dataset for Doc2Vec training."""

    def __init__(self, data_path: str) -> None:
        _check_embeddings_deps()
        self.data_path = data_path
        self._normalizer = Normalizer()

    def __iter__(self) -> Iterator[TaggedDocument]:
        for i, list_of_words in enumerate(smart_open.open(self.data_path, encoding="utf-8")):
            yield TaggedDocument(
                word_tokenize(self._normalizer.normalize(list_of_words)),
                [i],
            )


class CallbackSentEmbedding(CallbackAny2Vec):
    """Callback for Doc2Vec training."""

    def __init__(self) -> None:
        _check_embeddings_deps()
        self.epoch = 0

    def on_epoch_end(self, model: Doc2Vec) -> None:
        logger.info("Epoch %d of %d...", self.epoch+1, model.epochs)
        self.epoch += 1


class SentEmbedding:
    """Converts sentences to vectors.

    Examples:
        >>> # Load from Hugging Face Hub
        >>> sentEmbedding = SentEmbedding.load(repo_id='roshan-research/hazm-sent-embedding', model_filename='sent2vec-naab.model')
        >>> # Or load from a local model file
        >>> # sentEmbedding = SentEmbedding.load(model_path='sent2vec-naab.model')
    """

    def __init__(self, model: Doc2Vec | None = None) -> None:
        """Constructor."""
        _check_embeddings_deps()
        self.model = model
        self.word_embedding: WordEmbedding | None = None
        if self.model:
            self._update_word_embedding()

    def _update_word_embedding(self) -> None:
        if self.model:
            self.word_embedding = WordEmbedding(self.model.wv, "keyedvector")

    @classmethod
    def load(
        cls,
        model_path: str | Path | None = None,
        repo_id: str | None = None,
        model_filename: str | None = None,
    ) -> "SentEmbedding":
        """Factory method to load the model.

        Args:
            model_path: Path to the model file.
            repo_id: Hugging Face repository ID.
            model_filename: Filename in the Hugging Face repository.

        Returns:
            An instance of SentEmbedding.
        """
        final_model_path = model_path
        if repo_id and model_filename:
            try:
                from huggingface_hub import snapshot_download
                cache_dir = snapshot_download(repo_id=repo_id)
                final_model_path = Path(cache_dir) / model_filename
            except Exception as e:
                msg = f"Failed to import huggingface-hub: {e}"
                raise ValueError(msg) from e

        if not final_model_path:
            msg = "Either 'model_path' or 'repo_id' + 'model_filename' must be provided."
            raise ValueError(msg)

        model = Doc2Vec.load(str(final_model_path))
        return cls(model)

    def train(
        self,
        dataset_path: str,
        min_count: int = 5,
        workers: int = multiprocessing.cpu_count() - 1,
        windows: int = 5,
        vector_size: int = 300,
        epochs: int = 10,
        dest_path: str = "gensim_sent2vec.model",
    ) -> None:
        """Trains the model using Gensim Doc2Vec."""
        workers = max(1, workers)
        doc = SentenceEmbeddingCorpus(dataset_path)
        model = Doc2Vec(min_count=min_count, window=windows, vector_size=vector_size, workers=workers)
        model.build_vocab(doc)
        model.train(doc, total_examples=model.corpus_count, epochs=epochs, callbacks=[CallbackSentEmbedding()])
        model.dv.vectors = np.empty((0, vector_size))
        self.model = model
        self._update_word_embedding()
        model.save(dest_path)

    def get_sentence_vector(self, sent: str) -> ndarray:
        """Returns the vector for the given sentence.

        Examples:
            >>> result = sentEmbedding.get_sentence_vector('این متن به برداری تبدیل خواهد شد')
        """
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        tokenized_sent = word_tokenize(sent)
        return self.model.infer_vector(tokenized_sent)

    def similarity(self, sent1: str, sent2: str) -> float:
        """Calculates the similarity between two sentences.

        Examples:
            >>> result = sentEmbedding.similarity('شیر حیوانی وحشی است', 'پلنگ از دیگر جانوران درنده است')
        """
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return float(self.model.similarity_unseen_docs(word_tokenize(sent1), word_tokenize(sent2)))

    def get_vector_size(self) -> int:
        """Returns the size of the sentence vectors."""
        if not self.model:
            msg = "Model must be loaded first."
            raise AttributeError(msg)
        return self.model.vector_size

    def __getitem__(self, sent: str) -> ndarray:
        return self.get_sentence_vector(sent)
