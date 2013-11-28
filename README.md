Hazm
====

Python library for digesting Persian text.

+ Python 3.3 and 2.7 compatible
+ NLTK inspired

## Installation

	pip install hazm

## Usage

	>>> from hazm import sent_tokenize, word_tokenize
	>>> sent_tokenize('جدا کردن ساده است. تقریبا البته!')
	['جدا کردن ساده است.', 'تقریبا البته!']
	>>> word_tokenize('این جمله معمولی است.')
	['این', 'جمله', 'معمولی', 'است', '.']

	>>> from hazm import Stemmer, Lemmatizer
	>>> stemmer = Stemmer()
	>>> stemmer.stem('کتاب‌ها')
	'کتاب'
	>>> lemmatizer = Lemmatizer()
	>>> lemmatizer.lemmatize('می‌روم')
	'رفت#رو'

## Tests

	python3 -m hazm.{module}
	python3 -m doctest README.md
