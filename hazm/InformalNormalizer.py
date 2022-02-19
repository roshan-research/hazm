# coding: utf-8

from __future__ import unicode_literals
import codecs
from hazm.utils import informal_verbs, informal_words, NUMBERS, default_verbs
from hazm.Normalizer import Normalizer
from hazm.Lemmatizer import Lemmatizer
from hazm.Stemmer import Stemmer
from hazm.WordTokenizer import *
from hazm.SentenceTokenizer import *


class InformalNormalizer(Normalizer):

	def __init__(self, verb_file=informal_verbs, word_file=informal_words, seperation_flag=False, **kargs):
		self.seperation_flag = seperation_flag
		self.lemmatizer = Lemmatizer()
		self.ilemmatizer = InformalLemmatizer()
		self.stemmer = Stemmer()
		super(InformalNormalizer, self).__init__(**kargs)

		with codecs.open(verb_file, encoding='utf8') as vf:
			self.pastVerbs = {}
			self.presentVerbs = {}
			for f, i, flag in map(lambda x: x.strip().split(' ', 2), vf):
				splitedF = f.split("#")
				self.presentVerbs.update(
					{i: splitedF[1]}
				)
				self.pastVerbs.update(
					{splitedF[0]: splitedF[0]}
				)
		with codecs.open(default_verbs, encoding='utf8') as vf:
			for f, i in map(lambda x: x.strip().split('#', 2), vf):
				self.presentVerbs.update(
					{i:i}
				)
				self.pastVerbs.update(
					{f: f}
				)

		def informal_to_formal_conjucation(i, f, flag):
			iv = self.informal_conjugations(i)
			fv = self.lemmatizer.conjugations(f)
			res = {}
			if flag:
				for i, j in zip(iv, fv[48:]):
					res[i] = j
					if '‌' in i:
						res[i.replace('‌', '')] = j
						res[i.replace('‌', ' ')] = j
					if i.endswith('ین'):
						res[i[:-1] + 'د'] = j
			else:
				for i, j in zip(iv[8:], fv[56:]):
					res[i] = j
					if '‌' in i:
						res[i.replace('‌', '')] = j
						res[i.replace('‌', ' ')] = j
					if i.endswith('ین'):
						res[i[:-1] + 'د'] = j

			return res

		with codecs.open(verb_file, encoding='utf8') as vf:
			self.iverb_map = {}
			for f, i, flag in map(lambda x: x.strip().split(' ', 2), vf):
				self.iverb_map.update(
					informal_to_formal_conjucation(i, f, flag)
				)

		with codecs.open(word_file, encoding='utf8') as wf:
			self.iword_map = dict(
				map(lambda x: x.strip().split(' ', 1), wf)
			)

		self.words = set()
		if self.seperation_flag:
			self.words.update(self.iword_map.keys())
			self.words.update(self.iword_map.values())
			self.words.update(self.iverb_map.keys())
			self.words.update(self.iverb_map.values())
			self.words.update(self.lemmatizer.words)
			self.words.update(self.lemmatizer.verbs.keys())
			self.words.update(self.lemmatizer.verbs.values())

	def split_token_words(self, token):

		def shekan(token):
			res = ['']
			for i in token:
				res[-1] += i
				if i in set(['ا', 'د', 'ذ', 'ر', 'ز', 'ژ', 'و'] + list(NUMBERS)):
					res.append('')
			while '' in res:
				res.remove('')
			return res

		def perm(lst):
			if len(lst) > 1:
				up = perm(lst[1:])
			else:
				return [lst]
			res = []
			for i in up:
				res.append([lst[0]] + i)
				res.append([lst[0] + i[0]] + i[1:])
			res.sort(key=len)
			return res

		token = re.sub(r'(.)\1{2,}', r'\1', token)
		ps = perm(shekan(token))
		for c in ps:
			if set(map(lambda x: self.ilemmatizer.lemmatize(x), c)).issubset(self.words):
				return ' '.join(c)
		return token


	def normalized_word(self, word):
		"""
		>>> normalizer = InformalNormalizer()
		>>> normalizer.normalized_word('می‌رم')
		['می‌روم', 'می‌رم']
		>>> normalizer = InformalNormalizer(seperation_flag=True)
		>>> normalizer.normalized_word('صداوسیماجمهوری')
		['صداوسیما جمهوری', 'صداوسیماجمهوری']
		"""


		def analyzeWord(word):
			endWordsList = ["هاست", "هایی", "هایم", "ترین", "ایی", "انی", "شان", "شون", "است", "تان", "تون", "مان", "مون",
									  "هام", "هاش", "های", "طور", "ها", "تر", "ئی", "یی", "یم", "ام", "ای", "ان", "هم", "رو", "یت", "ه", "ی", "ش", "و", "ا", "ت", "م"]

			returnList = []

			collectionOfWordAndSuffix = []

			FoundEarly = False

			midWordCondidate = []


			if word.endswith("‌") or word.endswith("‎"):
				word = word[:-1]

			if word in self.lemmatizer.words or word in self.iword_map:
				if word in self.lemmatizer.words:
					collectionOfWordAndSuffix.append(
						{
							"word": word,
							"suffix": []
						}
					)
				if word in self.iword_map:
					collectionOfWordAndSuffix.append(
						{
							"word": self.iword_map[word],
							"suffix": []
						}
					)
				FoundEarly = True

			if word.endswith("‌") or word.endswith("‎"):
				word = word[:-1]
			if not FoundEarly:
				for endWord in endWordsList:
					if word.endswith(endWord):
						sliceWord = word[:-1 * len(endWord)]
						if sliceWord in self.lemmatizer.words or sliceWord in self.iword_map:
							if sliceWord in self.lemmatizer.words:
								collectionOfWordAndSuffix.append(
									{
										"word": sliceWord,
										"suffix": [endWord]
									}
								)
							if sliceWord in self.iword_map:
								collectionOfWordAndSuffix.append(
									{
										"word": self.iword_map[sliceWord],
										"suffix": [endWord]
									}
								)
						else:
							midWordCondidate.append(sliceWord)
							midWordCondidate.append([endWord])

				for endWord in endWordsList:
					for i in range(len(midWordCondidate) - 1):
						if i % 2 == 1:
							continue
						midWord = midWordCondidate[i]
						midWordEndWordList = midWordCondidate[i + 1]
						if midWord.endswith(endWord):
							sliceWord = midWord[:-1 * len(endWord)]
							if sliceWord in self.lemmatizer.words or sliceWord in self.iword_map:
								if sliceWord in self.lemmatizer.words:
									collectionOfWordAndSuffix.append(
										{
											"word": sliceWord,
											"suffix": [endWord] + midWordEndWordList
										}
									)
								if sliceWord in self.iword_map:
									collectionOfWordAndSuffix.append(
										{
											"word": self.iword_map[sliceWord],
											"suffix": [endWord] + midWordEndWordList
										}
									)

			# print("word : " + str(collectionOfWordAndSuffix))
			for i in range(len(collectionOfWordAndSuffix)):
				# if len(collectionOfWordAndSuffix[i]["suffix"]) > 2 and collectionOfWordAndSuffix[i]["suffix"][0] == "ه" and collectionOfWordAndSuffix[i]["suffix"][1].startswith("ا"):
				# 	continue
				newPossibelWordList = appendSuffixToWord(collectionOfWordAndSuffix[i])
				for j in range(len(newPossibelWordList)):
					newPossibelWord = newPossibelWordList[j]
					if newPossibelWord not in returnList:
						returnList.append(newPossibelWord)

			return returnList

		def analyzeVerbWord(word):

			if word in self.pastVerbs:
				word = self.pastVerbs[word]
				return [word]
			# if word in self.presentVerbs:
			# 	word = self.presentVerbs[word]
			# 	return [word]

			if word in self.lemmatizer.words or word in self.iword_map:
				return []

			returnList = []

			collectionOfVerbList = []


			if word.endswith("یم"):
				collectionOfVerbList.append({
					"word" : word[:-2],
					"suffix" : "یم"
				})
			if word.endswith("دم"):
				collectionOfVerbList.append({
					"word": word[:-2],
					"suffix": "دم"
				})
			if word.endswith("دیم"):
				collectionOfVerbList.append({
					"word": word[:-3],
					"suffix": "دیم"
				})
			if word.endswith("ید"):
				collectionOfVerbList.append({
					"word": word[:-2],
					"suffix": "ید"
				})
			if word.endswith("دی"):
				collectionOfVerbList.append({
					"word": word[:-2],
					"suffix": "دی"
				})
			if word.endswith("دید"):
				collectionOfVerbList.append({
					"word": word[:-3],
					"suffix": "دید"
				})
			if word.endswith("ند"):
				collectionOfVerbList.append({
					"word": word[:-2],
					"suffix": "ند"
				})
			if word.endswith("دن"):
				collectionOfVerbList.append({
					"word": word[:-2],
					"suffix": "دن"
				})
			if word.endswith("دند"):
				collectionOfVerbList.append({
					"word": word[:-3],
					"suffix": "دند"
				})
			if word.endswith("ین"):
				collectionOfVerbList.append({
					"word": word[:-2],
					"suffix": "ید"
				})
			if word.endswith("دین"):
				collectionOfVerbList.append({
					"word": word[:-3],
					"suffix": "دین"
				})
			if word.endswith("ست"):
				collectionOfVerbList.append({
					"word": word[:-2],
					"suffix": "ست"
				})
			if word.endswith("م"):
				collectionOfVerbList.append({
					"word": word[:-1],
					"suffix": "م"
				})
			if word.endswith("ی"):
				collectionOfVerbList.append({
					"word": word[:-1],
					"suffix": "ی"
				})
			if word.endswith("ه"):
				collectionOfVerbList.append({
					"word": word[:-1],
					"suffix": "د"
				})
				# collectionOfVerbList.append({
				# 	"word": word[:-1],
				# 	"suffix": "ه است"
				# })
			if word.endswith("د"):
				collectionOfVerbList.append({
					"word": word[:-1],
					"suffix": "د"
				})
			if word.endswith("ن"):
				# if word[:-1].endswith("هست"):
				# 	collectionOfVerbList.append({
				# 		"word": word[:-1],
				# 		"suffix": "ند"
				# 	})
				# elif word[:-1].endswith("ست"):
				# 	collectionOfVerbList.append({
				# 		"word": word[:-3],
				# 		"suffix": "ستند"
				# 	})
				collectionOfVerbList.append({
					"word": word[:-1],
					"suffix": "ن"
				})
				# else:
				# 	collectionOfVerbList.append({
				# 	"word": word[:-1],
				# 	"suffix": "ند"
				# 	})
					# collectionOfVerbList.append({
					# 	"word": word,
					# 	"suffix": ""
					# })
			collectionOfVerbList.append({
				"word": word,
				"suffix": ""
			})
			for i in range(len(collectionOfVerbList)):
				mainWord = collectionOfVerbList[i]["word"]
				collectionOfVerbList[i]["preffix"] = ""
				if mainWord.startswith("بر"):
					modifiedWord = mainWord[2:]
					newMainWord = ""
					if modifiedWord.startswith("نمی"):
						collectionOfVerbList[i]["preffix"] = "برنمی"
						newMainWord = modifiedWord[3:]
					elif modifiedWord.startswith("می"):
						collectionOfVerbList[i]["preffix"] = "برمی"
						newMainWord = modifiedWord[2:]
					elif modifiedWord.startswith("ن"):
						collectionOfVerbList[i]["preffix"] = "برن"
						newMainWord = modifiedWord[1:]
					elif modifiedWord.startswith("بی"):
						collectionOfVerbList[i]["preffix"] = "بربی"
						newMainWord = modifiedWord[2:]
					elif modifiedWord.startswith("ب"):
						collectionOfVerbList[i]["preffix"] = "برب"
						newMainWord = modifiedWord[1:]
					else:
						collectionOfVerbList[i]["preffix"] = "بر"
						newMainWord = modifiedWord
					if newMainWord != "":
						collectionOfVerbList[i]["word"] = newMainWord
				elif mainWord.startswith("نمی"):
					collectionOfVerbList[i]["preffix"] = "نمی"
					collectionOfVerbList[i]["word"] = mainWord[3:]
				elif mainWord.startswith("می"):
					collectionOfVerbList[i]["preffix"] = "می"
					collectionOfVerbList[i]["word"] = mainWord[2:]
				elif mainWord.startswith("ن"):
					collectionOfVerbList[i]["preffix"] = "ن"
					collectionOfVerbList[i]["word"] = mainWord[1:]
				elif mainWord.startswith("بی"):
					collectionOfVerbList[i]["preffix"] = "بی"
					collectionOfVerbList[i]["word"] = mainWord[2:]
				elif mainWord.startswith("ب"):
					collectionOfVerbList[i]["preffix"] = "ب"
					collectionOfVerbList[i]["word"] = mainWord[1:]

			collectionOfRealVerbList = []
			for i in range(len(collectionOfVerbList)):
				mainWord = collectionOfVerbList[i]["word"]
				if mainWord.startswith("‌") or mainWord.startswith("‎"):
					mainWord = mainWord[1:]

				if mainWord in self.pastVerbs:
					collectionOfVerbList[i]["word"] = self.pastVerbs[mainWord]
					collectionOfRealVerbList.append(collectionOfVerbList[i])
				if mainWord in self.presentVerbs:
					collectionOfVerbList[i]["word"] = self.presentVerbs[mainWord]
					collectionOfRealVerbList.append(collectionOfVerbList[i])

			# print("verb : " + str(collectionOfRealVerbList))
			for i in range(len(collectionOfRealVerbList)):
				preffix = collectionOfRealVerbList[i]["preffix"]
				suffix = collectionOfRealVerbList[i]["suffix"]
				mainWord = collectionOfRealVerbList[i]["word"]
				returnWord = preffix
				if preffix.endswith("می"):
					returnWord += "‌"
				returnWord += mainWord
				returnWord += suffix
				if mainWord != "":
					if returnWord not in returnList:
						returnList.append(returnWord)

			return returnList

		def appendSuffixToWord(OneCollectionOfWordAndSuffix):
			mainWord = OneCollectionOfWordAndSuffix["word"]
			suffixList = OneCollectionOfWordAndSuffix["suffix"]
			adhesiveAlphabet = ["ب", "پ", "ت", "ث", "ج", "چ", "ح", "خ", "س", "ش", "ص", "ض", "ع", "غ", "ف", "ق", "ک", "گ", "ل", "م", "ن", "ه", "ی"]
			returnWord = mainWord
			returnWord2 = None
			if len(suffixList) == 0:
				return [returnWord]
			if len(suffixList) > 1:
				if suffixList[0] == "ه" and suffixList[1] == "ا":
					suffixList[0] = "ها"
					suffixList.remove(suffixList[1])
				if suffixList[0] == "ه" and suffixList[1] == "است":
					suffixList[0] = "هاست"
					suffixList.remove(suffixList[1])
				if suffixList[0] == "ت" and suffixList[1] == "ا":
					suffixList[0] = "تا"
					suffixList.remove(suffixList[1])
			# print(suffixList)
			for i in range(len(suffixList)):
				# if suffixList[i] == "هاست":
				# 	for alphabet in adhesiveAlphabet:
				# 		if returnWord.endswith(alphabet):
				# 			returnWord += "‌"
				# 			break
				# 	returnWord += "ها است"
				if suffixList[i] == "شون":
					returnWord += "شان"
				# elif (suffixList[i] == "شان"):
				# 	returnWord += "شان"
				elif suffixList[i] == "تون":
					returnWord += "تان"
				# elif (suffixList[i] == "تان"):
				# 	returnWord += "تان"
				elif suffixList[i] == "مون":
					returnWord += "مان"
				# elif (suffixList[i] == "مان"):
				# 	returnWord += "مان"
				elif suffixList[i] == "هام":
					for alphabet in adhesiveAlphabet:
						if returnWord.endswith(alphabet):
							returnWord += "‌"
							break
					returnWord += "هایم"
				# elif suffixList[i] == "هاش":
				# 	for alphabet in adhesiveAlphabet:
				# 		if returnWord.endswith(alphabet):
				# 			returnWord += "‌"
				# 			break
				# 	returnWord += "هایش"

				# elif suffixList[i] == "است":
				# 	for alphabet in adhesiveAlphabet:
				# 		if returnWord.endswith(alphabet):
				# 			returnWord += "‌"
				# 			break
				# 	returnWord += "ها است"
				# elif suffixList[i] == "یم":
				# 	# returnWord2 = returnWord
				# 	# returnWord2 += " هستیم"
				# 	returnWord += "یم"
				elif suffixList[i] == "ها":
					for alphabet in adhesiveAlphabet:
						if returnWord.endswith(alphabet):
							returnWord += "‌"
							break
					returnWord += "ها"
				elif suffixList[i] == "ا" and suffixList[len(suffixList)-1] == "ا" and not returnWord.endswith("ه"):
					for alphabet in adhesiveAlphabet:
						if returnWord.endswith(alphabet):
							returnWord += "‌"
							break
					returnWord += "ها"
				elif suffixList[i] == "و" and suffixList[len(suffixList)-1] == "و":
					returnWord2 = returnWord
					returnWord2 += " و"
					returnWord += " را"
				# elif suffixList[i] == "ه" and suffixList[len(suffixList)-1] == "ه":
				# 	returnWord2 = returnWord
				# 	returnWord2 += "ه"
				# 	returnWord += " است"

				# elif suffixList[i] == "م" and suffixList[len(suffixList)-1] == "م":
				# 	returnWord2 = returnWord
				# 	returnWord2 += " هم"
				# 	returnWord += "م"

				# elif (suffixList[i] == "ت"):
				# 	returnWord += "ت"
				# elif (suffixList[i] == "ی"):
				# 	returnWord += "ی"
				# elif (suffixList[i] == "یت"):
				# 	returnWord += "یت"

				# elif (suffixList[i] == "ت"):
				# 	returnWord2 = returnWord
				# 	returnWord2 += "ه‌ات"
				# 	returnWord += "ت"
				else:
					returnWord += suffixList[i]
			if returnWord2 != None:
				return [returnWord,returnWord2]
			else:
				return [returnWord]

		def straightForwardResult(word):
			if word == "ب":
				return ["به"]
			if word == "ک":
				return ["که"]
			if word == "ش":
				return ["اش"]
			# if word == "تو":
			# 	return ["در", "تو"]
			# if word == "رو":
			# 	return ["را", "رو"]
			# if word == "چی":
			# 	return ["چه", "چیز"]
			if word == "بش":
				return ["بهش"]
			if word == "پایتون":
				return ["پایتون"]
			if word == "سراتو":
				return ["سراتو"]
			if word == "فالو":
				return ["فالو"]
			if word == "هرجا":
				return ["هرجا"]
			if word == "نشده":
				return ["نشده"]
			if word == "میدان":
				return ["میدان"]
			if word == "میدانی":
				return ["میدانی"]
			if word == "کفا":
				return ["کفا"]
			if word == "وبا":
				return ["و با"]
			if word == "ویا":
				return ["و یا"]
			if word == "نشد":
				return ["نشد"]
			if word == "شو":
				return ["شو"]
			if word == "پاشو":
				return ["پاشو"]
			if word == "میر":
				return ["میر"]
			if word == "بارم":
				return ["بار هم", "بارم"]
			if word == "شو":
				return ["شو", "اش را"]
			if word == "برند":
				return ["برند"]
			if word == "کنه":
				return ["کند"]
			if word == "بتونه":
				return ["بتواند"]
			if word == "باشه":
				return ["باشد"]
			if word == "بخوان":
				return ["بخوان"]
			if word == "بدم":
				return ["بدم"]
			if word == "برم":
				return ["برم"]
			if word == "بده":
				return ["بده"]
			if word == "نده":
				return ["نده"]
			if word == "شهرو":
				return ["شهرو"]
			if word == "شیرو":
				return ["شیرو"]
			if word == "نمانده":
				return ["نمانده"]
			if word == "ندیده":
				return ["ندیده"]
			if word == "نشین":
				return ["نشین"]
			if word == "انا":
				return ["انا"]
			if word == "خونی":
				return ["خونی"]
			if word == "یالا":
				return ["یالا"]
			if word == "میخواند" or word == "می‌خواند":
				return ["می‌خواند"]
			if word == "نمیخواند" or word == "نمی‌خواند":
				return ["نمی‌خواند"]
			if word == "میشه" or word == "می‌شه":
				return ["می‌شود"]
			if word == "می‌شد" or word == "میشد":
				return ["می‌شد"]
			if word == "می‌شدم" or word == "میشدم":
				return ["می‌شدم"]
			if word == "نمی‌شد" or word == "نمیشد":
				return ["نمی‌شد"]
			# if word == "عالیه":
			# 	return ["عالیه", "عالی است"]
			# if word == "رواست":
			# 	return ["روا است"]
			if word == "بردم":
				return ["بردم"]
			# if word == "درسته":
			# 	return ["درسته", "درست است"]
			if word == "شم":
				return ["بشوم"]
			if word == "اوست":
				return ["اوست"]
			if word == "بیا":
				return ["بیا"]
			if word == "نیا":
				return ["نیا"]
			if word == "میاد":
				return ["می‌آید"]
			if word == "میشدم":
				return ["می‌شدم"]
			if word == "میخواست" or word == "می‌خواست":
				return ["می‌خواست"]
			# if word == "گفتن":
			# 	return ["گفتند", "گفتن"]

			return []


		straightForwardWords = straightForwardResult(word)
		if len(straightForwardWords) > 0:
			return straightForwardWords

		verbWordsList = analyzeVerbWord(word)
		if len(verbWordsList) > 0:
			return verbWordsList
		possibleWords = analyzeWord(word)

		# if len(verbWordsList) != 0:
		# 	for i in range(len(verbWordsList)):
		# 		if verbWordsList[i] not in possibleWords:
		# 			possibleWords.append(verbWordsList[i])

		mainWord = word
		if mainWord in possibleWords:
			possibleWords.remove(mainWord)
			possibleWords.append(mainWord)
		else:
			if len(possibleWords) == 0:
				possibleWords.append(mainWord)

		# print("combine result : " + str(possibleWords))
		return possibleWords

	def normalize(self, text):

		sent_tokenizer = SentenceTokenizer()
		word_tokenizer = WordTokenizer()
		text = super(InformalNormalizer, self).normalize(text)
		sents = [word_tokenizer.tokenize(sentence) for sentence in sent_tokenizer.tokenize(text)]

		return [[self.normalized_word(word) for word in sent] for sent in sents]

	def informal_conjugations(self, verb):
		ends = ['م', 'ی', '', 'یم', 'ین', 'ن']
		present_simples = [verb + end for end in ends]
		if verb.endswith('ا'):
			present_simples[2] = verb + 'د'
		else:
			present_simples[2] = verb + 'ه'
		present_not_simples = ['ن' + item for item in present_simples]
		present_imperfects = ['می‌' + item for item in present_simples]
		present_not_imperfects = ['ن' + item for item in present_imperfects]
		present_subjunctives = [
			item if item.startswith('ب') else 'ب' + item for item in present_simples]
		present_not_subjunctives = ['ن' + item for item in present_simples]
		return present_simples + present_not_simples + \
			present_imperfects + present_not_imperfects + \
			present_subjunctives + present_not_subjunctives


class InformalLemmatizer(Lemmatizer):

	def __init__(self, **kargs):
		super(InformalLemmatizer, self).__init__(**kargs)

		temp = []
		self.words = set(self.words.keys())
		for word in self.words:
			if word.endswith("ً"):
				temp.append(word[:-1])

		self.words.update(temp)

		temp = {}
		for verb in self.verbs:
			if verb.endswith("د"):
				temp[verb[:-1] + 'ن'] = self.verbs[verb]

		self.verbs.update(temp)

		with codecs.open(informal_verbs, encoding='utf8') as vf:
			for f, i, flag in map(lambda x: x.strip().split(' ', 2), vf):
				self.verbs.update(dict(
					map(lambda x: (x, f), self.iconjugations(i))
				))

		with codecs.open(informal_words, encoding='utf8') as wf:
			self.words.update(
				map(lambda x: x.strip().split(' ', 1)[0], wf)
			)

	def iconjugations(self, verb):
		ends = ['م', 'ی', '', 'یم', 'ین', 'ن']
		present_simples = [verb + end for end in ends]
		if verb.endswith('ا'):
			present_simples[2] = verb + 'د'
		else:
			present_simples[2] = verb + 'ه'
		present_not_simples = ['ن' + item for item in present_simples]
		present_imperfects = ['می‌' + item for item in present_simples]
		present_not_imperfects = ['ن' + item for item in present_imperfects]
		present_subjunctives = [
			item if item.startswith('ب') else 'ب' + item for item in present_simples]
		present_not_subjunctives = ['ن' + item for item in present_simples]
		return present_simples + present_not_simples + \
			present_imperfects + present_not_imperfects + \
			present_subjunctives + present_not_subjunctives
