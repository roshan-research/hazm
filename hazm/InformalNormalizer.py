# coding: utf-8

"""این ماژول شامل کلاس‌ها و توابعی برای نرمال‌سازی متن‌های محاوره‌ای است.
"""

from __future__ import unicode_literals
import codecs
from .utils import informal_verbs, informal_words, NUMBERS, default_verbs
from .Normalizer import Normalizer
from .Lemmatizer import Lemmatizer
from .Stemmer import Stemmer
from .WordTokenizer import *
from .SentenceTokenizer import *


class InformalNormalizer(Normalizer):
    """این کلاس شامل توابعی برای نرمال‌سازی متن‌های محاوره‌ای است.

    Args:
            verb_file (str, optional): فایل حاوی افعال محاوره‌ای.
            word_file (str, optional): فایل حاوی کلمات محاوره‌ای.
            seperation_flag (bool, optional): اگر `True` باشد و در بخشی از متن به فاصله نیاز بود آن فاصله درج می‌شود.
            **kargs: پارامترهای نامدارِ اختیاری

    """

    def __init__(
        self,
        verb_file=informal_verbs,
        word_file=informal_words,
        seperation_flag=False,
        **kargs
    ):
        self.seperation_flag = seperation_flag
        self.lemmatizer = Lemmatizer()
        self.ilemmatizer = InformalLemmatizer()
        self.stemmer = Stemmer()
        super(InformalNormalizer, self).__init__(**kargs)

        self.sent_tokenizer = SentenceTokenizer()
        self.word_tokenizer = WordTokenizer()

        with codecs.open(verb_file, encoding="utf8") as vf:
            self.pastVerbs = {}
            self.presentVerbs = {}
            for f, i, flag in map(lambda x: x.strip().split(" ", 2), vf):
                splitedF = f.split("#")
                self.presentVerbs.update({i: splitedF[1]})
                self.pastVerbs.update({splitedF[0]: splitedF[0]})
        with codecs.open(default_verbs, encoding="utf8") as vf:
            for f, i in map(lambda x: x.strip().split("#", 2), vf):
                self.presentVerbs.update({i: i})
                self.pastVerbs.update({f: f})

        def informal_to_formal_conjucation(i, f, flag):
            iv = self.informal_conjugations(i)
            fv = self.lemmatizer.conjugations(f)
            res = {}
            if flag:
                for i, j in zip(iv, fv[48:]):
                    res[i] = j
                    if "‌" in i:
                        res[i.replace("‌", "")] = j
                        res[i.replace("‌", " ")] = j
                    if i.endswith("ین"):
                        res[i[:-1] + "د"] = j
            else:
                for i, j in zip(iv[8:], fv[56:]):
                    res[i] = j
                    if "‌" in i:
                        res[i.replace("‌", "")] = j
                        res[i.replace("‌", " ")] = j
                    if i.endswith("ین"):
                        res[i[:-1] + "د"] = j

            return res

        with codecs.open(verb_file, encoding="utf8") as vf:
            self.iverb_map = {}
            for f, i, flag in map(lambda x: x.strip().split(" ", 2), vf):
                self.iverb_map.update(informal_to_formal_conjucation(i, f, flag))

        with codecs.open(word_file, encoding="utf8") as wf:
            self.iword_map = dict(map(lambda x: x.strip().split(" ", 1), wf))

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
        """هرجایی در متن فاصله نیاز بود قرار می‌دهد.

        متأسفانه در برخی از متن‌ها، به بهانهٔ صرفه‌جویی در زمان یا از سرِ تنبلی،
        فاصله‌گذاری‌ها درست رعایت نمی‌شود. مثلاً جملهٔ «تو را دوست دارم.» به این
        شکل نوشته می‌شود: «تورادوست دارم.» این تابع فواصل ضروری را در متن
        ایجاد می‌کند و آن را به شکل صحیح برمی‌گرداند.

        Args:
                token (str): توکنی که باید فاصله‌گذاری شود.

        Returns:
                (str): توکنی با فاصله‌گذاری صحیح.
        """

        def shekan(token):
            res = [""]
            for i in token:
                res[-1] += i
                if i in set(["ا", "د", "ذ", "ر", "ز", "ژ", "و"] + list(NUMBERS)):
                    res.append("")
            while "" in res:
                res.remove("")
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

        token = re.sub(r"(.)\1{2,}", r"\1", token)
        ps = perm(shekan(token))
        for c in ps:
            if set(map(lambda x: self.ilemmatizer.lemmatize(x), c)).issubset(
                self.words
            ):
                return " ".join(c)
        return token

    def normalized_word(self, word):
        """اشکال مختلف نرمالایزشدهٔ کلمه را برمی‌گرداند.

        Examples:
                >>> normalizer = InformalNormalizer()
                >>> normalizer.normalized_word('می‌رم')
                ['می‌روم', 'می‌رم']

                >>> normalizer = InformalNormalizer(seperation_flag=True)
                >>> normalizer.normalized_word('صداوسیماجمهوری')
                ['صداوسیما جمهوری', 'صداوسیماجمهوری']

        Args:
                word(str): کلمه‌ای که باید نرمال‌سازی شود.

        Returns:
                (List[str]): اشکال نرمالایزشدهٔ کلمه.
        """

        def analyzeWord(word):
            endWordsList = [
                "هاست",
                "هایی",
                "هایم",
                "ترین",
                "ایی",
                "انی",
                "شان",
                "شون",
                "است",
                "تان",
                "تون",
                "مان",
                "مون",
                "هام",
                "هاش",
                "های",
                "طور",
                "ها",
                "تر",
                "ئی",
                "یی",
                "یم",
                "ام",
                "ای",
                "ان",
                "هم",
                "رو",
                "یت",
                "ه",
                "ی",
                "ش",
                "و",
                "ا",
                "ت",
                "م",
            ]

            returnList = []

            collectionOfWordAndSuffix = []

            FoundEarly = False

            midWordCondidate = []

            if word.endswith("‌") or word.endswith("‎"):
                word = word[:-1]

            if word in self.lemmatizer.words or word in self.iword_map:
                if word in self.lemmatizer.words:
                    collectionOfWordAndSuffix.append({"word": word, "suffix": []})
                if word in self.iword_map:
                    collectionOfWordAndSuffix.append(
                        {"word": self.iword_map[word], "suffix": []}
                    )
                FoundEarly = True

            if not FoundEarly:
                for endWord in endWordsList:
                    if word.endswith(endWord):
                        sliceWord = word[: -1 * len(endWord)]
                        if (
                            sliceWord in self.lemmatizer.words
                            or sliceWord in self.iword_map
                        ):
                            if sliceWord in self.lemmatizer.words:
                                collectionOfWordAndSuffix.append(
                                    {"word": sliceWord, "suffix": [endWord]}
                                )
                            if sliceWord in self.iword_map:
                                collectionOfWordAndSuffix.append(
                                    {
                                        "word": self.iword_map[sliceWord],
                                        "suffix": [endWord],
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
                            sliceWord = midWord[: -1 * len(endWord)]
                            if (
                                sliceWord in self.lemmatizer.words
                                or sliceWord in self.iword_map
                            ):
                                if sliceWord in self.lemmatizer.words:
                                    collectionOfWordAndSuffix.append(
                                        {
                                            "word": sliceWord,
                                            "suffix": [endWord] + midWordEndWordList,
                                        }
                                    )
                                if sliceWord in self.iword_map:
                                    collectionOfWordAndSuffix.append(
                                        {
                                            "word": self.iword_map[sliceWord],
                                            "suffix": [endWord] + midWordEndWordList,
                                        }
                                    )

            for i in range(len(collectionOfWordAndSuffix)):
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

            if word in self.iword_map:
                return []

            if word in self.lemmatizer.words:
                if word[-1] == "ن":
                    None
                else:
                    return []

            returnList = []

            collectionOfVerbList = []

            endVerbList = [
                "یم",
                "دم",
                "دیم",
                "ید",
                "دی",
                "دید",
                "ند",
                "دن",
                "دند",
                "ین",
                "دین",
                "ست",
                "ستم",
                "ستی",
                "ستیم",
                "ستید",
                "ستند",
                "م",
                "ی",
                "ه",
                "د",
                "ن",
            ]

            for endVerb in endVerbList:
                if word.endswith(endVerb):
                    if endVerb == "ین":
                        collectionOfVerbList.append({"word": word[:-2], "suffix": "ید"})
                    elif endVerb == "ن":
                        collectionOfVerbList.append({"word": word[:-1], "suffix": "ن"})
                        collectionOfVerbList.append({"word": word[:-1], "suffix": "ند"})
                    elif endVerb == "ه":
                        if len(word) > 1:
                            if word[-2] != "د":
                                collectionOfVerbList.append(
                                    {"word": word[:-1], "suffix": "د"}
                                )
                            collectionOfVerbList.append(
                                {"word": word[:-1], "suffix": "ه"}
                            )
                        else:
                            collectionOfVerbList.append(
                                {"word": word[:-1], "suffix": "ه"}
                            )
                    else:
                        collectionOfVerbList.append(
                            {"word": word[: -1 * len(endVerb)], "suffix": endVerb}
                        )
            collectionOfVerbList.append({"word": word, "suffix": ""})
            collectionOfVerbList2 = []
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
                        collectionOfVerbList2.append(
                            {
                                "word": mainWord,
                                "preffix": "",
                                "suffix": collectionOfVerbList[i]["suffix"],
                            }
                        )

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
                    collectionOfVerbList2.append(
                        {
                            "word": mainWord,
                            "preffix": "",
                            "suffix": collectionOfVerbList[i]["suffix"],
                        }
                    )

                elif mainWord.startswith("بی"):
                    collectionOfVerbList[i]["preffix"] = "بی"
                    collectionOfVerbList[i]["word"] = mainWord[2:]
                elif mainWord.startswith("ب"):
                    collectionOfVerbList[i]["preffix"] = "ب"
                    collectionOfVerbList[i]["word"] = mainWord[1:]
                    collectionOfVerbList2.append(
                        {
                            "word": mainWord,
                            "preffix": "",
                            "suffix": collectionOfVerbList[i]["suffix"],
                        }
                    )

            for i in range(len(collectionOfVerbList2)):
                collectionOfVerbList.append(collectionOfVerbList2[i])

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
            adhesiveAlphabet = {
                "ب": "ب",
                "پ": "پ",
                "ت": "ت",
                "ث": "ث",
                "ج": "ج",
                "چ": "چ",
                "ح": "ح",
                "خ": "خ",
                "س": "س",
                "ش": "ش",
                "ص": "ص",
                "ض": "ض",
                "ع": "ع",
                "غ": "غ",
                "ف": "ف",
                "ق": "ق",
                "ک": "ک",
                "گ": "گ",
                "ل": "ل",
                "م": "م",
                "ن": "ن",
                "ه": "ه",
                "ی": "ی",
            }
            returnList = []
            returnWord = mainWord
            returnWord2 = None
            returnWord3 = None
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
            for i in range(len(suffixList)):
                if suffixList[i] == "شون":
                    returnWord += "شان"
                elif suffixList[i] == "تون":
                    returnWord += "تان"
                elif suffixList[i] == "مون":
                    returnWord += "مان"
                elif suffixList[i] == "هام":
                    try:
                        var = adhesiveAlphabet[returnWord[-1]]
                        returnWord += "‌"
                    except:
                        None
                    returnWord += "هایم"
                elif suffixList[i] == "ها":
                    try:
                        var = adhesiveAlphabet[returnWord[-1]]
                        returnWord += "‌"
                    except:
                        None
                    returnWord += "ها"
                elif (
                    suffixList[i] == "ا"
                    and suffixList[len(suffixList) - 1] == "ا"
                    and not returnWord.endswith("ه")
                ):
                    try:
                        var = adhesiveAlphabet[returnWord[-1]]
                        returnWord += "‌"
                    except:
                        None
                    returnWord += "ها"
                elif suffixList[i] == "و" and suffixList[len(suffixList) - 1] == "و":
                    returnWord2 = returnWord
                    returnWord2 += " و"
                    returnWord += " را"

                elif suffixList[i] == "رو" and suffixList[len(suffixList) - 1] == "رو":
                    returnWord += " را"

                elif suffixList[i] == "ه" and suffixList[len(suffixList) - 1] == "ه":
                    returnWord2 = returnWord
                    returnWord2 += "ه"
                    returnWord3 = returnWord
                    returnWord3 += " است"
                    returnWord += "ه است"
                else:
                    returnWord += suffixList[i]
            returnList.append(returnWord)
            if returnWord2 != None:
                returnList.append(returnWord2)
            if returnWord3 != None:
                returnList.append(returnWord3)
            return returnList

        def straightForwardResult(word):
            straightForwardDic = {
                "ب": ["به"],
                "ک": ["که"],
                "ش": ["اش"],
                "بش": ["بهش"],
                "رو": ["را", "رو"],
                "پایتون": ["پایتون"],
                "دست": ["دست"],
                "دستی": ["دستی"],
                "دستم": ["دستم"],
                "دین": ["دین"],
                "شین": ["شین"],
                "سراتو": ["سراتو"],
                "فالو": ["فالو"],
                "هرجا": ["هرجا"],
                "میدان": ["میدان"],
                "میدون": ["میدان"],
                "کفا": ["کفا"],
                "ویا": ["و یا"],
                "نشد": ["نشد"],
                "شو": ["شو"],
                "مشیا": ["مشیا"],
                "پلاسما": ["پلاسما"],
                "فیلیمو": ["فیلیمو"],
                "پاشو": ["پاشو"],
                "میر": ["میر"],
                "بارم": ["بار هم", "بارم"],
                "برند": ["برند"],
                "کنه": ["کند"],
                "بتونه": ["بتواند"],
                "باشه": ["باشد"],
                "بخوان": ["بخوان"],
                "بدم": ["بدم"],
                "برم": ["برم"],
                "بده": ["بده"],
                "نده": ["نده"],
                "شهرو": ["شهرو"],
                "شیرو": ["شیرو"],
                "نگذاشته": ["نگذاشته"],
                "نگرفته": ["نگرفته"],
                "نمیشناخته": ["نمی‌شناخته"],
                "نمی‌شناخته": ["نمی‌شناخته"],
                "بشین": ["بشین"],
                "هارو": ["ها را"],
                "مارو": ["ما را"],
                "میخواسته": ["می‌خواسته"],
                "می‌خواسته": ["می‌خواسته"],
                "نمیخواسته": ["نمی‌خواسته"],
                "نمی‌خواسته": ["نمی‌خواسته"],
                "میتوانسته": ["می‌توانسته"],
                "می‌توانسته": ["می‌توانسته"],
                "میرفته": ["می‌رفته"],
                "می‌رفته": ["می‌رفته"],
                "نشین": ["نشین"],
                "انا": ["انا"],
                "خونی": ["خونی"],
                "خون": ["خون"],
                "یالا": ["یالا"],
                "میخواند": ["می‌خواند"],
                "می‌خواند": ["می‌خواند"],
                "نمیخواند": ["نمی‌خواند"],
                "نمی‌خواند": ["نمی‌خواند"],
                "میده": ["می‌دهد"],
                "می‌ده": ["می‌دهد"],
                "میشه": ["می‌شود"],
                "می‌شه": ["می‌شود"],
                "میشد": ["می‌شد"],
                "می‌شد": ["می‌شد"],
                "میشدم": ["می‌شدم"],
                "می‌شدم": ["می‌شدم"],
                "نمیشد": ["نمی‌شد"],
                "نمی‌شد": ["نمی‌شد"],
                "بردم": ["بردم"],
                "بره": ["بره", "برود"],
                "شم": ["بشوم"],
                "اوست": ["اوست"],
                "بیا": ["بیا"],
                "نیا": ["نیا"],
                "میاد": ["می‌آید"],
                "نشدی": ["نشدی"],
                "بخواند": ["بخواند"],
                "سیا": ["سیا"],
                "میدید": ["می‌دید"],
                "می‌دید": ["می‌دید"],
                "وا": ["وا"],
                "برگشته": ["برگشته"],
                "میخواست": ["می‌خواست"],
                "می‌خواست": ["می‌خواست"],
            }
            try:
                return straightForwardDic[word]
            except:
                return []

        straightForwardWords = straightForwardResult(word)
        if len(straightForwardWords) > 0:
            return straightForwardWords

        verbWordsList = analyzeVerbWord(word)
        if len(verbWordsList) > 0:
            return verbWordsList
        possibleWords = analyzeWord(word)

        mainWord = word
        if mainWord in possibleWords:
            possibleWords.remove(mainWord)
            possibleWords.append(mainWord)
        else:
            if len(possibleWords) == 0:
                possibleWords.append(mainWord)

        return possibleWords

    def normalize(self, text):
        """متن محاوره‌ای را به متن فارسی معیار تبدیل می‌کند.

        Examples:
                >>> normalizer = InformalNormalizer()
                >>> normalizer.normalize('بابا یه شغل مناسب واسه بچه هام پیدا کردن که به جایی برنمیخوره !')
                [[['بابا'], ['یک'], ['شغل'], ['مناسب'], ['برای'], ['بچه'], ['هایم'], ['پیدا'], ['کردن'], ['که'], ['به'], ['جایی'], ['برنمی\u200cخورد', 'برنمی\u200cخوره'], ['!']]]

                >>> normalizer = InformalNormalizer()
                >>> normalizer.normalize('اجازه بدیم همسرمون در جمع خانواده‌اش احساس آزادی کنه و فکر نکنه که ما دائم هواسمون بهش هست .')
                [[['اجازه'], ['بدهیم'], ['همسرمان'], ['در'], ['جمع'], ['خانواده\u200cاش'], ['احساس'], ['آزادی'], ['کند'], ['و'], ['فکر'], ['نکند', 'نکنه'], ['که'], ['ما'], ['دائم'], ['حواسمان'], ['بهش'], ['هست'], ['.']]]

        Args:
                text (str): متن محاوره‌ای که باید تبدیل به متن فارسی معیار شود.

        Returns:
                (List[List[List[str]]]): متن فارسی معیار.

        """

        text = super(InformalNormalizer, self).normalize(text)
        sents = [
            self.word_tokenizer.tokenize(sentence)
            for sentence in self.sent_tokenizer.tokenize(text)
        ]

        return [[self.normalized_word(word) for word in sent] for sent in sents]

    def informal_conjugations(self, verb):
        """صورت‌های صرفی فعل را در شکل محاوره‌ای تولید می‌کند.

        Args:
                verb (str): فعلی که باید صرف شود.

        Returns:
                (List[str]): صورت‌های صرفی فعل.
        """
        ends = ["م", "ی", "", "یم", "ین", "ن"]
        present_simples = [verb + end for end in ends]
        if verb.endswith("ا"):
            present_simples[2] = verb + "د"
        else:
            present_simples[2] = verb + "ه"
        present_not_simples = ["ن" + item for item in present_simples]
        present_imperfects = ["می‌" + item for item in present_simples]
        present_not_imperfects = ["ن" + item for item in present_imperfects]
        present_subjunctives = [
            item if item.startswith("ب") else "ب" + item for item in present_simples
        ]
        present_not_subjunctives = ["ن" + item for item in present_simples]
        return (
            present_simples
            + present_not_simples
            + present_imperfects
            + present_not_imperfects
            + present_subjunctives
            + present_not_subjunctives
        )


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
                temp[verb[:-1] + "ن"] = self.verbs[verb]

        self.verbs.update(temp)

        with codecs.open(informal_verbs, encoding="utf8") as vf:
            for f, i, flag in map(lambda x: x.strip().split(" ", 2), vf):
                self.verbs.update(dict(map(lambda x: (x, f), self.iconjugations(i))))

        with codecs.open(informal_words, encoding="utf8") as wf:
            self.words.update(map(lambda x: x.strip().split(" ", 1)[0], wf))

    def iconjugations(self, verb):
        ends = ["م", "ی", "", "یم", "ین", "ن"]
        present_simples = [verb + end for end in ends]
        if verb.endswith("ا"):
            present_simples[2] = verb + "د"
        else:
            present_simples[2] = verb + "ه"
        present_not_simples = ["ن" + item for item in present_simples]
        present_imperfects = ["می‌" + item for item in present_simples]
        present_not_imperfects = ["ن" + item for item in present_imperfects]
        present_subjunctives = [
            item if item.startswith("ب") else "ب" + item for item in present_simples
        ]
        present_not_subjunctives = ["ن" + item for item in present_simples]
        return (
            present_simples
            + present_not_simples
            + present_imperfects
            + present_not_imperfects
            + present_subjunctives
            + present_not_subjunctives
        )
