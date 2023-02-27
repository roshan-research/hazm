from hazm import *

dadeganReader = DadeganReader("test.conllu")
for sent in dadeganReader.sents():
    print(sent)
    x=0