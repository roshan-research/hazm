# from break_words import *
import itertools
import kenlm
from optparse import OptionParser
from hazm import *
from azbar import TextCleaner

# address should be check while use
# lm_path = '/home/sobhe/harf-asr/resources//lm.binary'
lm_path = '/home/sobhe/harf-train/resources/lm_data/lm_formal.binary'
# cleaner = TextCleaner('/home/sobhe/azbar/resources/chars.klm')
lm = kenlm.Model(lm_path)

def get_lm_option_parser():
    parser = OptionParser()
    parser.add_option("--input", dest="input_path", metavar="FILE", default=None)
    parser.add_option("--output", dest="output_path", metavar="FILE", default=None)
    parser.add_option("--output-split", dest="output_split_path", metavar="FILE", default=None)
    parser.add_option("--diff", action="store_true", dest="diff",
                      help="Only keep difference lines", default=False)
    parser.add_option("--repeat", dest="repeat", type="int", default=1)
    return parser

def lm_score(text):
    return lm.score(text, bos=False, eos=False) / len(text) if text.split() else lm.score(text, bos=False, eos=False)


# def getNoOfPossibleSentences(changedWord):
#     returnNumber = 1
#     for i in range(len(changedWord)):
#         if isinstance(changedWord[i],list):
#             returnNumber = returnNumber * len(changedWord[i])
#     return returnNumber


def getPossibleSentences(listWords):
    returnList = [""]
    changed = []
    # for s in listWords:
    #     for word_l in s:
    #         if len(word_l) == 1:
    #             changed.append(word_l[0])
    #         else:
    #             wordlist = []
    #             for j in word_l:
    #                 wordlist.append(j)
    #             wordlist = list(set(wordlist))
    #             if len(wordlist) == 1:
    #                 changed.append(wordlist[0])
    #             else:
    #                 changed.append(wordlist)
    for s in listWords:
        for word_l in s:
            if len(word_l) == 1:
                changed.append(word_l[0])
            else:
                # wordlist = []
                changed.append(word_l)
                # for j in word_l:
                #     wordlist.append(j)
                # if len(wordlist) == 2:
                #     changed.append(wordlist[0])
                # else:
                #     wordlist = list(set(wordlist))
                #     changed.append(wordlist)
    with open("debug.txt", "a", encoding='utf-8') as debug:
        debug.write(str(changed) + "\n")
    # NoOfSentences = getNoOfPossibleSentences(changed)
    # if NoOfSentences > 100000:
    #     changed = []
    #     for s in listWords:
    #         for word_l in s:
    #             if len(word_l) == 1:
    #                 changed.append(word_l[0])
    #             else:
    #                 wordlist = []
    #                 for j in word_l:
    #                     wordlist.append(j)
    #                 if len(wordlist) == 2:
    #                     changed.append(wordlist[0])
    #                 else:
    #                     wordlist = list(set(wordlist))
    #                     changed.append(wordlist)
    #     with open("debug.txt", "a", encoding='utf-8') as debug:
    #         debug.write("----------------------" + "\n")
    #         debug.write(str(changed) + "\n")
    for i in range(len(changed)):
        if isinstance(changed[i], list):
            lenBeforeChange = len(returnList)
            for j in range(len(returnList)):
                for k in range(len(changed[i])):
                    returnList.append(returnList[j])
            for j in range(lenBeforeChange):
                returnList.remove(returnList[0])
            for j in range(len(returnList)):
                for k in range(len(changed[i])):
                    if j % len(changed[i]) == k:
                        returnList[j] += changed[i][k] + " "
        else:
            for j in range(len(returnList)):
                returnList[j] += changed[i] + " "
    for i in range(len(returnList)):
        returnList[i] = returnList[i][:-1]
        returnList[i] = returnList[i].replace("_", " ")
    # with open("debug_output-broken4.txt", "a", encoding='utf-8') as debug:
    #     debug.write(str(returnList) + "\n")
    #     debug.write(str(returnList[0]) + "\n")

    return returnList

if __name__ == "__main__":
    parser = get_lm_option_parser()
    (options, args) = parser.parse_args()
    normalizer = Normalizer()
    standardizer = InformalNormalizer()

    with open(options.input_path, "r", encoding='utf-8') as r, open(options.output_path, "w", encoding='utf-8') as w:
        for i, line in enumerate(r):
            sen = line.strip()
            # clean_text = cleaner.clean_text(sen)
            st_l = standardizer.normalize(sen)
            with open("debug.txt", "a", encoding='utf-8') as debug:
                debug.write(str(i+1) + "\n")
                debug.write("sen is:" + str(sen) + "\n")
                # debug.write("clean sen is:" + str(clean_text) + "\n")
            possibleSentences = getPossibleSentences(st_l)
            sen = ""
            print("length of possible sentences: ", len(possibleSentences))
            # if len(possibleSentences) > 10:
            #     with open("debug2.txt", "a", encoding='utf-8') as debug:
            #         debug.write(" complex sen number is:" + str(i+1) + "\n")
            # if len(possibleSentences) > 100 and len(possibleSentences) < 1001:
            #     with open("debug2.txt", "a", encoding='utf-8') as debug:
            #         debug.write("complex sen number is:" + str(i+1) + "\n")
            max = -10
            for oneSentence in possibleSentences:
                score = lm_score(oneSentence)
                if score > max:
                    max = score
                    sen = oneSentence

            with open("debug.txt", "a", encoding='utf-8') as debug:
                debug.write("result sen is:" + str(sen) + "\n")
            w.write(sen + "\n")
            print(i, end="\r")
    print("\nFinished")
