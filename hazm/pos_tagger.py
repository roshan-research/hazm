"""این ماژول شامل کلاس‌ها و توابعی برای برچسب‌گذاری توکن‌هاست."""

from nltk.tag import stanford  # noqa: I001
from hazm import SequenceTagger

import os
import subprocess


punctuation_list = [
    '"',
    "#",
    "(",
    ")",
    "*",
    ",",
    "-",
    ".",
    "/",
    ":",
    "[",
    "]",
    "«",
    "»",
    "،",
    ";",
    "?",
    "!",
]


class POSTagger(SequenceTagger):
    """این کلاس‌ها شامل توابعی برای برچسب‌گذاری توکن‌هاست."""

    def __init__(
        self: "POSTagger", model=None, data_maker=None, universal_tag=False,
    ) -> None:
        data_maker = self.data_maker if data_maker is None else data_maker
        self.__is_universal = universal_tag
        super().__init__(model, data_maker)

    def __universal_converter(self: "POSTagger", tagged_list):
        return [(word, tag.split(",")[0]) for word, tag in tagged_list]

    def __is_punc(self: "POSTagger", word):
        return word in punctuation_list

    def data_maker(self: "POSTagger", tokens):
        """تابعی که لیستی از لیستی از کلمات توکنایز شده را گرفته و لیست دو بعدی از از دیکشنری‌هایی که تعیین‌کننده ویژگی‌ها هر کلمه هستند را برمی‌گرداند.

        Examples:
            >>> posTagger = POSTagger(model = 'pos_tagger.model')
            >>> posTagger.data_maker(tokens = [['دلم', 'اینجا', 'مانده‌است', '.']])
            [[{'word': 'دلم', 'is_first': True, 'is_last': False, 'prefix-1': 'د', 'prefix-2': 'دل', 'prefix-3': 'دلم', 'suffix-1': 'م', 'suffix-2': 'لم', 'suffix-3': 'دلم', 'prev_word': '', 'two_prev_word': '', 'next_word': 'اینجا', 'two_next_word': 'مانده\u200cاست', 'is_numeric': False, 'prev_is_numeric': '', 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': '', 'next_is_punc': False}, {'word': 'اینجا', 'is_first': False, 'is_last': False, 'prefix-1': 'ا', 'prefix-2': 'ای', 'prefix-3': 'این', 'suffix-1': 'ا', 'suffix-2': 'جا', 'suffix-3': 'نجا', 'prev_word': 'دلم', 'two_prev_word': '.', 'next_word': 'مانده\u200cاست', 'two_next_word': '.', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': False}, {'word': 'مانده\u200cاست', 'is_first': False, 'is_last': False, 'prefix-1': 'م', 'prefix-2': 'ما', 'prefix-3': 'مان', 'suffix-1': 'ت', 'suffix-2': 'ست', 'suffix-3': 'است', 'prev_word': 'اینجا', 'two_prev_word': 'دلم', 'next_word': '.', 'two_next_word': '', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': True}, {'word': '.', 'is_first': False, 'is_last': True, 'prefix-1': '.', 'prefix-2': '.', 'prefix-3': '.', 'suffix-1': '.', 'suffix-2': '.', 'suffix-3': '.', 'prev_word': 'مانده\u200cاست', 'two_prev_word': 'اینجا', 'next_word': '', 'two_next_word': '', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': '', 'is_punc': True, 'prev_is_punc': False, 'next_is_punc': ''}]]

        Args:
            tokens (List[List[str]]): جملاتی که نیاز به تبدیل آن به برداری از ویژگی‌ها است.

        Returns:
            List(List(Dict())): لیستی از لیستی از دیکشنری‌های بیان‌کننده ویژگی‌های یک کلمه.
        """
        return [
            [self.features(token, index) for index in range(len(token))]
            for token in tokens
        ]

    def features(self: "POSTagger", sentence, index):
        """features."""
        return {
            "word": sentence[index],
            "is_first": index == 0,
            "is_last": index == len(sentence) - 1,
            # *ix
            "prefix-1": sentence[index][0],
            "prefix-2": sentence[index][:2],
            "prefix-3": sentence[index][:3],
            "suffix-1": sentence[index][-1],
            "suffix-2": sentence[index][-2:],
            "suffix-3": sentence[index][-3:],
            # word
            "prev_word": "" if index == 0 else sentence[index - 1],
            "two_prev_word": "" if index == 0 else sentence[index - 2],
            "next_word": "" if index == len(sentence) - 1 else sentence[index + 1],
            "two_next_word": (
                ""
                if index in {len(sentence) - 1, len(sentence) - 2}
                else sentence[index + 2]
            ),
            # digit
            "is_numeric": sentence[index].isdigit(),
            "prev_is_numeric": "" if index == 0 else sentence[index - 1].isdigit(),
            "next_is_numeric": (
                "" if index == len(sentence) - 1 else sentence[index + 1].isdigit()
            ),
            # punc
            "is_punc": self.__is_punc(sentence[index]),
            "prev_is_punc": "" if index == 0 else self.__is_punc(sentence[index - 1]),
            "next_is_punc": (
                ""
                if index == len(sentence) - 1
                else self.__is_punc(sentence[index + 1])
            ),
        }

    def tag(self: "POSTagger", tokens):
        """یک جمله را در قالب لیستی از توکن‌ها دریافت می‌کند و در خروجی لیستی از
        `(توکن، برچسب)`ها برمی‌گرداند.

        Examples:
            >>> posTagger = POSTagger(model = 'pos_tagger.model')
            >>> posTagger.tag(tokens = ['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.'])
            [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]

            >>> posTagger = POSTagger(model = 'pos_tagger.model', universal_tag = True)
            >>> posTagger.tag(tokens = ['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.'])
            [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]

        Args:
            tokens (List[str]): لیستی از توکن‌های یک جمله که باید برچسب‌گذاری شود.

        Returns:
            (List[Tuple[str,str]]): ‌لیستی از `(توکن، برچسب)`ها.

        """
        tagged_token = super().tag(tokens)
        return (
            self.__universal_converter(tagged_token)
            if self.__is_universal
            else tagged_token
        )

    def tag_sents(self: "POSTagger", sentences):
        """جملات را در قالب لیستی از توکن‌ها دریافت می‌کند
        و در خروجی، لیستی از لیستی از `(توکن، برچسب)`ها برمی‌گرداند.

        هر لیست از `(توکن، برچسب)`ها مربوط به یک جمله است.

        Examples:
            >>> posTagger = POSTagger(model = 'pos_tagger.model')
            >>> posTagger.tag_sents(sentences = [['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.']])
            [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]]

            >>> posTagger = POSTagger(model = 'pos_tagger.model', universal_tag = True)
            >>> posTagger.tag_sents(sentences = [['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.']])
            [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]]

        Args:
            sentences (List[List[str]]): لیستی از جملات که باید برچسب‌گذاری شود.

        Returns:
            (List[List[Tuple[str,str]]]): لیستی از لیستی از `(توکن، برچسب)`ها.
                    هر لیست از `(توکن،برچسب)`ها مربوط به یک جمله است.

        """
        tagged_sents = super().tag_sents(sentences)
        return (
            [self.__universal_converter(tagged_sent) for tagged_sent in tagged_sents]
            if self.__is_universal
            else tagged_sents
        )


class StanfordPOSTagger(stanford.StanfordPOSTagger):
    """StanfordPOSTagger."""

    def __init__(
        self: "StanfordPOSTagger",
        model_filename: "str",
        path_to_jar: str,
        *args, # noqa: ANN002
        **kwargs, # noqa: ANN003
    ) -> None:
        self._SEPARATOR = "/"
        super(stanford.StanfordPOSTagger, self).__init__(
            model_filename=model_filename,
            path_to_jar=path_to_jar,
            *args,  # noqa: B026
            **kwargs,
        )

    def tag(self: "StanfordPOSTagger", tokens):
        """tag.

        Examples:
            >>> tagger = StanfordPOSTagger(model_filename='persian.tagger', path_to_jar='stanford_postagger.jar')
            >>> tagger.tag(['من', 'به', 'مدرسه', 'رفته_بودم', '.'])
            [('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]

        """
        return self.tag_sents([tokens])[0]

    def tag_sents(self: "StanfordPOSTagger", sentences):
        """tag_sents."""
        refined = ([w.replace(" ", "_") for w in s] for s in sentences)
        return super(stanford.StanfordPOSTagger, self).tag_sents(refined)


class SpacyPOSTagger(POSTagger):
    def __init__(
        self: "SpacyPOSTagger",
        model_path=None,
        using_gpu=False,
        gpu_id=0
    ):
        
        import spacy  # noqa: I001

        from spacy.tokens import Doc
        from spacy.tokens import DocBin
        from spacy.vocab import Vocab

        from sklearn.metrics import classification_report,f1_score,accuracy_score,precision_score,recall_score

        from tqdm import tqdm
        """
        Initialize the SpacyPOSTagger with a model and data paths.

        Args:
        - model_path: Path to a pre-trained spaCy model.
        - test_dataset: Test dataset for evaluation. It has a similar structure to the training dataset.
        - test_directory: Directory to save the test data in spaCy format.
        - using_gpu: Set to True if you want use gpu (if you dont have one and set this to True the function use cpu automatically)
        This constructor calls the constructor of the parent class POSTagger.
        """
        super().__init__(universal_tag=True)
        self.model_path = model_path #### Usually an output directory for spacy model contain two other directory name model-last , model-best,You should give model_path like this : output/model-last
        self.using_gpu = using_gpu
        self.gpu_id = gpu_id
        self.tagger = None
        self._setup()

    def _setup(self: "SpacyPOSTagger"):
        """
        Set up the configuration for the spaCy model, including GPU settings and data preparation.

        This function initializes and configures the spaCy model, checks for GPU availability, and prepares the training and testing datasets in spaCy format.

        If using GPU, GPU settings are configured to enhance processing speed. Then, the pre-trained spaCy model is loaded based on the provided model path.
        
        Training and testing datasets are prepared and saved in the respective directories for use during model training and evaluation.
        """  # noqa: D212
        if self.using_gpu:
            self._setup_gpu()
        else:
            print("------------- You Prefer to use CPU --------------")
        

    def _setup_model(self: "SpacyPOSTagger",sents):
        """
        Initialize and configure the spaCy model for tagging without GPU settings.

        This method loads and configures the spaCy model based on the provided model path. It also sets up a custom tokenizer for text processing and constructs a dictionary for reference.

        Args:
            - model_path: Path to the pre-trained spaCy model.

        This method is typically called during setup to prepare the model for tagging tasks.
        """
        self.peykare_dict = {}  # Initialize a dictionary for reference
        self.tagger = spacy.load(self.model_path)  # Load the spaCy model
        self._set_peykare_dictionary(sents)  # Construct a reference dictionary
        self.tagger.tokenizer = self._custom_tokenizer  # Set a custom tokenizer for the model.

    def _setup_gpu(self: "SpacyPOSTagger"):
        """
        Check GPU availability and configure spaCy to use it if possible.

        This method checks whether a GPU is available and, if so, configures spaCy to utilize it for improved processing speed. It sets the 'gpu_availability' attribute to 'True' or 'False' accordingly.

        This check is performed during setup to make use of available GPU resources for enhanced performance.
        """
        print("------------------ GPU Setup Process Started ---------------------")
        gpu_available = spacy.prefer_gpu(gpu_id=self.gpu_id)  # Check if a GPU is available
        if gpu_available:
            print("------------ GPU is available and ready for use -------------")
            spacy.require_gpu(gpu_id=self.gpu_id)  # Configure spaCy to use the GPU
            self.gpu_availability = True
        else:
            print("------------ GPU is not available; spaCy will use CPU -------------")
            self.gpu_availability = False


    def _setup_dataset(self: "SpacyPOSTagger", dataset,saved_directory,data_type='train'):
        """
        Setup the training dataset in spaCy's binary format.

        This function prepares the training dataset and saves it in spaCy's binary format.
        """
        assert data_type in ['train','test']
        db = DocBin()
        for sent in tqdm(dataset):
            words = [word[0] for word in sent]
            tags = [word[1] for word in sent]
            doc = Doc(Vocab(strings=words), words=words)
            for d, tag in zip(doc, tags):
                d.tag_ = tag
            db.add(doc)

        self._handle_data_path(saved_directory)
        db.to_disk(f'{saved_directory}/{data_type}.spacy')

    def _handle_data_path(self,path='POSTaggerDataset'):
        """
        Create the directory if it doesn't exist.

        This method checks if the specified directory exists, and if not, it creates the directory to store the data.

        Args:
            - path: The path to the directory (default is 'POSTaggerDataset').

        This method is called to ensure the directory is available for saving processed data.
        """
        if not os.path.exists(path):
            os.makedirs(path)


    def _custom_tokenizer(self: "SpacyPOSTagger", text):
        """
        Implement a custom tokenization method for spaCy.

        This method defines a custom tokenization method for spaCy. It is used to tokenize input text based on a custom dictionary, or it raises an error if tokenization is not available.

        Args:
            - text: The input text to be tokenized.

        This custom tokenization method is used by the spaCy model during processing.

        """

        if text in self.peykare_dict:
            return Doc(self.tagger.vocab, self.peykare_dict[text])
        else:
            raise ValueError('No tokenization available for input.')

    def _set_peykare_dictionary(self: "SpacyPOSTagger", sents):
        """
        Create a dictionary for custom tokenization.

        This method constructs a dictionary to store custom tokenization mappings based on input sentences. It is used for custom tokenization in spaCy.

        Args:
            - sents: Input sentences to build the custom tokenization dictionary.

        This method is called during setup to establish a dictionary for tokenization.
        """
        self.peykare_dict = {' '.join([w for w in item]): [w for w in item] for item in sents}


    def _add_to_dict(self: "SpacyPOSTagger", sents):
        """
            Add the sentences to dictianory if it doesnt exist already
        """
        for sent in sents:
            key = ' '.join(sent)
            if key not in self.peykare_dict:
                self.peykare_dict[key] = sent


    def tag(self: "SpacyPOSTagger", tokens,universal_tag=True):
        """یک جمله را در قالب لیستی از توکن‌ها دریافت می‌کند و در خروجی لیستی از
        `(توکن، برچسب)`ها برمی‌گرداند.

        Examples:
            >>> posTagger = POSTagger(model = 'pos_tagger.model')
            >>> posTagger.tag(tokens = ['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.'])
            [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]

            >>> posTagger = POSTagger(model = 'pos_tagger.model', universal_tag = True)
            >>> posTagger.tag(tokens = ['من', 'به', 'مدرسه', 'ایران', 'رفته_بودم', '.'])
            [('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]

        Args:
            tokens (List[str]): لیستی از توکن‌های یک جمله که باید برچسب‌گذاری شود.

        Returns:
            (List[Tuple[str,str]]): ‌لیستی از `(توکن، برچسب)`ها.

        """
        if self.tagger == None:
            self._setup_model([tokens])
        self._add_to_dict([tokens])

        doc = self.tagger([' '.join([tok for tok in tokens])])
        if not universal_tag:
            tags = [tok.tag_ for tok in doc]
        else:
            tags = [tok.tag_.replace(',EZ','') for tok in doc]

        return list(zip(tokens,tags))
              # noqa: W293
    def tag_sents(self:"SpacyPOSTagger",sents,universal_tag=True,batch_size=128):
        """
            Args:
                sents : List[List[Tokens]]
                batch_size : number of batches give to model for processing sentences each time
        """
        """
            Returns : List[List[Tuple(str,str)]]
        """
        if self.tagger == None:
            self._setup_model(sents)

        self._add_to_dict(sents)
        
        docs = list(self.tagger.pipe((' '.join([w for w in sent]) for sent in sents), batch_size=batch_size))
        if not universal_tag:
            tags = [[w.tag_ for w in doc] for doc in docs]
        else:
            tags = [[w.tag_.replace(',EZ','') for w in doc] for doc in docs]
        
        combined_out = [list(zip(tok,tag)) for tok,tag in zip(sents,tags)]
        return combined_out

    def train(
        self: "SpacyPOSTagger",
        train_dataset,
        test_dataset,
        data_directory,
        base_config_file,
        train_config_path,
        output_dir,
        use_direct_config=False
    ):
        """
        Train the spaCy model using a subprocess and a configuration file.

        This method executes the training process for the spaCy model by invoking spaCy's training module using subprocess. It takes input configuration files, training and testing data, and GPU settings (if available).

        Args:
            - train_dataset: Training dataset for the tagger. It is a list of sentences, where each sentence is a list of token-tag pairs.
            - test_dataset: Testing dataset for the tagger. It is a list of sentences, where each sentence is a list of token-tag pairs.
            - data_directory: Directory to save the training and testing data in spaCy format.
            - base_config_file: Path to the base configuration file for spaCy.
            - train_config_path: if use_direct_config set to True this is the path of config file for training that you will use
              if use_direct_config set to False this is the path that you want train config file will create with base_config
            - output_dir: Directory for storing the trained model and training logs.

        Upon successful training, this method updates the model path to the trained model.

        This method is typically called to initiate the training process of the spaCy model.
        """

        self.spacy_train_directory = data_directory
        self.train_dataset = train_dataset ### List[List[Tuple]]
        self.test_dataset = test_dataset
        if self.train_dataset:
            # Set up the training dataset configuration
            self._setup_dataset(dataset=self.train_dataset, saved_directory=self.spacy_train_directory, data_type='train')

        if self.test_dataset:
            self._setup_dataset(test_dataset,saved_directory=data_directory,data_type='test')

        train_data = f'{data_directory}/train.spacy'
        test_data = f'{data_directory}/test.spacy'

        if use_direct_config == False:
            self._setup_train_config(base_config_file, train_config_path=train_config_path)
        else:
            self.train_config_file = train_config_path

        command = f"python -m spacy train {self.train_config_file} --output ./{output_dir} --paths.train ./{train_data} --paths.dev ./{test_data}"
        if self.gpu_availability:
            command += f" --gpu-id {self.gpu_id}"

        subprocess.run(command, shell=True)
        self.model_path = f"{output_dir}/model-last"
        self._setup_model([[w for w,_ in sent] for sent in test_dataset])

    def _setup_train_config(self: "SpacyPOSTagger", base_config, train_config_path):
        """
        Create and configure the training configuration file for spaCy.

        This method sets up the training configuration file by copying a base configuration file and customizing it according to the specified parameters.

        Args:
            - base_config: Path to the base configuration file.
            - train_config_file_name: Name of the training configuration file for saving it.

        This method is called to generate the training configuration file used in the training process.
        """
        self.train_config_file = train_config_path
        print("----------------- Setting up the training configuration file ----------------------")
        command = f"python -m spacy init fill-config {base_config} {train_config_path}"  # Generate the training configuration file
        subprocess.run(command, shell=True)
        print("----------------- Training configuration file created successfully ----------------------")
        print(f"----------------- Training Config file address is {train_config_path} --------------------")

    def evaluate(self: "SpacyPOSTagger", test_sents,batch_size):
        """
        Evaluate the spaCy model on input sentences using different tag options.

        This method evaluates the spaCy model on input sentences with and without 'EZ' tags and reports classification metrics.

        Args:
            - sents: List of sentences for evaluation.
            - batch_size : number of batches that model should process each time
        This method calls the internal evaluation method for both tag options.

        This method is typically used for model evaluation and reporting metrics.
        """
        self._setup_model([[w for w,_ in sent] for sent in test_sents])
        if self.tagger:
            golds, predictions = self._get_labels_and_predictions(test_sents,batch_size)        
            print("-----------------------------------------")
            self._evaluate_tags(test_sents, golds, predictions, use_ez_tags=True,batch_size=batch_size)
            print("-----------------------------------------")
            self._evaluate_tags(test_sents, golds, predictions, use_ez_tags=False,batch_size=batch_size)
        else:
            raise ValueError("Model does not exist.Please train a new one with train method of this instance or give a model_path , setup the model with self._setup_model() and then call evaluate")

    def _evaluate_tags(self, sents, golds=None, predictions=None, use_ez_tags=True,batch_size=128):
        """
        Evaluate model predictions and report classification metrics.

        This method evaluates model predictions and reports classification metrics for the specified tag option.

        Args:
            - sents: List of sentences for evaluation.
            - golds: List of gold labels (optional).
            - predictions: List of model predictions (optional).
            - use_ez_tags: A flag indicating whether to consider 'EZ' tags.
            - batch_size : number of batches model should process

        If `golds` and `predictions` are not provided, they are automatically extracted from the input sentences.

        This method calculates and displays precision, recall, and F1-score for the specified tag option.

        This method is called by the `evaluate` method to perform model evaluation.
        """
        if golds is None or predictions is None:
            golds, predictions = self._get_labels_and_predictions(sents,batch_size)

        predictions_cleaned = []
        golds_cleaned = []
        if use_ez_tags:
            get_tag_func = self._get_ez_tags
        else:
            get_tag_func = self._remove_ez_tags

        for preds, golds in zip(predictions, golds):
            for pred in preds:
                pred_cleaned = get_tag_func(pred)
                predictions_cleaned.append(pred_cleaned)
            for gold in golds:
                gold_cleaned = get_tag_func(gold)
                golds_cleaned.append(gold_cleaned)
        
        print(classification_report(golds_cleaned, predictions_cleaned))
        print('Precision: %.5f' % precision_score(golds_cleaned, predictions_cleaned, average='weighted'))
        print('Recall: %.5f' % recall_score(golds_cleaned, predictions_cleaned, average='weighted'))
        print('F1-Score: %.5f' % f1_score(golds_cleaned, predictions_cleaned, average='macro'))

    def _get_ez_tags(self, label):
        """
        Extract 'EZ' tags from labels.

        This method extracts 'EZ' tags from labels if they are present and returns them.

        Args:
            - label: The label containing 'EZ' tags.

        Returns:
            The 'EZ' tags or '-' if 'EZ' tags are not present.
        """
        if 'EZ' in label:
            label = 'EZ'
        else:
            label = '-'

        return label

    def _remove_ez_tags(self, label):
        """
        Remove 'EZ' tags from labels.

        This method removes 'EZ' tags from labels if they are present and returns the cleaned label.

        Args:
            - label: The label containing 'EZ' tags.

        Returns:
            The label with 'EZ' tags removed.
        """
        return label.replace(',EZ', '') if 'EZ' in label else label

    def _evaluate_ez_tags(self, sents):
        """
        Evaluate model predictions with 'EZ' tags included.

        This method evaluates model predictions with 'EZ' tags included.
        """
        self._evaluate_tags(sents, use_ez_tags=True)

    def _evaluate_normal_tags(self, sents):
        """
        Evaluate model predictions without 'EZ' tags.

        This method evaluates model predictions without 'EZ' tags.
        """
        self._evaluate_tags(sents, use_ez_tags=False)

    def _get_labels_and_predictions(self: "SpacyPOSTagger", sents,batch_size):
        """
        Extract gold labels and model predictions for evaluation.

        This method extracts gold labels and model predictions from input sentences.

        Args:
            - sents: List of sentences for evaluation.

        Returns:
            Lists of gold labels and model predictions.

        This method is typically used for gathering data to perform model evaluation.
        """
        gold_labels = [[tag for _, tag in sent] for sent in sents]
        tokens = [[w for w,_ in sent] for sent in sents]
        prediction_labels = self.tag_sents(tokens,batch_size)
        return gold_labels, prediction_labels
