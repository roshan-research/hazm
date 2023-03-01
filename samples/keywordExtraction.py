
from hazm import Embedding, Normalizer, sent_tokenize, word_tokenize, POSTagger
import nltk
import numpy as np
import pandas as pd
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

def posTagger(tokenize_text ,pos_model_path = 'pos'):
    tagger = POSTagger(pos_model_path)
    return tagger.tag(tokenize_text)

def extractGrammer(tagged_text, grammer):
    keyphrase_candidate = set()
    np_parser = nltk.RegexpParser(grammer)
    trees = np_parser.parse_sents(tagged_text)
    for tree in trees:
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):  # For each nounphrase
            # Concatenate the token with a space
            keyphrase_candidate.add(' '.join(word for word, tag in subtree.leaves()))
    keyphrase_candidate = {kp for kp in keyphrase_candidate if len(kp.split()) <= 5}
    keyphrase_candidate = list(keyphrase_candidate)
    return keyphrase_candidate  

def extractCandidates(tagged_text, grammers = grammers):
    all_candidates = set()
    for grammer in grammers:
        all_candidates.update(tagged_text(tagged_text, grammer))
    return np.array(list(all_candidates))
    


def embedRank(text, keyword_num):
    tokens = tokenize(text)
    token_tag = posTagger(tokens)
    candidates = extractCandidates(token_tag)


    
    

    



if __name__ == '__main__':
    text = ''
    keyword_num = 10
    keywords = embedRank(text, keyword_num)