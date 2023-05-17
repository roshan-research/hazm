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
+ Python 3.8, 3.9, 3.10 and 3.11 support

## Documentation
Visit https://roshan-ai.ir/hazm/docs to view the full documentation.

## Precisions

The `Chunker` and `Lemmatizer` as surface analyzers have a precision of 89.9%. Also, `POSTagger` and `DependencyParser` as morphological taggers, have a precision of 97.1%.

|**Module name**           |**Precision**   |
|--------------------------|----------------|
| **Lemmatizer**           | 89.9%          |
| **Chunker**              | 93.4%          |
| **POSTagger**            | 97.2%          |
| **POSTagger(Universal)** | 98.8%          |
| **DependencyParser**     | 97.1%          |


## Usage

```python
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

>>> tagger = POSTagger(model='resources/POSTagger.model')
>>> tagger.tag(word_tokenize('ما بسیار کتاب می‌خوانیم'))
[('ما', 'PRO'), ('بسیار', 'ADV'), ('کتاب', 'N'), ('می‌خوانیم', 'V')]

>>> chunker = Chunker(model='resources/Chunker.model')
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

We welcome and appreciate any contributions to this repo, such as bug reports, feature requests, code improvements, documentation updates, etc. Please follow the [Contribution guideline](./CONTRIBUTION.md) when contributing. You can open an issue, fork the repo, write your code, create a pull request and wait for a review and feedback. Thank you for your interest and support in this repo! 


## Thanks

### Code contributores
![Alt](https://repobeats.axiom.co/api/embed/ae42bda158791645d143c3e3c7f19d8a68d06d08.svg "Repobeats analytics image")

<a href="https://github.com/roshan-research/hazm/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=roshan-research/hazm" />
</a>

### Others
+ Thanks to [Virastyar](http://virastyar.ir/) project for providing the persian word list.

[![Star History Chart](https://api.star-history.com/svg?repos=roshan-research/hazm&type=Date)](https://star-history.com/#roshan-research/hazm&Date)
