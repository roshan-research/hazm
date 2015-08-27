from __future__ import unicode_literals

from .utils import informal_verbs, informal_words
from .Normalizer import Normalizer
from .Lemmatizer import Lemmatizer
from .WordTokenizer import *
from .SentenceTokenizer import *


class InformalNormalizer(Normalizer):

    def __init__(self, verb_file=informal_verbs, word_file=informal_words, **args):
        super(InformalNormalizer, self).__init__(**args)
        lemmatizer = Lemmatizer()

        def informal_to_formal_conjucation(i, f, flag):
            iv = self.informal_conjugations(i)
            fv = lemmatizer.conjugations(f)
            res = {}
            if flag:
                for i, j in zip(iv, fv[48:]):
                    res[i] = j
                    if '‌' in i:
                        res[i.replace('‌', '')] = j
                        res[i.replace('‌', ' ')] = j
                    if i.endswith('ین'):
                        res[i[:-1] + 'د'] = j
            else:
                 for i, j in zip(iv[8:], fv[56:]):
                    res[i] = j
                    if '‌' in i:
                        res[i.replace('‌', '')] = j
                        res[i.replace('‌', ' ')] = j
                    if i.endswith('ین'):
                        res[i[:-1] + 'د'] = j
            
            for i,j in res.items():
                print(i,j) 
            return res

        with open(verb_file, 'r') as vf:
            self.iverb_map = {}
            for f, i, flag in map(lambda x: x.strip().split(' ', 2), vf):
                self.iverb_map.update(
                    informal_to_formal_conjucation(i, f, flag)
                )

        with open(word_file, 'r') as wf:
            self.iword_map = dict(
                map(lambda x: x.strip().split(' ', 1), wf)
            )

    def normalize(self, text):
        """
        >>> normalizer = InformalNormalizer()
        >>> normalizer.normalize('فردا می‌رم')
        'فردا می‌روم'
        """
        sent_tokenizer = SentenceTokenizer()
        word_tokenizer = WordTokenizer()
        text = super(InformalNormalizer, self).normalize(text)
        sents = [
            word_tokenizer.tokenize(sentence)
            for sentence in sent_tokenizer.tokenize(text)
        ]

        for i in range(len(sents)):
            for j in range(len(sents[i])):
                if sents[i][j] in self.iverb_map:
                    sents[i][j] = self.iverb_map[sents[i][j]]

                if sents[i][j] in self.iword_map:
                    sents[i][j] = self.iword_map[sents[i][j]]

        text = '\n'.join([' '.join(word) for word in sents])
        return super(InformalNormalizer, self).normalize(text)

    def informal_conjugations(self, verb):
        ends = ['م', 'ی', '', 'یم', 'ین', 'ن']
        present_simples = [verb + end for end in ends]
        if verb.endswith('ا'):
            present_simples[2] = verb + 'د'
        else:
            present_simples[2] = verb + 'ه'
        present_not_simples = ['ن' + item for item in present_simples]
        present_imperfects = ['می‌' + item for item in present_simples]
        present_not_imperfects = ['ن' + item for item in present_imperfects]
        present_subjunctives = [item if item.startswith('ب') else 'پ' + item for item in present_simples]
        present_not_subjunctives = ['ن' + item for item in present_simples]
        return present_simples + present_not_simples + \
            present_imperfects + present_not_imperfects + \
            present_subjunctives + present_not_subjunctives


class InformalLemmatizer(object):

    def __init__(self):
        self.lemm = Lemmatizer()

    def lemmatize(self, word):
        if (word.endswith('ه') and (word + 'د') in lemmatizer.verbs):
          return word + 'د'
        elif word.endswith('ه') and (word[:-1] + 'د') in lemmatizer.verbs:
          sent[i] = word[:-1] + 'د'
          vres[(word, sent[i])] += 1
        elif word.endswith('ن') and (word + 'د') in lemmatizer.verbs:
          sent[i] = word + 'د'
          vres[(word, sent[i])] += 1
        elif (word.endswith('ه') and (word[:-1] + 'ود') in lemmatizer.verbs):
          sent[i] = word[:-1] + 'ود'
          vres[(word, sent[i])] += 1

        else:
            word = word[::-1].replace('و', 'ا', 1)[::-1]
            if word in lemmatizer.verbs:
                sent[i] = word
                vres[(word, sent[i])] += 1
            elif (word.endswith('ه') and (word + 'د') in lemmatizer.verbs):
                sent[i] = word + 'د'
                vres[(word, sent[i])] += 1
            elif word.endswith('ه') and (word[:-1] + 'د') in lemmatizer.verbs:
                sent[i] = word[:-1] + 'د'
                vres[(word, sent[i])] += 1
            elif word.endswith('ن') and (word + 'د') in lemmatizer.verbs:
                sent[i] = word + 'د'
                vres[(word, sent[i])] += 1
            elif (word.endswith('ه') and (word[:-1] + 'ود') in lemmatizer.verbs):
                sent[i] = word[:-1] + 'ود'
                vres[(word, sent[i])] += 1
            else:
                if not word in inf.iword_map:
                    nres[word] += 1
                if not (word.startswith('و') or word.endswith('و')):
                    word = word[::-1].replace('و', 'ا', 1)[::-1]
                else:
                    word = word
            """
            if not lemmatizer.lemmatize(word, tag) in lemmatizer.words:
      if word in inf.iword_map:
        sent[i] = inf.iword_map[word]
        nres[(word, sent[i])] += 1
      elif word in lemmatizer.words:
        sent[i] = word
        nres[(word, sent[i])] += 1

    if word in self.iverbs:
            return self.iverbs[word]
        elif word in self.iwords:
            return self.iwords[word]
        if word.endswith('ی') and word[:-1].strip() in self.iwords:
            return self.iwords
        else:
            return self.lemm.lemmatize(word)
            """

