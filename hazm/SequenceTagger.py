# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای برچسب‌گذاری توکن‌هاست.

"""

from __future__ import unicode_literals
from pycrfsuite import Tagger, Trainer
import numpy as np
import time
import multiprocessing
import math
import warnings

punctuations_list = ['"', '#', '(', ')', '*', ',', '-', '.', '/', ':', '[', ']', '«', '»', '،',';','?','!']

class SequenceTagger():
    """این کلاس شامل توابعی برای برچسب‌گذاری توکن‌ها است. این کلاس در نقش یک
    wrapper برای کتابخانهٔ [Wapiti](https://wapiti.limsi.fr/) است.
    
    Args:
        patterns (List, optional): الگوهای لازم برای ساخت مدل.
        **options (Dict, optional): آرگومان‌های نامدارِ اختیاری.
    
    """

    def __init__(self, model=None, universal_tag=False):
        self.is_universal = universal_tag
        if model != None:
            self.load_model(model)
            
    
    def load_model(self, model):
        self.model = Tagger().open(model)

    def __is_punc(self, word):
        return word in punctuations_list
    
    def __universal_converter(self, tagged_list):
        return [tag.split(',')[0] for tag in tagged_list]

    def __features(self, sentence, index):
        return {
        'word': sentence[index],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 1,
        
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
        'is_punc': self.__is_punc(sentence[index]),
        'prev_is_punc':  '' if  index==0 else self.__is_punc(sentence[index-1]),
        'next_is_punc':  '' if index== len(sentence) -1 else self.__is_punc(sentence[index+1]),
    }


    def make_data(self, tagged_list):
        X, y = [], []
        tagged_list = np.array(tagged_list)
        words = tagged_list[:, 0]

        for tagged in tagged_list:
            X.append([self.__features(words, index) for index in range(len(tagged))])
            y.append([tag for _, tag in tagged])

        return X,y
        

    def train(self, tagged_list, algouritm='lbfgs', c1=0.4, c2=0.04, max_iteration=400, verbose=True, file_name='crf.model', data_maker=make_data, report_duration=True):
        """لیستی از جملات را می‌گیرد و بر اساس آن مدل را آموزش می‌دهد.
        
        هر جمله، لیستی از `(توکن، برچسب)`هاست.
        
        Examples:
            >>> tagger = SequenceTagger(patterns=['*', 'u:word-%x[0,0]'])
            >>> tagger.train([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
        
        Args:
            sentences (List[List[Tuple[str,str]]]): جملاتی که مدل از روی آن‌ها آموزش می‌بیند.
        
        """
        trainer = Trainer(verbose=verbose)
        trainer.set_params({
        'algourithm': algouritm,
        'c1': c1,
        'c2': c2,  
        'max_iterations': max_iteration,
        'feature.possible_transitions': True,
        })

        start_time = time.time()
        X, y = data_maker(tagged_list)

        for xseq, yseq in zip(X, y):
            trainer.append(xseq, yseq)

        end_time = time.time()
        data_preprocessing_time = end_time - start_time

        if(report_duration):
            print(f'preprocessing time: {data_preprocessing_time}')
        
        start_time = time.time()
        trainer.train(file_name)
        end_time = time.time()
        training_time = end_time - start_time

        if(report_duration):
            print(f'training time: {training_time}')
            print(f'the total time duration: {data_preprocessing_time + training_time}')
        
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
        self.model.save(filename)

    def tag(self, tokens, data_maker = make_data):
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
        return self.model.tag(data_maker(tokens)) if self.is_universal else self.__universal_converter(self.model.tag(data_maker(tokens)))
        # if(self.is_universal):
        #     return self.model.tag(data_maker(tokens))
        # else:
        #     return self.__universal_converter(self.model.tag(data_maker(tokens)))

    def __tag_sents(self, sentences, tagges, start_ind, end_ind):
        

            
        

    def tag_sents(self, sentences, workers = multiprocessing.cpu_count() - 1):
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
        workers = 1 if workers == 0 else workers
        sents_size = len(sentences)
        segments_size = math.ceil(sents_size / workers)

        i = 0
        while(i*segments_size<sents_size):
            start_ind = i * segments_size
            end_ind = (i + 1) * segments_size


            i += 1



        

        


class IOBTagger(SequenceTagger):
    """
    
    """

    def tag_sents(self, sentences):
        """
        
        Examples:
            >>> tagger = IOBTagger(patterns=['*', 'U:word-%x[0,0]', 'U:word-%x[0,1]'])
            >>> tagger.train([[('من', 'PRO', 'B-NP'), ('به', 'P', 'B-PP'), ('مدرسه', 'N', 'B-NP'), ('رفته_بودم', 'V', 'B-VP'), ('.', 'PUNC', 'O')]])
            >>> tagger.tag_sents([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
            [[('من', 'PRO', 'B-NP'), ('به', 'P', 'B-PP'), ('مدرسه', 'N', 'B-NP'), ('رفته_بودم', 'V', 'B-VP'), ('.', 'PUNC', 'O')]]
        
        """
        sentences = list(sentences)
        lines = "\n\n".join(
            [
                "\n".join(["\t".join(word) for word in sentence])
                for sentence in sentences
            ]
        ).replace(" ", "_")
        results = self.model.label_sequence(lines).decode("utf8")
        tags = iter(results.strip().split("\n"))
        return [[word + (next(tags),) for word in sentence] for sentence in sentences]

    def evaluate(self, gold):
        """
        
        Examples:
            >>> tagger = IOBTagger(patterns=['*', 'U:word-%x[0,0]', 'U:word-%x[0,1]'])
            >>> tagger.evaluate([[('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]])
        
        """
        tagged_sents = self.tag_sents(
            ([word[:-1] for word in sentence] for sentence in gold)
        )
        return accuracy(sum(gold, []), sum(tagged_sents, []))
