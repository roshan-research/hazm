# coding: utf8

from __future__ import unicode_literals
import os, codecs
from .Normalizer import Normalizer
from .WordTokenizer import WordTokenizer


def coarse_pos_e(tags):
    """
    Coarse POS tags of Peykare corpus:
        N: Noun, V: Verb, AJ: Adjective, ADV: Adverb, PRO: Pronoun, DET: Determiner, P: Preposition, POSTP: Postposition, NUM: Number, CONJ: Conjunction, PUNC: Punctuation, RES: Residual, CL: Classifier, INT: Interjection

    >>> coarse_pos_e(['N','COM','SING'])
    'N'
    """

    try:
        return list(
                set(tags) & {'N', 'V', 'AJ', 'ADV', 'PRO', 'DET', 'P', 'POSTP', 'NUM', 'CONJ', 'PUNC', 'CL', 'INT',
                             'RES'})[
                   0] + ('e' if 'EZ' in tags else '')
    except Exception:
        return 'N'


def join_verb_parts(sentence):
    """
    Join verb parts like Dadedgan corpus.

    >>> join_verb_parts([('اولین', 'AJ'), ('سیاره', 'Ne'), ('خارج', 'AJ'), ('از', 'P'), ('منظومه', 'Ne'), ('شمسی', 'AJ'), ('دیده', 'AJ'), ('شد', 'V'), ('.', 'PUNC')])
    [('اولین', 'AJ'), ('سیاره', 'Ne'), ('خارج', 'AJ'), ('از', 'P'), ('منظومه', 'Ne'), ('شمسی', 'AJ'), ('دیده_شد', 'V'), ('.', 'PUNC')]
    """

    if not hasattr(join_verb_parts, 'tokenizer'):
        join_verb_parts.tokenizer = WordTokenizer()
    before_verbs, after_verbs, verbe = join_verb_parts.tokenizer.before_verbs, join_verb_parts.tokenizer.after_verbs, join_verb_parts.tokenizer.verbe

    result = [('', '')]
    for word in reversed(sentence):
        if word[0] in before_verbs or (result[-1][0] in after_verbs and word[0] in verbe):
            result[-1] = (word[0] + '_' + result[-1][0], result[-1][1])
        else:
            result.append(word)
    return list(reversed(result[1:]))


class PeykareReader():
    """
    interfaces [Peykare Corpus](http://www.rcisp.com/?q=%D9%BE%DB%8C%DA%A9%D8%B1%D9%87%20%D9%85%D8%AA%D9%86%DB%8C%20%D8%B2%D8%A8%D8%A7%D9%86%20%D9%81%D8%A7%D8%B1%D8%B3%DB%8C)
    Bijankhan, M., Sheykhzadegan, J., Bahrani, M., & Ghayoomi, M. (2011). Lessons from building a Persian written corpus: Peykare. Language Resources and Evaluation, 45, 143–164.

    >>> peykare = PeykareReader(root='corpora/peykare')
    >>> next(peykare.sents())
    [('دیرزمانی', 'N'), ('از', 'P'), ('راه‌اندازی', 'Ne'), ('شبکه‌ی', 'Ne'), ('خبر', 'Ne'), ('الجزیره', 'N'), ('نمی‌گذرد', 'V'), ('،', 'PUNC'), ('اما', 'CONJ'), ('این', 'DET'), ('شبکه‌ی', 'Ne'), ('خبری', 'AJe'), ('عربی', 'N'), ('بسیار', 'ADV'), ('سریع', 'ADV'), ('توانسته', 'V'), ('در', 'P'), ('میان', 'Ne'), ('شبکه‌های', 'Ne'), ('عظیم', 'AJe'), ('خبری', 'AJ'), ('و', 'CONJ'), ('بنگاه‌های', 'Ne'), ('چندرسانه‌ای', 'AJe'), ('دنیا', 'N'), ('خودی', 'N'), ('نشان', 'N'), ('دهد', 'V'), ('.', 'PUNC')]
    >>> doc = next(peykare.docs())
    >>> next(peykare.doc_to_sentence(doc))
    [('دیرزمانی', 'N,COM,SING,TIME,YA'), ('از', 'P'), ('راه\u200cاندازی', 'N,COM,SING,EZ'), ('شبکه\u200cی', 'N,COM,SING,EZ'), ('خبر', 'N,COM,SING,EZ'), ('الجزیره', 'N,PR,SING'), ('نمی\u200cگذرد', 'V,PRES,NEG,3'), ('،', 'PUNC'), ('اما', 'CONJ'), ('این', 'DET,DEMO'), ('شبکه\u200cی', 'N,COM,SING,EZ'), ('خبری', 'AJ,SIM,EZ'), ('عربی', 'N,PR,SING'), ('بسیار', 'ADV,INTSF,SIM'), ('سریع', 'ADV,GENR,SIM'), ('توانسته', 'V,PASTP'), ('در', 'P'), ('میان', 'N,COM,SING,EZ'), ('شبکه\u200cهای', 'N,COM,PL,EZ'), ('عظیم', 'AJ,SIM,EZ'), ('خبری', 'AJ,SIM'), ('و', 'CONJ'), ('بنگاه\u200cهای', 'N,COM,PL,EZ'), ('چندرسانه\u200cای', 'AJ,SIM,EZ'), ('دنیا', 'N,COM,SING'), ('خودی', 'N,COM,SING,YA'), ('نشان', 'N,COM,SING'), ('دهد', 'V,SUB,POS,3'), ('.', 'PUNC')]
    >>> next(peykare.doc_to_sent(doc))
    [('دیرزمانی', 'N'), ('از', 'P'), ('راه\u200cاندازی', 'Ne'), ('شبکه\u200cی', 'Ne'), ('خبر', 'Ne'), ('الجزیره', 'N'), ('نمی\u200cگذرد', 'V'), ('،', 'PUNC'), ('اما', 'CONJ'), ('این', 'DET'), ('شبکه\u200cی', 'Ne'), ('خبری', 'AJe'), ('عربی', 'N'), ('بسیار', 'ADV'), ('سریع', 'ADV'), ('توانسته', 'V'), ('در', 'P'), ('میان', 'Ne'), ('شبکه\u200cهای', 'Ne'), ('عظیم', 'AJe'), ('خبری', 'AJ'), ('و', 'CONJ'), ('بنگاه\u200cهای', 'Ne'), ('چندرسانه\u200cای', 'AJe'), ('دنیا', 'N'), ('خودی', 'N'), ('نشان', 'N'), ('دهد', 'V'), ('.', 'PUNC')]
    """

    def __init__(self, root, joined_verb_parts=True, pos_map=coarse_pos_e, fine_grained_tags=False):
        self.fine_grained_tags = fine_grained_tags
        self._root = root
        self._pos_map = pos_map if pos_map else lambda tags: ','.join(tags)
        self._joined_verb_parts = joined_verb_parts
        self._normalizer = Normalizer(punctuation_spacing=False, affix_spacing=False)

    def docs(self):
        for root, dirs, files in os.walk(self._root):
            for name in sorted(files):
                with codecs.open(os.path.join(root, name), encoding='windows-1256') as peykare_file:
                    text = peykare_file.read()
                    if text:
                        yield text

    def doc_to_sentence(self, doc):
        sentence = []
        for line in doc.split('\r\n'):
            if not line:
                continue

            parts = line.split(' ')
            tags, word = parts[3], self._normalizer.normalize('‌'.join(parts[4:]))

            if word and word != '#':
                sentence.append((word, tags))

            if parts[2] == 'PUNC' and word in {'#', '.', '؟', '!'}:
                if len(sentence) > 1:
                    yield sentence
                sentence = []

    def doc_to_sent(self, doc):
        if not self.fine_grained_tags:
            map_pos = lambda item: (item[0], self._pos_map(item[1].split(',')))
            for sentence in self.doc_to_sentence(doc):
                if self._joined_verb_parts:
                    sentence = join_verb_parts(sentence)

                yield list(map(map_pos, sentence))
        else:
            yield from self.doc_to_sentence(doc)

    def _sentences(self):
        for doc in self.docs():
            for sent in self.doc_to_sentence(doc):
                yield sent

    def sents(self):
        if not self.fine_grained_tags:
            map_pos = lambda item: (item[0], self._pos_map(item[1].split(',')))
            for sentence in self._sentences():
                if self._joined_verb_parts:
                    sentence = join_verb_parts(sentence)
                yield list(map(map_pos, sentence))
        else:
            yield from self._sentences()