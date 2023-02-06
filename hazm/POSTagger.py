# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای برچسب‌گذاری توکن‌هاست. **میزان دقت برچسب‌زنی در نسخهٔ حاضر ۹۷.۱ درصد [^1] است.**
[^1]: 
	این عدد با انتشار هر نسخه بروزرسانی می‌شود.
"""

from __future__ import unicode_literals
from nltk.tag import stanford
from .SequenceTagger import SequenceTagger


class POSTagger(SequenceTagger):
    """این کلاس‌ها شامل توابعی برای برچسب‌گذاری توکن‌هاست. **میزان دقت برچسب‌زنی در نسخهٔ حاضر ۹۷.۱ درصد [^1] است.** این کلاس تمام توابع خود را از کلاس [SequenceTagger][hazm.SequenceTagger.SequenceTagger] به ارث می‌برد.
    [^1]:
            این عدد با انتشار هر نسخه بروزرسانی می‌شود.
    """


class StanfordPOSTagger(stanford.StanfordPOSTagger):
    """ """

    def __init__(self, model_filename, path_to_jar, *args, **kwargs):
        self._SEPARATOR = "/"
        super(stanford.StanfordPOSTagger, self).__init__(
            model_filename=model_filename, path_to_jar=path_to_jar, *args, **kwargs
        )

    def tag(self, tokens):
        """
        Examples:
                >>> tagger = StanfordPOSTagger(model_filename='resources/persian.tagger', path_to_jar='resources/stanford-postagger.jar')
                >>> tagger.tag(['من', 'به', 'مدرسه', 'رفته_بودم', '.'])
                [('من', 'PRO'), ('به', 'P'), ('مدرسه', 'N'), ('رفته_بودم', 'V'), ('.', 'PUNC')]

        """
        return self.tag_sents([tokens])[0]

    def tag_sents(self, sentences):
        """ """
        refined = map(lambda s: [w.replace(" ", "_") for w in s], sentences)
        return super(stanford.StanfordPOSTagger, self).tag_sents(refined)
