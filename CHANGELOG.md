# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Add Windows compatibility without WSL dependency. Thanks @E-Ghafour.
- Enhance the normalizer module with new functionality. Thanks @sir-kokabi.
- Increase the lemmatizer and tokenizer accuracy by adding over 30,000 nouns and 1,000 verbs. Thanks @sir-kokabi.
- Improve the POSTagger and chunker accuracy. Thanks @E-Ghafour.
- Replace patterns with data_maker function in SequenceTagger. Thanks @E-Ghafour.
- Add universal tags support in POSTagger. Thanks @E-Ghafour.
- Update IOBTagger, POSTagger, Chunker to work with the new implementation. Thanks @E-Ghafour.
- Drop Python 2 support and migrate all code to Python 3. Thanks @sir-kokabi.
- Migrate to mkdocs-material 9 for faster and better-looking docs. Thanks @sir-kokabi.
- Fix tests in some modules. Thanks @E-Ghafour and @sir-kokabi.
- Add and increase test coverage in some modules. Thanks @E-Ghafour and @sir-kokabi.
- Overhaul the project structure and GitHub repo to follow the latest standards and tools for easier contribution. Thanks @sir-kokabi.
- Add EZ tag support in PeykareReader. Thanks @E-Ghafour.
- Perform a heavy refactoring of some modules for better code readability and maintainability. Thanks @sir-kokabi.
- Fix various reported issues.

## [0.8.3] - 2023-03-10


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
