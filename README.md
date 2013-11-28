Hazm
====

Python library for digesting Persian text.

+ NLTK compatible
+ Supports Python 3.3 and 2.7

## Usage

```python

>>> from hazm import Normalizer
>>> normalizer = Normalizer()
>>> normalizer.normalize('اصلاح نويسه ها ، تنظيم فاصله علائم ( نگارشي ) و استفاده از نیم‌فاصله پردازش را آسان می کند')
'اصلاح نویسه‌ها، تنظیم فاصله علائم (نگارشی) و استفاده از نیم‌فاصله پردازش را آسان می‌کند'

>>> from hazm import sent_tokenize, word_tokenize
>>> sent_tokenize('ما برای وصل کردن آمدیم! شما چطور؟')
['ما برای وصل کردن آمدیم!', 'شما چطور؟']
>>> word_tokenize('این جمله معمولی است.')
['این', 'جمله', 'معمولی', 'است', '.']

>>> from hazm import Stemmer, Lemmatizer
>>> stemmer = Stemmer()
>>> stemmer.stem('کتاب‌ها')
'کتاب'
>>> lemmatizer = Lemmatizer()
>>> lemmatizer.lemmatize('می‌روم')
'رفت#رو'

```

## Installation

	pip install hazm

## Tests

	python3 -m doctest README.md
	python3 -m hazm.{module}
