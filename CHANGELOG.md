# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Add windows compaitiblity by replacing `Wapiti` with `Python-crfsuite`. @E-Ghafour.
- Add `seperate_mi parameter` to `Normalizer` to separate the prefixes «می» and «نمی» in verbs (می‌خوانم instead of میخوانم). @sir-kokabi. 
- Add `remove_specials_chars` parameter to `Normalizer` to remove non-useful characters for text processing (e.g. ۝۞). @sir-kokabi.
- Add `decrease_repeated_chars` parameter to `Normalizer` to remove extra repeated characters. @sir-kokabi.
- Add `unicodes_replacement` parameter to `Normalizer` to replace some characters with standard ones (e.g. محمد instead of ﷴ). @sir-kokabi.
- Add regex pattern to `Normalizer` to convert «هها» to «ه‌ها» (e.g. شنبه‌ها instead of شنبهها). @sir-kokabi.
- Add regex pattern to `Normalizer` to remove unneded ZWNJs after and before space. @sir-kokabi.
- Add regex pattern to `Normalizer` to correct text with letters and numbers (e.g. پلاک ۱۲ instead of پلاک۱۲). @sir-kokabi.
- Add more Non-standard unicode characters to be replaced in `Normalizer`. @sir-kokabi.
- Add regex pattern to `Normalizer` to remove unneded ZWNJs at the start and end of words. @sir-kokabi.
- Add 40,000+ new words to improve `Lemmatizer` and `Tokenizer`. @sir-kokabi.
- `PersianPlainTextReader`, remove diacritics, new nltk compatibility (#120). @mhbashari.
- Support slash & back-slash (/ \) in `Tokenizer` (#102). @elahimanesh.
- Support universal POS mapper to `PeykareReader` & `DadeganReader` (#239). @phsfr.
- Fix pep8 issues. (#135). @hadifar.
- Add translate_nums option to `Normalizer` (#16). @kharazi.
- Change می روم to می‌روم in example (#203). @SMSadegh19.
- Improve `InformalNormalizer` #219. @riasati.
- Add new tests and fix some tests. @sir-kokabi @E-Ghafour.
- Move Corpus Readers to `CorpusReaders` folder. @sir-kokabi.
- Update accuracy of `Lemmatizer`, `POSTagger`, `DependencyParser` in the readme. @E-Ghafour.
- Add Contribution section to readme. @sir-kokabi.
- Add `POSTagger` and `Chunker` accuracy to docs. @sir-kokabi.
- Add a central `CHANGELOG.md`. @sir-kokabi.
- Add new GitHub workflows. @sir-kokabi.
- Add an example of extracting keywords with the help of [hazm](https://github.com/roshan-research/hazm) to docs. @E-Ghafour @sir-kokabi.
- Add [Contribution](https://github.com/roshan-research/hazm/blob/master/CONTRIBUTION.md) and [Coding guide](https://github.com/roshan-research/hazm/blob/master/CODING.md). @sir-kokabi.
- Add some [shields](https://shields.io/) to readme. @sir-kokabi.
- Improve `conjugation` function. @sir-kokabi.
- Fix `Stemmer` issues with multiple suffixes. @sir-kokabi.
- Refactor and optimize codes. @sir-kokabi.
- Fix reported issues.
- Migrate from Travis to GitHub Action. @sir-kokabi.
- Remove `remove_extra_spaces`, `affix_spacing` and `punctuation_spacing` parameters from `Normalizer` and replace them with one `correct_spacing` parameter. @sir-kokabi.
- Remove `token_based` parameter from `Normalizer`. @sir-kokabi.
- Remove `setup.py`, `requirements.txt` and replace them with [pyproject.toml](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) file. @sir-kokabi.
- Remove `tests.py` and run tests with [pytest](https://pytest.org/) via [poethepoet](https://poethepoet.natn.io/). @sir-kokabi.
- Update .gitignore file. @sir-kokabi.
- Use [poetry](https://python-poetry.org/)) tool. @sir-kokabi.
- Change minimum python requirement version to `3.8` in readme. @sir-kokabi.
- Replace **sobhe** with new name **Roshan-Research**. @sir-kokabi.

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
