import subprocess

from typing import Tuple , List
from tqdm import tqdm


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

    def predict_entities(self,sentences):
        raise NotImplementedError
    
    def evaluate_model(self):
        raise NotImplementedError

    def load_data(self):
        raise NotImplementedError
    
    def preprocess_data(self):
        raise NotImplementedError
    
    def train_model(self):
        raise NotImplementedError
    
    def save_model(self):
        raise NotImplementedError
    
    def load_model(self):
        raise NotImplementedError


class HazmNER(BaseNER):
    def __init__(self, model_path):
        super().__init__(model_path)
        import spacy


        self.model_path = model_path
        self.model = spacy.load(self.model_path)

    def predict_entities(self,sentences):
        results = []
        for sentence in sentences:
            doc = self.model(sentence)        
            entities = [(ent.text, ent.label_) for ent in doc.ents]        
            results.append(entities)
        return results

    def evaluate_model(self,dataset_path):
        subprocess.run(f"python -m spacy evaluate {self.model_path} {dataset_path}")

    def load_data(self):
        raise NotImplementedError
    
    def preprocess_data(self):
        raise NotImplementedError
    
    def train_model(self):
        raise NotImplementedError
    
    def save_model(self):
        raise NotImplementedError
    
    def load_model(self):
        raise NotImplementedError

def prepare_conll_data_format(
    path: str,
    sep: str = "\t",
    lower: bool = True,
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
                    # Optionally convert token to lowercase
                    if lower:
                        token = token.lower()
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
