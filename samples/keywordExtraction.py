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

def posTagger(text ,pos_model_path = 'POStagger.model'):
    tokens = tokenize(text)
    tagger = POSTagger(pos_model_path)
    return tagger.tag_sents(tokens)

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
    
def text2vec(candidates, sent2vec_model_path = 'sent2vec.model'):
    sent2vec_model = Embedding.SentEmbedding(sent2vec_model_path)
    candidate_vector = [[sent2vec_model[candidate] for candidate in candidates]]
    text_vector = sent2vec_model[' '.join(candidates)]
    return candidate_vector, text_vector


def vectorSimilarity(candidates_vector, text_vector, norm=True):
    candidate_sim_text = cosine_similarity(candidates_vector, text_vector.reshape(1,-1))
    candidate_sim_candidate = cosine_similarity(candidates_vector)
    if(norm):
        return 
    return candidate_sim_text, candidate_sim_candidate

def extractKeyword(candidates, keyword_num):
    candidates_vector, text_vector = text2vec(candidates)
    candidate_sim_text_norm, candidate_sim_candidate_norm = vectorSimilarity()




def embedRank(text, keyword_num):
    token_tag = posTagger(text)
    candidates = extractCandidates(token_tag)
    return extractKeyword(candidates, keyword_num)
    






    
    

    



if __name__ == '__main__':
    text = ''
    keyword_num = 10
    keywords = embedRank(text, keyword_num)