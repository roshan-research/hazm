# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Windows compaitiblity by using `Python-crfsuite` instead of `Wapiti`. @E-Ghafour.
- Four parameters to Normalizer for better text processing: `seperate_mi`, `remove_specials_chars`, `decrease_repeated_chars`, and `unicodes_replacement`. @sir-kokabi.
- Three regex patterns to Normalizer to fix ZWNJs and spacing issues. @sir-kokabi.
- 400 Non-standard unicode characters to be replaced in `Normalizer`. @sir-kokabi.
- 40,000+ new words to improve `Lemmatizer` and `Tokenizer`. @sir-kokabi.
- `PersianPlainTextReader` to process raw text datasets (#120). @mhbashari.
- Slash & back-slash (/ \) support in `Tokenizer` (#102). @elahimanesh.
- Support universal POS mapper in `PeykareReader` & `DadeganReader` (#239). @phsfr.
- `data_maker` function instead of pattern in SequenceTagger. @E-Ghafour.
- Support Universal tags in POSTagger && EZ tag in PeykareReader. @E-Ghafour.
- `Conjugation` class to handle verb conjugation. @sir-kokabi.

### Fixed
- Improve `InformalNormalizer` #219. @riasati.
- Improve the accuracy of POSTagger and chunker. @E-Ghafour.
- Fix pep8 issues. (#135). @hadifar.
- Fix Some tests issues. @sir-kokabi @E-Ghafour.
- Fix `Stemmer` issues with multiple suffixes. @sir-kokabi.
- Fix various reported issues

### Changed
- Drop Python 2 support and migrate all code to Python 3. @sir-kokabi.
- Change می روم to می‌روم in example (#203). @SMSadegh19.
- Overhaul the project structure and GitHub repo. @sir-kokabi.

**Full Changelog**: https://github.com/roshan-research/hazm/compare/v0.8.2...v0.9.0

## [0.8.2] - 2022-11-29

### Added

- WordEmbedding ([Download the pre-trained fastext model](https://mega.nz/file/GqZUlbpS#XRYP5FHbPK2LnLZ8IExrhrw3ZQ-jclNSVCz59uEhrxY)).
- SentenceEmbedding (Download the pre-trained model from here).
- [Documentation](https://www.roshan-ai.ir/hazm/docs/) by @sir-kokabi & @ruhollahh.
- Degarbayan and MirasText corpus reader. Thanks @maanijou to add Degarbayan interface (#176).

### Fixed

- Improve `InformalNormalizer` by @riasati (#214, #215).
- Improve `README.md` by @edalatfard (#187).
- Fix MAGHSURAH Y bug in normalizer by @mavahedinia (#116).
- Fix endless loop in python3 by @mohamad-qodosi (#186).
- Fix `self.words` in `WordTokenizer` by @SinRas (#190).
- Fix some tokenization issues by @behnam-sa (#199).
- Fix some embedding bugs by @E-Ghafour (#229).
- Fix some some bugs in Embedding by @imani (#230).

### Changed

- Use `set` insetead of `list` to remove duplicate stop words by @Azdy-dev (#175).

## [0.7.0] - 2018-10-12

### Added

- Excremental Informal normalizer.
- A list of stop words.
- A tool for separating contiguous words.
- Quran corpus reader.
- Wikipedia corpus reader.
- Persica corpus reader.
- SentiPers corpus reader.
- TNews corpus reader.

### Fixed

- Improve normalizer to normalize numbers, links and hashtags.

## [0.5.0] - 2015-03-20

### Added

- Interface to use [Wapiti](https://wapiti.limsi.fr/) POSTagger.

### Fixed

- Improve posTagger accuracy.
- Improve DependencyParser accuracy.
  

## [0.4.0] - 2014-12-16

### Added
- Rule-based dependency parsing.
- Dependency parser to tree converter.
- TreeBank corpus reader.
- VerbValency corpus reader.

### Fixed

- Improve POSTagger accuracy.
- Improve DependencyParser accuracy.

## [0.3.0] - 2014-08-28

### Added

- Peykare corpus reader.
- Dadegan corpus reader.

### Fixed

- Improve POSTagger accuracy.
- Improve DependencyParser accuracy.

## [0.2.0] - 2014-07-12

### Added
- List of words from the newest version of Virastyar.
- Persian symbols for quotes and decimals.

### Fixed
- Fix compatibility with new version of NLTK.
- Improve tests.


## [0.1.0] - 2013-12-14

### Added
- Hamshahri corpus reader.
- Bijankhan corpus reader.

### Fixed
- Improve POSTagger accuracy.
- Improve DependencyParser accuracy.
