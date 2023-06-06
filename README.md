# Hazm

![Tests](https://img.shields.io/github/actions/workflow/status/roshan-research/hazm/test.yml?branch=master)
![PyPI - Downloads](https://img.shields.io/github/downloads/roshan-research/hazm/total)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hazm)
![GitHub](https://img.shields.io/github/license/roshan-research/hazm)

Python library for digesting Persian text.

- Text cleaning
- Sentence and word tokenizer
- Word lemmatizer
- POS tagger
- Word embedding
- Sent embeddding
- Shallow parser
- Dependency parser
- Interfaces for Persian corpora
- [NLTK](http://nltk.org/) compatible

## Table of content
- [Hazm](#hazm)
- [Installation](#installation)
  - [Download Pre-trained models](#download-pre-trained-models)
- [Usage](#usage)
- [Documentation](#documentation)
- [Modules accuracy](#modules-accuracy)
- [Hazm in other languages](#hazm-in-other-languages)
- [Contribution](#contribution)
- [Thanks](#thanks)
  - [Code contributores](#code-contributores)
  - [Others](#others)

## Installation

The latest stable version of Hazm can be installed through `pip`:

    pip install hazm

But for testing or using Hazm with the latest updates you may use:

    pip install https://github.com/roshan-research/hazm/archive/master.zip --upgrade
    
### Download Pre-trained models

| **Module name**          |  |
|:------------------------ |:--------------------|
| **WordEmbedding**        | [download pre-trained word2vec model](https://mega.nz/file/GqZUlbpS#XRYP5FHbPK2LnLZ8IExrhrw3ZQ-jclNSVCz59uEhrxY)|
| **SentEmbedding**        | [download pre-trained sent2vec model](https://mega.nz/file/WzR0QChY#J1nG-HGq0UJP69VMY8I1YGl_MfEAFCo5iizpjofA4OY)|
| **Chunker**              | [download pre-trained chunker model](https://drive.google.com/file/d/16hlAb_h7xdlxF4Ukhqk_fOV3g7rItVtk)         |
| **POSTagger**            | [download pre-trained pos_tagger model](https://drive.google.com/file/d/1Q3JK4NVUC2t5QT63aDiVrCRBV225E_B3)      |
| **DependencyParser**     | [download pre-trained dependency parser](https://drive.google.com/file/d/1tAy6bV57ZXGCRcxqzMBcsHejr78rRM98)     |

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

>>> tagger = POSTagger(model='resources/pos_tagger.model')
>>> tagger.tag(word_tokenize('ما بسیار کتاب می‌خوانیم'))
[('ما', 'PRO'), ('بسیار', 'ADV'), ('کتاب', 'N'), ('می‌خوانیم', 'V')]

>>> chunker = Chunker(model='resources/chunker.model')
>>> tagged = tagger.tag(word_tokenize('کتاب خواندن را دوست داریم'))
>>> tree2brackets(chunker.parse(tagged))
'[کتاب خواندن NP] [را POSTP] [دوست داریم VP]'

>>> word_embedding = WordEmbedding(model_type = 'fasttext', model_path = 'resources/word2vec.bin')
>>> word_embedding.doesnt_match(['سلام' ,'درود' ,'خداحافظ' ,'پنجره'])
'پنجره'
>>> word_embedding.doesnt_match(['ساعت' ,'پلنگ' ,'شیر'])
'ساعت'

>>> parser = DependencyParser(tagger=tagger, lemmatizer=lemmatizer)
>>> parser.parse(word_tokenize('زنگ‌ها برای که به صدا درمی‌آید؟'))
<DependencyGraph with 8 nodes>

```

## Documentation

Visit https://roshan-ai.ir/hazm/docs to view the full documentation.

## Modules accuracy

| **Module name**          | **accuracy**  |
|:------------------------ |:--------------|
| **Lemmatizer**           | 89.9%         |
| **Chunker**              | 93.4%         | 
| **POSTagger** | 97.2% <br> universal: 98.8% |
| **DependencyParser**     | 97.1%         | 

## Hazm in other languages

**Disclaimer:** These ports are not developed or maintained by Roshan. They may not have the same functionality or quality as the original Hazm..

- [**JHazm**](https://github.com/mojtaba-khallash/JHazm): A Java port of Hazm
- [**NHazm**](https://github.com/mojtaba-khallash/NHazm): A C# port of Hazm

## Contribution

We welcome and appreciate any contributions to this repo, such as bug reports, feature requests, code improvements, documentation updates, etc. Please follow the [Contribution guideline](./CONTRIBUTION.md) when contributing. You can open an issue, fork the repo, write your code, create a pull request and wait for a review and feedback. Thank you for your interest and support in this repo!

## Thanks

### Code contributores

![Alt](https://repobeats.axiom.co/api/embed/ae42bda158791645d143c3e3c7f19d8a68d06d08.svg "Repobeats analytics image")

<a href="https://github.com/roshan-research/hazm/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=roshan-research/hazm" />
</a>

### Others

- Thanks to [Virastyar](http://virastyar.ir/) project for providing the persian word list.

[![Star History Chart](https://api.star-history.com/svg?repos=roshan-research/hazm&type=Date)](https://star-history.com/#roshan-research/hazm&Date)
