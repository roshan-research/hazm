# Hazm - Persian NLP Toolkit

![Tests](https://img.shields.io/github/actions/workflow/status/roshan-research/hazm/test.yml?branch=master)
![PyPI - Downloads](https://img.shields.io/github/downloads/roshan-research/hazm/total)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hazm)
![GitHub](https://img.shields.io/github/license/roshan-research/hazm)

- [Evaluation](#Evaluation)
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Pretrained-Models](#pretrained-models)
- [Usage](#usage)
- [Documentation](#documentation)
- [Hazm in other languages](#hazm-in-other-languages)
- [Contribution](#contribution)
- [Thanks](#thanks)
  - [Code contributores](#code-contributores)
  - [Others](#others)

## Evaluation
|  Module name   |     |
| :--- | --- |
| DependencyParser | **85.6%** |
| POSTagger | **98.8%** |
| Chunker | **93.4%** |
| Lemmatizer | **89.9%** |

## Introduction

[**Hazm**](https://www.roshan-ai.ir/hazm/) is a python library to perform natural language processing tasks on Persian text. It offers various features for analyzing, processing, and understanding Persian text. You can use Hazm to normalize text, tokenize sentences and words, lemmatize words, assign part-of-speech tags, identify dependency relations, create word and sentence embeddings, or read popular Persian corpora.

## Features

- **Normalization:** Converts text to a standard form, such as removing diacritics, correcting spacing, etc.
- **Tokenization:** Splits text into sentences and words.
- **Lemmatization:** Reduces words to their base forms.
- **POS tagging:** Assigns a part of speech to each word.
- **Dependency parsing:** Identifies the syntactic relations between words.
- **Embedding:** Creates vector representations of words and sentences.
- **Persian corpora reading:** Easily read popular Persian corpora with ready-made scripts and minimal code.

## Installation

To install the latest version of Hazm, run the following command in your terminal:

    pip install hazm

Alternatively, you can install the latest update from GitHub (this version may be unstable and buggy):

    pip install git+https://github.com/roshan-research/hazm.git

## Pretrained-Models

Finally if you want to use our pretrained models, you can download it from the links below: 

| **Module name**          | **Size** |
|:------------------------ |:-------- |
| [**Download WordEmbedding**](https://mega.nz/file/GqZUlbpS#XRYP5FHbPK2LnLZ8IExrhrw3ZQ-jclNSVCz59uEhrxY)        | ~ 5 GB |
| [**Download SentEmbedding**](https://mega.nz/file/WzR0QChY#J1nG-HGq0UJP69VMY8I1YGl_MfEAFCo5iizpjofA4OY)        | ~ 1 GB |
| [**Download POSTagger**](https://drive.google.com/file/d/1Q3JK4NVUC2t5QT63aDiVrCRBV225E_B3)            | ~ 18 MB |
| [**Download UniversalDependencyParser**](https://drive.google.com/file/d/1MDapMSUXYfmQlu0etOAkgP5KDiWrNAV6/view?usp=share_link)     | ~ 15 MB |
| [**Download DependencyParser**](https://drive.google.com/file/d/1Ww3xsZC5BXY5eN8-2TWo40G-WvppkXYD/view?usp=drive_link)     | ~ 13 MB |
| [**Download Chunker**](https://drive.google.com/file/d/16hlAb_h7xdlxF4Ukhqk_fOV3g7rItVtk)              | ~ 4 MB |

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

>>> tagger = POSTagger(model='pos_tagger.model')
>>> tagger.tag(word_tokenize('ما بسیار کتاب می‌خوانیم'))
[('ما', 'PRO'), ('بسیار', 'ADV'), ('کتاب', 'N'), ('می‌خوانیم', 'V')]

>>> chunker = Chunker(model='chunker.model')
>>> tagged = tagger.tag(word_tokenize('کتاب خواندن را دوست داریم'))
>>> tree2brackets(chunker.parse(tagged))
'[کتاب خواندن NP] [را POSTP] [دوست داریم VP]'

>>> word_embedding = WordEmbedding(model_type = 'fasttext', model_path = 'word2vec.bin')
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
