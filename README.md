Hazm
====

Python library for digesting Persian text.

+ Text cleaning
+ Sentence and word tokenizer
+ Word lemmatizer
+ POS tagger
+ Dependency parser
+ Interfaces for Persian corpora 
+ [NLTK](http://nltk.org/) compatible
+ Python 2.7, 3.2, 3.3 and 3.4 support
+ [![Build Status](https://travis-ci.org/sobhe/hazm.png)](https://travis-ci.org/sobhe/hazm)


## Usage

```python
>>> from __future__ import unicode_literals

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

>>> from hazm import POSTagger
>>> tagger = POSTagger(model='resources/postagger.model')
>>> tagger.tag(word_tokenize('ما بسیار کتاب می‌خوانیم'))
[('ما', 'PRO'), ('بسیار', 'ADV'), ('کتاب', 'N'), ('می‌خوانیم', 'V')]

>>> from hazm import DependencyParser
>>> parser = DependencyParser(tagger=tagger, lemmatizer=lemmatizer)
>>> parser.parse(word_tokenize('زنگ‌ها برای که به صدا درمی‌آید؟'))
<DependencyGraph with 8 nodes>

```


## Installation

	pip install hazm

We have also trained [tagger and parser models](http://dl.dropboxusercontent.com/u/90405495/resources.zip). You may put these models in the `resources` folder of your project.


## Extensions

+ [**JHazm**](https://github.com/mojtaba-khallash/JHazm): A Java version of Hazm
+ [**NHazm**](https://github.com/mojtaba-khallash/NHazm): A C# version of Hazm


## Thanks

+ to constributors: [Mojtaba Khallash](https://github.com/mojtaba-khallash) and [Mohsen Imany](https://github.com/imani).
+ to [Virastyar](http://virastyar.ir/) project for persian word list.
