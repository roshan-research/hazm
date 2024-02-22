import subprocess
from typing import Tuple , List
from tqdm import tqdm



def prepare_conll_data_format(
    path: str,
    sep: str = "\t",
    verbose: bool = True,
) -> Tuple[List[List[str]], List[List[str]]]:
    """
    Prepare data in CoNNL-like format.
    
    Args:
    - path (str): The path to the CoNNL-formatted file.
    - sep (str): Separator used to split tokens and labels. Default is "\t".
    - lower (bool): Flag indicating whether to convert tokens to lowercase. Default is True.
    - verbose (bool): Flag indicating whether to display progress bar. Default is True.
    
    Returns:
    - Tuple[List[List[str]], List[List[str]]]: A tuple containing token sequences and label sequences.
    """
    # Initialize lists to store token and label sequences
    token_seq = []
    label_seq = []
    
    # Open the file and read line by line
    with open(path, mode="r", encoding="utf-8") as fp:
        tokens = []
        labels = []
        
        # Optionally display a progress bar
        if verbose:
            fp = tqdm(fp)
        
        # Iterate through each line in the file
        for line in fp:
            # If the line is not empty
            if line != "\n":
                try:
                    # Split the line into token and label using the specified separator
                    token, label = line.strip().split(sep)
                    tokens.append(token)
                    labels.append(label)
                except:
                    continue
            else:
                # If encounter an empty line, indicates the end of a sentence
                if len(tokens) > 0:
                    token_seq.append(tokens)
                    label_seq.append(labels)
                tokens = []
                labels = []

    return token_seq, label_seq


def convert_to_spacy_format(data):
    """
    Convert data from CoNNL-like format to SpaCy format.
    
    Args:
    - data (List[Tuple[str, str]]): List of tuples containing token-label pairs.
    
    Returns:
    - Tuple[str, List[Tuple[int, int, str]]]: A tuple containing the processed text and entity annotations.
    """
    # Initialize variables to store text and entities
    text = ''
    entities = []
    
    # Iterate through each token-label pair
    for word, label in data:
        # If the label is 'O', append the word to the text
        if label == 'O':
            text += ' ' + word
        else:
            # If the label indicates an entity, update text and entities accordingly
            text += ' ' + word
            if text:
                entities.append((len(text) - len(word) - 1, len(text) - 1, label))
            else:
                entities.append((0, len(word) - 1, label))

    # Merge adjacent entities with the same label
    if text:
        return text.strip(), merge_tags(entities)
    else:
        return text, []
    
def merge_tags(tags):
    """
    Merge adjacent entities with the same label.
    
    Args:
    - tags (List[Tuple[int, int, str]]): List of entity annotations.
    
    Returns:
    - List[Tuple[int, int, str]]: List of merged entity annotations.
    """
    merged_tags = []
    current_tag = None
    start = None
    end = None

    for i, (start_idx, end_idx, tag) in enumerate(tags):
        if tag.startswith('B-'):
            if current_tag is not None:
                merged_tags.append((start, end, current_tag))
            current_tag = tag[2:]
            start = start_idx
            end = end_idx
        elif tag.startswith('I-'):
            if current_tag is not None and tag[2:] == current_tag:
                end = end_idx
        else:  # tag == 'O'
            if current_tag is not None:
                merged_tags.append((start, end, current_tag))
                current_tag = None

    if current_tag is not None:
        merged_tags.append((start, end, current_tag))

    return merged_tags




class BaseNER(object):
    def __init__(self,model_path):
        """
            load_data: Load data from a file or any data source.
            preprocess_data: Preprocess the loaded data, including tokenization, normalization, and any other necessary steps.
            train_model: Train the NER model using the preprocessed data.
            evaluate_model: Evaluate the trained model using appropriate metrics.
            predict_entities: Predict named entities in new text using the trained model.
            save_model: Save the trained NER model for future use.
            load_model: Load a pre-trained NER model from disk.

        """
        pass



class HazmNER(BaseNER):
    def __init__(self, model_path):
        """
        Initialize the HazmNER object.

        Parameters:
            model_path (str): The path to the pre-trained NER model.
        """
        super().__init__(model_path)
        import spacy

        from spacy.tokens import Doc
        from spacy.tokens import DocBin
        from spacy.vocab import Vocab

        self.model_path = model_path
        self.model = self.load_model(model_path)

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

    
    def _save_spacy_data(self, data, save_path):
        """
        Save data in Spacy format.

        Parameters:
            data (list of tuple): Data to be saved in Spacy format.
            save_path (str): Path to save the Spacy data.
        """
        nlp = spacy.blank("fa")
        db = DocBin()
        for text, annotations in tqdm(data):
            doc = nlp(text)
            ents = []
            if annotations:
                for start, end, label in annotations:
                    span = doc.char_span(start, end, label=label)
                    ents.append(span)
            else:
                continue
            doc.ents = ents
            db.add(doc)
        db.to_disk(save_path)
    
    def _preprocess_data(self, data_path, save_path, sep, set_type='train'):
        """
        Preprocess data for training or evaluation.

        Parameters:
            data_path (str): Path to the data file.
            save_path (str): Path to save the preprocessed data.
            sep (str): Separator used in the data file.
            set_type (str): Type of data (train or val).

        Raises:
            AssertionError: If set_type is not 'train' or 'val'.
        """
        assert set_type in ['train', 'val']
        data = []
        spacy_data = []
        tokens, entities = prepare_conll_data_format(data_path, sep=sep, verbose=False)
        for i in range(len(tokens)):
            data.append(list(zip(tokens[i], entities[i])))
        
        for sample in data:
            spacy_data.append(convert_to_spacy_format(sample))

        self._save_spacy_data(spacy_data, save_path + set_type + ".spacy")

    
    def train_model(self, model_save_path, train_path, dev_path, data_save_path, sep):
        """
        Train the NER model.

        Parameters:
            model_save_path (str): Path to save the trained model.
            train_path (str): Path to the training data.
            dev_path (str): Path to the validation data.
            data_save_path (str): Path to save the preprocessed data.
            sep (str): Separator used in the data files.
        """
        self._preprocess_data(train_path, save_path=data_save_path, sep=sep)
        self._preprocess_data(dev_path, save_patdata_0h=data_save_path, sep=sep)
        subprocess.run(f"python -m spacy train config.cfg --output {model_save_path} --paths.train {train_path+'train.spacy'} --paths.dev {dev_path+'dev.spacy'}")
        self.model = self._load_model(model_save_path)
    
    def _load_model(self, model_path):
        """
        Load the trained NER model.

        Parameters:
            model_path (str): Path to the trained model.

        Returns:
            spacy.Language: Loaded NER model.
        """
        return spacy.load(model_path)
