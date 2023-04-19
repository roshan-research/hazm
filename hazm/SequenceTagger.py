"""این ماژول شامل کلاس‌ها و توابعی برای برچسب‌گذاری توکن‌هاست.

"""

from __future__ import unicode_literals
from pycrfsuite import Tagger, Trainer
import numpy as np
import time
import multiprocessing
import math
import warnings

punctuation_list = ['"', '#', '(', ')', '*', ',', '-', '.', '/', ':', '[', ']', '«', '»', '،',';','?','!']

def is_punc(word):
    return word in punctuation_list

def features(sentence, index):
    return {
    'word': sentence[index],
    'is_first': index == 0,
    'is_last': index == len(sentence) - 1,
    #*ix
    'prefix-1': sentence[index][0],
    'prefix-2': sentence[index][:2],
    'prefix-3': sentence[index][:3],
    'suffix-1': sentence[index][-1],
    'suffix-2': sentence[index][-2:],
    'suffix-3': sentence[index][-3:],
    #word
    'prev_word': '' if index == 0 else sentence[index - 1],
    'two_prev_word':'' if index == 0 else sentence[index - 2],
    'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
    'two_next_word': '' if (index == len(sentence) - 1 or index == len(sentence) - 2) else sentence[index + 2],
    #digit
    'is_numeric': sentence[index].isdigit(),
    'prev_is_numeric': '' if index == 0 else sentence[index - 1].isdigit(),
    'next_is_numeric': '' if index == len(sentence) - 1 else sentence[index + 1].isdigit(),
    #punc
    'is_punc': is_punc(sentence[index]),
    'prev_is_punc':  '' if  index==0 else is_punc(sentence[index-1]),
    'next_is_punc':  '' if index== len(sentence) -1 else is_punc(sentence[index+1]),
}

def features_IOB(words, pos_taggs, index):
    word_features = features(words, index)
    word_features.update({
        'pos': pos_taggs[index],
        'prev_pos': '' if index == 0 else pos_taggs[index - 1],
        'next_pos': '' if index == len(pos_taggs) - 1 else pos_taggs[index + 1]
    })
    return word_features
    
def prepare_data(tokens):
    return [[features(token, index) for index in range(len(token))] for token in tokens]

def prepare_data_IOB(tokens):
    words = [[word for word, _ in token] for token in tokens]
    tags = [[tag for _, tag in token] for token in tokens]
    return [[features_IOB(word_tokens, tag_tokens, index) for index in range(len(word_tokens))] for word_tokens, tag_tokens in zip(words, tags)]

# .update(add_pos_to_features(tag_tokens, index))
class SequenceTagger():
    """این کلاس شامل توابعی برای برچسب‌گذاری توکن‌ها است. این کلاس در نقش یک
    wrapper برای کتابخانهٔ [Wapiti](https://wapiti.limsi.fr/) است.
    
    Args:
        patterns (List, optional): الگوهای لازم برای ساخت مدل.
        **options (Dict, optional): آرگومان‌های نامدارِ اختیاری.
    
    """

    def __init__(self, model=None, universal_tag=False):
        self.__is_universal = universal_tag
        if model != None:
            self.load_model(model)
            
    def load_model(self, model):
        tagger = Tagger()
        tagger.open(model)
        self.model = tagger
    
    def __universal_converter(self, tagged_list):
        return [tag.split(',')[0] for tag in tagged_list]
    
    def __tag(self, tokens):
        return self.__universal_converter(self.model.tag(self.__data_provider([tokens])[0])) if self.__is_universal else self.model.tag(self.__data_provider([tokens])[0]) 

    def __train(self, X, y, args, verbose, file_name, report_duration):
        trainer = Trainer(verbose=verbose)
        trainer.set_params(args)
        
        start_time = time.time()
        for xseq, yseq in zip(X, y):
            trainer.append(xseq, yseq)

        end_time = time.time()
        data_preprocessing_time = end_time - start_time

        if(report_duration):
            print(f'preprocessing time: {data_preprocessing_time}')
        
        start_time = time.time()
        trainer.train(file_name)
        end_time = time.time()

        if(report_duration):
            print(f'training time: {end_time - start_time}')
            
        self.load_model(file_name)
        
    def train(self, tagged_list, c1=0.4, c2=0.04, max_iteration=400, verbose=True, file_name='crf.model', data_maker=prepare_data, report_duration=True):
        """لیستی از جملات را می‌گیرد و بر اساس آن مدل را آموزش می‌دهد.
        
        هر جمله، لیستی از `(توکن، برچسب)`هاست.
        
        Examples:
            >>> tagger = SequenceTagger(patterns=['*', 'u:word-%x[0,0]'])
            >>> tagger.train([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
        
        Args:
            sentences (List[List[Tuple[str,str]]]): جملاتی که مدل از روی آن‌ها آموزش می‌بیند.
        
        """
        
        X = data_maker([[word for word, _ in tagged_sent] for tagged_sent in tagged_list])
        y = [[tag for _, tag in tagged_sent] for tagged_sent in tagged_list]
        
        args = {
        'c1': c1,
        'c2': c2,  
        'max_iterations': max_iteration,
        'feature.possible_transitions': True,
        }

        return self.__train(X, y, args, verbose, file_name, report_duration)
        
    def save_model(self, filename):
        """مدل تهیه‌شده توسط تابع [train()][hazm.SequenceTagger.SequenceTagger.train]
        را ذخیره می‌کند.
        
        Examples:
            >>> tagger = SequenceTagger(patterns=['*', 'u:word-%x[0,0]'])
            >>> tagger.train([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
            >>> tagger.save_model('resources/test.model')
        
        Args:
            filename (str): نام و مسیر فایلی که می‌خواهید مدل در آن ذخیره شود.
        
        """
        self.model.dump(filename)

    def tag(self, tokens, data_provider = prepare_data):
        """یک جمله را در قالب لیستی از توکن‌ها دریافت می‌کند و در خروجی لیستی از
        `(توکن، برچسب)`ها برمی‌گرداند.
        
        Examples:
            >>> tagger = SequenceTagger(patterns=['*', 'u:word-%x[0,0]'])
            >>> tagger.tag(['من', 'به', 'مدرسه', 'رفته_بودم', '.'])
            [('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]
        
        Args:
            tokens (List[str]): لیستی از توکن‌های یک جمله که باید برچسب‌گذاری شود.
        
        Returns:
            (List[Tuple[str,str]]): ‌لیستی از `(توکن، برچسب)`ها.
        
        """
        self.__data_provider = data_provider
        return self.__tag(tokens)

    def tag_sents(self, sentences, data_provider = prepare_data):
        """جملات را در قالب لیستی از توکن‌ها دریافت می‌کند
        و در خروجی، لیستی از لیستی از `(توکن، برچسب)`ها برمی‌گرداند.
        
        هر لیست از `(توکن، برچسب)`ها مربوط به یک جمله است.
        
        Examples:
            >>> tagger = SequenceTagger(patterns=['*', 'u:word-%x[0,0]'])
            >>> tagger.tag_sents([['من', 'به', 'مدرسه', 'رفته_بودم', '.']])
            [[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]]
        
        Args:
            sentences (List[List[str]]): لیستی از جملات که باید برچسب‌گذاری شود.
        
        Returns:
            (List[List[Tuple[str,str]]]): لیستی از لیستی از `(توکن، برچسب)`ها.
                    هر لیست از `(توکن،برچسب)`ها مربوط به یک جمله است.
        
        """
        self.__data_provider = data_provider
        return [self.__tag(tokens) for tokens in sentences]



class IOBTagger(SequenceTagger):
    """
    
    """
    def __chunker_format(self, tagged_data, chunks):
        return [(token[0], token[1], chunk_tag) for token, chunk_tag in zip(tagged_data, chunks)]

    def tag(self, tagged_data, data_provider = prepare_data_IOB):
        chunk_tags = super().tag(tagged_data, data_provider)
        return self.__chunker_format(tagged_data, chunk_tags)
    
    def train(self, tagged_list, c1=0.4, c2=0.04, max_iteration=400, verbose=True, file_name='crf.model', data_maker=prepare_data, report_duration=True):
        return super().train(tagged_list, c1, c2, max_iteration, verbose, file_name, data_maker, report_duration)

    def tag_sents(self, sentences, data_provider = prepare_data_IOB):
        """
        
        Examples:
            >>> tagger = IOBTagger(patterns=['*', 'U:word-%x[0,0]', 'U:word-%x[0,1]'])
            >>> tagger.train([[('من', 'PRO', 'B-NP'), ('به', 'P', 'B-PP'), ('مدرسه', 'N', 'B-NP'), ('رفته_بودم', 'V', 'B-VP'), ('.', 'PUNC', 'O')]])
            >>> tagger.tag_sents([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
            [[('من', 'PRO', 'B-NP'), ('به', 'P', 'B-PP'), ('مدرسه', 'N', 'B-NP'), ('رفته_بودم', 'V', 'B-VP'), ('.', 'PUNC', 'O')]]
        
        """
        chunk_tags = super().tag_sents(sentences, data_provider)
        return [self.__chunker_format(tagged_data, chunks) for tagged_data, chunks in zip(sentences, chunk_tags)]
