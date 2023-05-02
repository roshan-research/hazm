Hazm
====
![Tests](https://img.shields.io/github/actions/workflow/status/roshan-research/hazm/tests.yml?branch=master)
![PyPI - Downloads](https://img.shields.io/github/downloads/roshan-research/hazm/total)
![GitHub](https://img.shields.io/github/license/roshan-research/hazm)

Python library for digesting Persian text.
+ Text cleaning
+ Sentence and word tokenizer
+ Word lemmatizer
+ POS tagger
+ Shallow parser
+ Dependency parser
+ Interfaces for Persian corpora
+ [NLTK](http://nltk.org/) compatible
+ Python 2.7, 3.4, 3.5, 3.6, 3.7 and 3.8 support

## Documentation
Visit https://roshan-ai.ir/hazm/docs to view the full documentation.

## Precisions

The `Chunker` and `Lemmatizer` as surface analyzers have a precision of 89.9%. Also, `POSTagger` and `DependencyParser` as morphological taggers, have a precision of 97.1%.

|**Module name**       |**Precision**   |
|----------------------|----------------|
| **Lemmatizer**       | 89.9%          |
| **Chunker**          | 89.9%          |
| **POSTagger**        | 97.1%          |
| **DependencyParser** | 97.1%          |


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
The latest stable version of Hazm can be installed through `pip`:

	pip install hazm

But for testing or using Hazm with the latest updates you may use:

	pip install https://github.com/roshan-research/hazm/archive/master.zip --upgrade

We have also trained [tagger and parser models](https://github.com/roshan-research/hazm/releases/download/v0.5/resources-0.5.zip). You may put these models in the `resources` folder of your project.

## Extensions

Note: These are not official versions of hazm, not uptodate on functionality and are not supported by Roshan.

+ [**JHazm**](https://github.com/mojtaba-khallash/JHazm): A Java port of Hazm
+ [**NHazm**](https://github.com/mojtaba-khallash/NHazm): A C# port of Hazm

## Contribution

We welcome and appreciate any contributions to this repo, such as bug reports, feature requests, code improvements, documentation updates, etc. Please follow the [coding guideline](./CODING.md) when contributing. You can open an issue, fork the repo, write your code, create a pull request and wait for a review and feedback. Thank you for your interest and support in this repo! 

We look forward to collaborating with you! 😊

## Thanks

+ to constributors: [Mojtaba Khallash](https://github.com/mojtaba-khallash) and [Mohsen Imany](https://github.com/imani).
+ to [Virastyar](http://virastyar.ir/) project for persian word list.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=roshan-research/hazm&type=Date)](https://star-history.com/#roshan-research/hazm&Date)
