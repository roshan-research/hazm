import subprocess
from typing import Tuple , List
from tqdm import tqdm



class HazmNER:
    from spacy.tokens import Doc
    from spacy.tokens import DocBin
    from spacy.vocab import Vocab

    def __init__(self, model_path, use_gpu=False):
        """
        Initialize the HazmNER object.

        Parameters:
            model_path (str): The path to the pre-trained NER model.
            use_gpu (bool): Whether to use GPU for processing.
        """
        self.model_path = model_path
        self.use_gpu = use_gpu
        self.model = self._load_model(model_path, use_gpu)
        
    def predict_entities(self, sentences):
        """
        Predict named entities in a list of sentences.

        Parameters:
            sentences (list of str): List of sentences to predict named entities.

        Returns:
            list of list of tuple: Predicted named entities for each sentence.
        """
        names = []
        for sentence in sentences:
            entities = self.predict_entity(sentence)
            names.append(entities)
        return names
    
    def predict_entity(self, sentence):
        """
        Predict named entities in a single sentence.

        Parameters:
            sentence (str): Input sentence to predict named entities.

        Returns:
            list of tuple: Predicted named entities in the input sentence.
        """
        doc = self.model(sentence)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    def evaluate_model(self, dataset_path):
        """
        Evaluate the performance of the NER model on a dataset.

        Parameters:
            dataset_path (str): Path to the evaluation dataset.
        """
        subprocess.run(f"python -m spacy evaluate {self.model_path} {dataset_path}")
    
    def _load_model(self, model_path, use_gpu):
        """
        Load the trained NER model.

        Parameters:
            model_path (str): Path to the trained model.
            use_gpu (bool): Whether to use GPU for processing.

        Returns:
            spacy.Language: Loaded NER model.
        """
        import spacy
        if use_gpu:
            spacy.require_gpu()
        return spacy.load(model_path)
