# ruff: noqa: EXE002
"""این ماژول شامل کلاس‌ها و توابعی برای تجزیهٔ متن به عبارات اسمی، فعلی و حرف است."""

from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from nltk.chunk import RegexpParser
from nltk.chunk import conlltags2tree
from nltk.chunk import tree2conlltags
from nltk.chunk.util import ChunkScore

from hazm import IOBTagger
from hazm import POSTagger





def tree2brackets(tree: str) -> str:
    """خروجی درختی تابع [parse()][hazm.chunker.Chunker.parse] را به یک ساختار
    کروشه‌ای تبدیل می‌کند.

    Examples:
        >>> chunker = Chunker(model='chunker.model')
        >>> tree=chunker.parse([('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')])
        >>> print(tree)
        (S
          (NP نامه/NOUN,EZ ایشان/PRON)
          (POSTP را/ADP)
          (VP دریافت/NOUN داشتم/VERB)
          ./PUNCT)

        >>> tree2brackets(tree)
        '[نامه ایشان NP] [را POSTP] [دریافت داشتم VP] .'

    Args:
        tree: ساختار درختی حاصل از پردزاش تابع parse()

    Returns:
        رشته‌ای از کروشه‌ها که در هر کروشه جزئی از متن به همراه نوع آن جای گرفته است.

    """
    s, tag = "", ""
    for item in tree2conlltags(tree):
        if item[2][0] in {"B", "O"} and tag:
            s += tag + "] "
            tag = ""

        if item[2][0] == "B":
            tag = item[2].split("-")[1]
            s += "["
        s += item[0] + " "

    if tag:
        s += tag + "] "

    return s.strip()


class Chunker(IOBTagger):
    """این کلاس شامل توابعی برای تقطیع متن، آموزش و ارزیابی مدل است."""

    def __init__(
        self: "Chunker",
        model: Optional[str] = None,
        data_maker: Optional[List[List[Dict]]] = None,
    ) -> None:
        """constructor."""
        data_maker = self.data_maker if data_maker is None else data_maker
        self.posTagger = POSTagger()
        super().__init__(model, data_maker)

    def data_maker(
        self: "Chunker",
        tokens: List[List[Tuple[str, str]]],
    ) -> List[List[Dict]]:
        """تابعی که لیستی دو بعدی از کلمات به همراه لیبل را گرفته و لیست دو بعدی از از دیکشنری‌هایی که تعیین‌کننده ویژگی‌ها هر کلمه هستند را برمی‌گرداند.

        Examples:
            >>> chunker = Chunker(model = 'chunker.model')
            >>> chunker.data_maker(tokens = [[('من', 'PRON'), ('به', 'ADP'), ('مدرسه', 'NOUN,EZ'), ('ایران', 'NOUN'), ('رفته_بودم', 'VERB'), ('.', 'PUNCT')]])
            [[{'word': 'من', 'is_first': True, 'is_last': False, 'prefix-1': 'م', 'prefix-2': 'من', 'prefix-3': 'من', 'suffix-1': 'ن', 'suffix-2': 'من', 'suffix-3': 'من', 'prev_word': '', 'two_prev_word': '', 'next_word': 'به', 'two_next_word': 'مدرسه', 'is_numeric': False, 'prev_is_numeric': '', 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': '', 'next_is_punc': False, 'pos': 'PRON', 'prev_pos': '', 'next_pos': 'ADP'}, {'word': 'به', 'is_first': False, 'is_last': False, 'prefix-1': 'ب', 'prefix-2': 'به', 'prefix-3': 'به', 'suffix-1': 'ه', 'suffix-2': 'به', 'suffix-3': 'به', 'prev_word': 'من', 'two_prev_word': '.', 'next_word': 'مدرسه', 'two_next_word': 'ایران', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': False, 'pos': 'ADP', 'prev_pos': 'PRON', 'next_pos': 'NOUN,EZ'}, {'word': 'مدرسه', 'is_first': False, 'is_last': False, 'prefix-1': 'م', 'prefix-2': 'مد', 'prefix-3': 'مدر', 'suffix-1': 'ه', 'suffix-2': 'سه', 'suffix-3': 'رسه', 'prev_word': 'به', 'two_prev_word': 'من', 'next_word': 'ایران', 'two_next_word': 'رفته_بودم', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': False, 'pos': 'NOUN,EZ', 'prev_pos': 'ADP', 'next_pos': 'NOUN'}, {'word': 'ایران', 'is_first': False, 'is_last': False, 'prefix-1': 'ا', 'prefix-2': 'ای', 'prefix-3': 'ایر', 'suffix-1': 'ن', 'suffix-2': 'ان', 'suffix-3': 'ران', 'prev_word': 'مدرسه', 'two_prev_word': 'به', 'next_word': 'رفته_بودم', 'two_next_word': '.', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': False, 'pos': 'NOUN', 'prev_pos': 'NOUN,EZ', 'next_pos': 'VERB'}, {'word': 'رفته_بودم', 'is_first': False, 'is_last': False, 'prefix-1': 'ر', 'prefix-2': 'رف', 'prefix-3': 'رفت', 'suffix-1': 'م', 'suffix-2': 'دم', 'suffix-3': 'ودم', 'prev_word': 'ایران', 'two_prev_word': 'مدرسه', 'next_word': '.', 'two_next_word': '', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': False, 'is_punc': False, 'prev_is_punc': False, 'next_is_punc': True, 'pos': 'VERB', 'prev_pos': 'NOUN', 'next_pos': 'PUNCT'}, {'word': '.', 'is_first': False, 'is_last': True, 'prefix-1': '.', 'prefix-2': '.', 'prefix-3': '.', 'suffix-1': '.', 'suffix-2': '.', 'suffix-3': '.', 'prev_word': 'رفته_بودم', 'two_prev_word': 'ایران', 'next_word': '', 'two_next_word': '', 'is_numeric': False, 'prev_is_numeric': False, 'next_is_numeric': '', 'is_punc': True, 'prev_is_punc': False, 'next_is_punc': '', 'pos': 'PUNCT', 'prev_pos': 'VERB', 'next_pos': ''}]]

        Args:
            tokens: جملاتی که نیاز به تبدیل آن به برداری از ویژگی‌ها است.

        Returns:
            لیستی از لیستی از دیکشنری‌های بیان‌کننده ویژگی‌های یک کلمه.

        """
        words = [[word for word, _ in token] for token in tokens]
        tags = [[tag for _, tag in token] for token in tokens]
        return [
            [
                self.features(words=word_tokens, pos_tags=tag_tokens, index=index)
                for index in range(len(word_tokens))
            ]
            for word_tokens, tag_tokens in zip(words, tags)
        ]

    def features(
        self: "Chunker",
        words: List[str],
        pos_tags: List[str],
        index: int,
    ) -> Dict[str, Union[str, bool]]:
        """ویژگی‌های کلمه را برمی‌گرداند."""
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
        self: "Chunker",
        trees: List[str],
        c1: float = 0.4,
        c2: float = 0.04,
        max_iteration: int = 400,
        verbose: bool = True,
        file_name: str = "chunker_crf.model",
        report_duration: bool = True,
    ) -> None:
        """از روی درخت ورودی، مدل را آموزش می‌دهد.

        Args:
            trees: لیستی از درخت‌ها برای آموزش مدل.
            c1: مقدار L1 regularization.
            c2: مقدار L2 regularization.
            max_iteration: تعداد تکرار آموزش بر کل دیتا.
            verbose: نمایش اطلاعات مربوط به آموزش.
            file_name: نام و مسیر فایلی که می‌خواهید مدل در آن ذخیره شود.
            report_duration: نمایش گزارشات مربوط به زمان.

        """
        return super().train(
            [tree2conlltags(tree) for tree in trees],
            c1,
            c2,
            max_iteration,
            verbose,
            file_name,
            report_duration,
        )

    def parse(self: "Chunker", sentence: List[Tuple[str, str]]) -> str:
        """جمله‌ای را در قالب لیستی از تاپل‌های دوتایی [(توکن, نوع), (توکن, نوع), ...]
        دریافت می‌کند و درخت تقطع‌شدهٔ آن را بر می‌گرداند.

        Examples:
            >>> chunker = Chunker(model = 'chunker.model')
            >>> tree = chunker.parse(sentence = [('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')])
            >>> print(tree)
            (S
              (NP نامه/NOUN,EZ ایشان/PRON)
              (POSTP را/ADP)
              (VP دریافت/NOUN داشتم/VERB)
              ./PUNCT)

        Args:
            sentence: جمله‌ای که باید درخت تقطیع‌شدهٔ آن تولید شود.

        Returns:
            ساختار درختی حاصل از تقطیع.
            برای تبدیل این ساختار درختی به یک ساختار کروشه‌ای و قابل‌درک‌تر
            می‌توانید از تابع `tree2brackets()` استفاده کنید.

        """
        return conlltags2tree(super().tag(sentence))

    def parse_sents(
        self: "Chunker",
        sentences: List[List[Tuple[str, str]]],
    ) -> Iterator[str]:
        """جملات ورودی را به‌شکل تقطیع‌شده و در قالب یک برمی‌گرداند.

        Args:
            sentences: جملات ورودی.

        Yields:
            یک `Iterator` از جملات تقطیع شده.

        """
        for conlltagged in super().tag_sents(sentences):
            yield conlltags2tree(conlltagged)

    def evaluate(self: "Chunker", trees: List[str]) -> float:
        """داده صحیح دریافت شده را با استفاده از مدل لیبل می‌زند و دقت مدل را برمی‌گرداند.

        Examples:
            >>> chunker = Chunker(model = 'chunker.model')
            >>> trees = list(chunker.parse_sents([[('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')]]))
            >>> chunker.evaluate(trees)
            1.0

        Args:
            trees: لیست درختانی که با استفاده از آن مدل را ارزیابی می‌کنیم.

        Returns:
            دقت مدل

        """
        return super().evaluate([tree2conlltags(tree) for tree in trees])


class RuleBasedChunker(RegexpParser):
    """کلاس RuleBasedChunker.


    Examples:
    >>> chunker = RuleBasedChunker()
    >>> tree2brackets(chunker.parse([('نامه', 'Ne'), ('۱۰', 'NUMe'), ('فوریه', 'Ne'), ('شما', 'PRO'), ('را', 'POSTP'), ('دریافت', 'N'), ('داشتم', 'V'), ('.', 'PUNC')]))
    '[نامه ۱۰ فوریه شما NP] [را POSTP] [دریافت داشتم VP] .'

    """

    def __init__(self: "RuleBasedChunker") -> None:
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
    def __init__(
            self: "SpacyChunker",
            model_path=None,
            using_gpu=None,
            gpu_id=0
        ):
        import os
        import subprocess
        import spacy

        from spacy.tokens import Doc
        from spacy.tokens import DocBin
        from spacy.vocab import Vocab

        from sklearn.metrics import classification_report,f1_score,accuracy_score,precision_score,recall_score

        from tqdm import tqdm


        """
        Initialize the SpacyChunker with data and model paths.

        Args:
        - model_path: Path to a pre-trained spaCy model.
        - using_gpu: Flag indicating whether to use GPU for processing.
        - gpu_id: id of gpu core that you want to train or evaluate model on it

        This constructor initializes the SpacyChunker and performs the initial setup.
        """
        super().__init__()
        self.model_path = model_path
        self.using_gpu = using_gpu
        self.gpu_id = gpu_id
        self.model = None
        self._setup()

    # Edit : این تابع داخلی هست و بهتر هست با _ شروع شود

    def _setup(self: "SpacyChunker"):
        """
        Set up the configuration for the spaCy model, including GPU settings.

        This function initializes and configures the spaCy model and data for training and evaluation.
        It ensures that GPU usage is appropriately configured if specified.

        Args:
        - target_dataset_for_evaluation: The dataset type to use for evaluation, either 'dev' or 'test'.

        This setup function is a crucial part of preparing the SpacyChunker for training and evaluation.
        """
        self._setup_gpu()

    def _setup_gpu(self: "SpacyChunker"):
        """
        Check GPU availability and configure spaCy to use it if possible.

        This method checks whether a GPU is available and, if so, configures spaCy to utilize it for improved processing speed.
        The GPU availability is determined based on the 'using_gpu' flag.

        This check is performed during setup to make use of available GPU resources for enhanced performance.
        """
        print("------------------ GPU Setup Process Started ---------------------")
        if self.using_gpu:
            gpu_available = spacy.prefer_gpu(self.gpu_id)
            if gpu_available: 
                print("------------ GPU is available and ready for use -------------")
                spacy.require_gpu(self.gpu_id)
                self.gpu_availability = True
            else:
                print("------------ GPU is not available; spaCy will use CPU -------------")
                self.gpu_availability = False

    def _setup_model(self: "SpacyChunker",sents):
        """
        Load and configure the spaCy model for a specific dataset type.

        This function loads a pre-trained spaCy model and configures it for a specific dataset type ('train', 'dev', or 'test').

        Args:
        - sents : List[List[str]] contain each sentence tokens in a separate list.All lists are in one major list

        The model setup process is essential for training and evaluation on the chosen dataset type.
        """
        self.peykare_dict = {}
        self.model = spacy.load(self.model_path)
        self._setup_dictionary(sents)
        self.model.tokenizer = self._custom_tokenizer
    
    def _custom_tokenizer(self,text):
        """
        Custom tokenizer for spaCy.

        Args:
            - text: Input text to be tokenized.

        Returns:
            - Doc: SpaCy Doc object representing the tokenized text.
        """
        if text in self.peykare_dict:
            return Doc(self.model.vocab, self.peykare_dict[text])
        else:
            raise ValueError('No tokenization available for input.')
        
    def _setup_dictionary(self:"SpacyChunker",sents):
        """
        Set up a dictionary for custom tokenization.

        Args:
            - sents: List of sentences, each represented as a list of words.

        This dictionary is used for custom tokenization in the spaCy model.
        """
        for item in sents:
            self.peykare_dict[' '.join([w for w in item])] = [w for w in item]

    def _add_to_dict(self: "SpacyChunker", sents):
        """
            Add the sentences to dictianory if it doesnt exist already
        """
        for sent in sents:
            key = ' '.join(sent)
            if key not in self.peykare_dict:
                self.peykare_dict[key] = sent


    def _setup_dataset(self: "SpacyChunker",sents,saved_directory,dataset_type):
        """
        Set up spaCy DocBin dataset for training.

        Args:
            - sents: List of sentences, each represented as a list of (word, tag) tuples.
            - saved_directory: Directory to save the spaCy dataset.
            - dataset_type: Type of the dataset ('train', 'dev', or 'test').

        This function prepares the dataset in spaCy format and saves it to disk.
        """

        assert dataset_type in ['train','dev','test']
        db = DocBin()
        for sent in tqdm(sents):
            words = [word[0] for word in sent]
            tags = [word[2] for word in sent]
            doc = Doc(Vocab(strings=words), words = words)
            for d, tag in zip(doc, tags):
                d.tag_ = tag
            db.add(doc)
        db.to_disk(f'{saved_directory}/{dataset_type}.spacy')
        

    def train(
            self: "SpacyChunker",
            train_dataset,
            test_dataset,
            data_directory,
            base_config_file,
            train_config_path,
            output_dir,
            use_direct_config=False        
        ):
        """
        Train the spaCy chunker model.

        Args:
            - train_dataset: Training dataset, each sentence represented as a list of (word, tag) tuples.
            - test_dataset: Testing dataset, each sentence represented as a list of (word, tag) tuples.
            - data_directory: Directory to save the spaCy datasets.
            - base_config_file: Path to the base configuration file.
            - train_config_path: Path to the training configuration file.
            - output_dir: Directory to save the trained model.
            - use_direct_config: Boolean indicating whether to use a directly provided config file.

        This function trains the spaCy chunker model and sets up the model for prediction.
        """
        if use_direct_config == False:
            self._setup_train_config(
                base_config=base_config_file,
                train_config_path=train_config_path
            )
        else:
            self.train_config_file = train_config_path

        self.train_dataset = train_dataset
        self.test_dataset = test_dataset

        if self.train_dataset:
            # Set up the training dataset configuration
            self._setup_dataset(sents=self.train_dataset,saved_directory=data_directory, dataset_type='train')

        if self.test_dataset:
            self._setup_dataset(sents=self.test_dataset,saved_directory=data_directory,dataset_type='test')

        train_data = f'{data_directory}/train.spacy'
        test_data = f'{data_directory}/test.spacy'

        command = f"python -m spacy train {self.train_config_file} --output ./{output_dir} --paths.train ./{train_data} --paths.dev ./{test_data}"
        if self.gpu_availability:
            command += f" --gpu-id {self.gpu_id}"
        
        subprocess.run(command, shell=True)
        self.model_path = f"{output_dir}/model-last"
        self._setup_model([[w for w,_,_ in sent] for sent in test_dataset])



    def _setup_train_config(self:"SpacyChunker",base_config,train_config_path):
        """
        Create and configure the training configuration file for spaCy.

        Args:
            - base_config: Path to the base configuration file.
            - train_config_file_name: Name of the training configuration file for saving it.

        This method is called to generate the training configuration file used in the training process.
        """
        print("----------------- Setting up the training configuration file ----------------------")
        self.train_config_file = train_config_path  # Set the path for the training configuration file
        command = f"python -m spacy init fill-config {base_config} {train_config_path}"  # Generate the training configuration file
        subprocess.run(command, shell=True)
        print("----------------- Training configuration file created successfully ----------------------")
        print(f"----------------- Training Config file address is {train_config_path} --------------------")


    def evaluate(self:"SpacyChunker",test_sents):
        """
        Score the accuracy of the chunker against the gold standard.

        Args:
            - test_sents: List of sentences, each represented as a list of (word, tag) tuples.

        Returns:
            - ChunkScore: Object reflecting the performance of this chunk peraser.
        """
        predictions , golds = self._label_yielder(test_sents)
        chunkscore = ChunkScore()
        for pred, correct in zip(predictions, golds):
            chunkscore.score(correct, pred)

        print("Accuracy is:",chunkscore.accuracy())
        print("Precision is:",chunkscore.precision())
        print("F_Score is:",chunkscore.f_measure())
        print("Recall is:",chunkscore.recall())

        return chunkscore

    def _label_yielder(self: "SpacyChunker",sents):
        """
        sents: List(List(Tuple(str,str,str)))
        Yield gold and predicted trees for evaluation.

        This function prepares gold and predicted trees for evaluation by parsing the test data.
        
        Returns:
        - preds_tree: Predicted trees for evaluation.
        - golds_tree: Gold standard trees for evaluation.
        """
        golds = sents
        test_inp = [[(prev_tuple[0], prev_tuple[1]) for prev_tuple in inner_list] for inner_list in golds]
        parsed = self.parse_sents(test_inp)
        preds_tree = list(parsed)
        golds_tree = list(self._make_tree_generator(golds))
        return preds_tree, golds_tree
    
    def parse(self: "SpacyChunker", sentence: List[Tuple[str, str]]) -> str:
        """جمله‌ای را در قالب لیستی از تاپل‌های دوتایی [(توکن, نوع), (توکن, نوع), ...]
        دریافت می‌کند و درخت تقطع‌شدهٔ آن را بر می‌گرداند.

        Examples:
            >>> chunker = Chunker(model = 'chunker.model')
            >>> tree = chunker.parse(sentence = [('نامه', 'NOUN,EZ'), ('ایشان', 'PRON'), ('را', 'ADP'), ('دریافت', 'NOUN'), ('داشتم', 'VERB'), ('.', 'PUNCT')])
            >>> print(tree)
            (S
              (NP نامه/NOUN,EZ ایشان/PRON)
              (POSTP را/ADP)
              (VP دریافت/NOUN داشتم/VERB)
              ./PUNCT)

        Args:
            sentence: جمله‌ای که باید درخت تقطیع‌شدهٔ آن تولید شود.

        Returns:
            ساختار درختی حاصل از تقطیع.
            برای تبدیل این ساختار درختی به یک ساختار کروشه‌ای و قابل‌درک‌تر
            می‌توانید از تابع `tree2brackets()` استفاده کنید.

        """
        if self.model == None:
            self._setup_model([[w for w,_ in sentence]])

        self._add_to_dict([[w[0] for w in sentence]])

        doc = self.model(' '.join([w for w , _ in sentence]))
        words = [w for w , _ in sentence]
        tags = [tag for _ , tag in sentence]
        preds = [w.tag_ for w in doc]
        chunk = list(zip(words,tags,preds))
        return conlltags2tree(chunk)



    def parse_sents(self: "SpacyChunker", sentences: List[List[Tuple[str, str]]],batch_size=128) -> Iterator[str]:
        """
        Parse multiple sentences and extract predictions.

        This function takes a list of sentences and processes each one using the spaCy model,
        extracting predictions for words, tags, and their associated predicted tags.

        Args:
        - sentences: List of sentences, each represented as a list of word-tag tuples.
        - Batch size: number of batchces that model should process

        Returns:
        - Iterator of predictions for multiple sentences.
        """
        if self.model == None:
            self._setup_model([[w for w , _ in sentence] for sentence in sentences])
        self._add_to_dict([[w for w,_ in sentence] for sentence in sentences])

        docs = list(self.model.pipe((' '.join([w for w , _ in sent]) for sent in sentences), batch_size=batch_size))
        words = [[w for w,_, in sentence] for sentence in sentences]
        tags = [[tag for _, tag in sentence] for sentence in sentences]
        preds = [[w.tag_ for w in doc] for doc in docs]
        combined = [list(zip(word_list, tag_list, pred_list)) for word_list, tag_list, pred_list in zip(words, tags, preds)]
        test_preds = self._make_tree_generator(combined)
        return test_preds

    def _make_tree_generator(self: "SpacyChunker", sents):
        """
        Generate NLTK tree structures from CoNLL tags.

        This function creates NLTK tree structures from CoNLL-formatted chunk tags.
        It's used to prepare gold and predicted trees for evaluation.

        Args:
        - sents: List of sentences in CoNLL format (word, tag, chunk).

        Yields:
        - Generator of NLTK tree structures for each sentence.
        """
        for sent in sents:
            yield conlltags2tree(sent)