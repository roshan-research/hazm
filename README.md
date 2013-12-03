Hazm
====

Python library for digesting Persian text.

+ Text cleaning
+ Sentence and word tokenizer
+ Word lemmatizer
+ Corpus readers for [Hamshahri](http://ece.ut.ac.ir/dbrg/hamshahri/) and [Bijankhan](http://ece.ut.ac.ir/dbrg/bijankhan/)
+ [NLTK](http://nltk.org/) compatible
+ Python 3.3 and 2.7 support
+ [![Build Status](https://travis-ci.org/nournia/hazm.png)](https://travis-ci.org/nournia/hazm)

## Usage

```python

>>> from hazm import Normalizer
>>> normalizer = Normalizer()
>>> normalizer.normalize('اصلاح نويسه ها و استفاده از نیم‌فاصله پردازش را آسان مي كند')
'اصلاح نویسه‌ها و استفاده از نیم‌فاصله پردازش را آسان می‌کند'

>>> from hazm import sent_tokenize, word_tokenize
>>> sent_tokenize('ما هم برای وصل کردن آمدیم! ولی برای پردازش، جدا بهتر نیست؟')
['ما هم برای وصل کردن آمدیم!', 'ولی برای پردازش، جدا بهتر نیست؟']
>>> word_tokenize('ولی برای پردازش، جدا بهتر نیست؟')
['ولی', 'برای', 'پردازش', '،', 'جدا', 'بهتر', 'نیست', '؟']

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

## Thanks

+ from constributors: [Mojtaba Khallash](https://github.com/mojtaba-khallash) and [Mohsen Imany](https://github.com/imani).
+ from [Virastyar](http://virastyar.ir/) for persian word list.
