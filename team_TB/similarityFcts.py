from fuzzywuzzy import fuzz
import pandas as pd 
import spacy
nlp = spacy.load("fr_core_news_lg")
nlpd = spacy.load("fr_core_news_md")
from fuzzywuzzy import fuzz
import json 


def writeJson(path,data):
    with open(path,"w",encoding='utf-8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

        
def ComMembList(keywordQ, keywordR, tol=90):
    rate = 0
    for elt1 in keywordQ:
        for elt2 in keywordR:
            score = fuzz.token_sort_ratio(elt1, elt2)
            if score >= tol:
                rate = rate +1
    if rate > 1:
        return True, rate 
    else:
        return False,rate
    
# Search for Medkeywords in the DB 
def getRepDB(keywordQ,nwQstp):
    indxA = 0
    indxB = 0
    rateRef = 0
    rateA = 0
    rateB = 0
    with open('output/corpusMerck.json', 'r') as f:
        corpusB = json.load(f)
    with open('output/CorpusMS.json', 'r') as fs:
        corpusA = json.load(fs)
    keywordA = [item['keywords'] for item in corpusA]
    keywordB = [item['keywords'] for item in corpusB]
    for ikA in range(len(keywordA)):
        _, rateA = ComMembList(keywordQ, keywordA, tol=90)
        if rateA > rateRef:
            indxA = ikA
    for ikB in range(len(keywordB)):
        _, rateB = ComMembList(keywordQ, keywordB, tol=90)
        if rateB > rateRef:
            indxB = ikB
    
    if indxA !=0:
        rateA = similTestStcs(nwQstp,corpusA[indxA])
    if indxB !=0:
        rateB = similTestStcs(nwQstp,corpusB[indxB])
    
    return max(rateA,rateB)

def similTestStcs(qst,Stc):

    vectQst = nlpd(qst).vector
    vectStc = nlpd(Stc).vector

    similarity = vectQst.dot(vectStc) / (vectQst.norm() * vectStc.norm())

    return similarity