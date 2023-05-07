from fuzzywuzzy import fuzz
import pandas as pd 
import spacy
# nlp = spacy.load("fr_core_news_lg")
nlpd = spacy.load("fr_core_news_md")

import json 

from collections import Counter
import re
import numpy as np

def similTestStcs(qst,Stc):

    vectQst = nlpd(qst).vector
    vectStc = nlpd(Stc).vector
    similarity = vectQst.dot(vectStc) / (np.linalg.norm(vectQst) * np.linalg.norm(vectStc))
    # similarity = vectQst.dot(vectStc) / (vectQst.norm() * vectStc.norm())

    return similarity

def count_words(keywordQ, KwCorpus):
    word_counter = Counter()
    cpt = 0
    for word in keywordQ:
        word_singular = re.sub(r's$', '', word) 
        word_plural = word_singular + 's' 
        word_counter[word] = 0
        word_counter[word_singular] = 0
        word_counter[word_plural] = 0

    for text in KwCorpus:
        for word in word_counter:
            if re.search(r'\b{}\b'.format(word), text, re.IGNORECASE):
                cpt += 1
                # word_counter[word] += 1
    return cpt#,word_counter

# Search for Medkeywords in the DB 
def getRepDB(keywordQ,keywordQP,corpus,nwQstp):
    taux_simStc = 0
    indxStc = 0
    taux_sim = 0
    taux_simP = 0
    rateA = 0
    rateAP = 0
    keywordA = [item['keywords'] for item in corpus]

    for ikA in range(len(keywordA)):
        rateA = count_words(keywordQ, keywordA[ikA])
        if rateA > taux_sim:
            rateAP = count_words(keywordQP, keywordA[ikA])
                # print(rateA/len(keywordQ))
                # print(rateAP/len(keywordQP))
                # print("---")
            if rateAP > taux_simP:#> taux_simP:
                indxStc = ikA
                taux_sim = rateA
                taux_simP = rateAP
                    # print(indxStc)
    
    # if indxStc !=0:
    if taux_simP/len(keywordQP)>=0.7:
        # print(rateAP)
        # print(keywordQP)
        # print(rateAP/len(keywordQP))
        # print(corpus[indxStc]['sentence'])
        # print("----")
        taux_simStc = similTestStcs(nwQstp,corpus[indxStc]['sentence'])
        # print(taux_simStc)
    return taux_simStc


def writeJson(path,data):
    with open(path,"w",encoding='utf-8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
