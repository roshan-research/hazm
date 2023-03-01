from hazm import Embedding, Normalizer, sent_tokenize, word_tokenize, POSTagger
import nltk
from sklearn.metrics.pairwise import cosine_similarity

grammers = [
"""
NP:
        {<Ne>?<N.*>}    # Noun(s) + Noun(optional) 
        
""",

"""
NP:
        {<N.*><AJ.*>?}    # Noun(s) + Adjective(optional) 
        
"""
]

def tokenize(text):
    normalizer = Normalizer()
    return [word_tokenize(sent) for sent in sent_tokenize(normalizer(text))]

def posTagger(tokenize_text ,model_path = 'pos'):
    tagger = POSTagger(model_path)
    return tagger.tag(tokenize_text)
    


def embedRank(text, keyword_num):
    tokens = tokenize(text)
    token_tag = posTagger(tokens)

    
    

    



if __name__ == '__main__':
    text = ''
    keyword_num = 10
    keywords = embedRank(text, keyword_num)