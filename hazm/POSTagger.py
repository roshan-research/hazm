#coding=utf8

from nltk.tag import stanford


class POSTagger(stanford.POSTagger):
	def __init__(self, *args, **kwargs):
		kwargs['encoding'] = 'utf8'
		if 'path_to_model' not in kwargs:
			kwargs['path_to_model'] = 'resources/persian.tagger'
		if 'path_to_jar' not in kwargs:
			kwargs['path_to_jar'] = 'resources/stanford-postagger.jar'
		super(stanford.POSTagger, self).__init__(*args, **kwargs)

	def batch_tag(self, sentences):
		"""
		>>> tagger.tag(['من', 'به', 'مدرسه', 'رفته بودم', '.'])
		[('من', 'PR'), ('به', 'PREP'), ('مدرسه', 'N'), ('رفته بودم', 'V'), ('.', 'PUNC')]
		"""
		_sentences = [[item.replace(' ', '_') for item in sentence] for sentence in sentences]
		results = super(stanford.POSTagger, self).batch_tag(_sentences)
		return [[(word, tag[1].split('/')[-1]) for word, tag in zip(sentence, result)] for sentence, result in zip(sentences, results)]


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'tagger': POSTagger()})
