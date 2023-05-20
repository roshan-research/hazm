from hazm import pos_tagger


from hazm import POSTagger
from hazm import word_tokenize

tagger = POSTagger(model="resources/pos_tagger.model")
print(tagger.tag(word_tokenize("ما بسیار کتاب می‌خوانیم")))