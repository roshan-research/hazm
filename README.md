Hazm
====

Python library for digesting Persian text.

+ Text cleaning
+ Sentence and word tokenizer
+ Word lemmatizer
+ POS tagger
+ Shallow parser
+ Dependency parser
+ Interfaces for Persian corpora
+ [NLTK](http://nltk.org/) compatible
+ Python 2.7, 3.4 and 3.5 support
+ [![Build Status](https://travis-ci.org/sobhe/hazm.png)](https://travis-ci.org/sobhe/hazm)


## Usage

```python
>>> from __future__ import unicode_literals
>>> from hazm import *

>>> normalizer = Normalizer()
>>> normalizer.normalize('اصلاح نويسه ها و استفاده از نیم‌فاصله پردازش را آسان مي كند')
'اصلاح نویسه‌ها و استفاده از نیم‌فاصله پردازش را آسان می‌کند'

>>> sent_tokenize('ما هم برای وصل کردن آمدیم! ولی برای پردازش، جدا بهتر نیست؟')
['ما هم برای وصل کردن آمدیم!', 'ولی برای پردازش، جدا بهتر نیست؟']
>>> word_tokenize('ولی برای پردازش، جدا بهتر نیست؟')
['ولی', 'برای', 'پردازش', '،', 'جدا', 'بهتر', 'نیست', '؟']

>>> stemmer = Stemmer()
>>> stemmer.stem('کتاب‌ها')
'کتاب'
>>> lemmatizer = Lemmatizer()
>>> lemmatizer.lemmatize('می‌روم')
'رفت#رو'

>>> tagger = POSTagger(model='resources/postagger.model')
>>> tagger.tag(word_tokenize('ما بسیار کتاب می‌خوانیم'))
[('ما', 'PRO'), ('بسیار', 'ADV'), ('کتاب', 'N'), ('می‌خوانیم', 'V')]

>>> chunker = Chunker(model='resources/chunker.model')
>>> tagged = tagger.tag(word_tokenize('کتاب خواندن را دوست داریم'))
>>> tree2brackets(chunker.parse(tagged))
'[کتاب خواندن NP] [را POSTP] [دوست داریم VP]'

>>> parser = DependencyParser(tagger=tagger, lemmatizer=lemmatizer)
>>> parser.parse(word_tokenize('زنگ‌ها برای که به صدا درمی‌آید؟'))
<DependencyGraph with 8 nodes>

```


## Installation
The latest stabe verson of Hazm can be installed through `pip`:

	pip install hazm

But for testing or using Hazm with the latest updates you may use:

	pip install https://github.com/sobhe/hazm/archive/master.zip --upgrade

We have also trained [tagger and parser models](https://github.com/sobhe/hazm/releases/download/v0.5/resources-0.5.zip). You may put these models in the `resources` folder of your project.


## Extensions

Note: These are not official versions of hazm, not uptodate on functionality and are not supported by Sobhe.

+ [**JHazm**](https://github.com/mojtaba-khallash/JHazm): A Java port of Hazm
+ [**NHazm**](https://github.com/mojtaba-khallash/NHazm): A C# port of Hazm

## Thanks

+ to constributors: [Mojtaba Khallash](https://github.com/mojtaba-khallash) and [Mohsen Imany](https://github.com/imani).
+ to [Virastyar](http://virastyar.ir/) project for persian word list.
