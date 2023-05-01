from fuzzywuzzy import fuzz
import pandas as pd 
import spacy
nlp = spacy.load("fr_core_news_lg")
from fuzzywuzzy import fuzz
import json 

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
def getRepDB(keywordQ):
    indx = 0
    rateRef = 0
    corpusA = pd.read_csv("./output/CorpusAnw.csv",delimiter=";")
    keywordDBd = corpusA["ListMed"]
    for ik in range(10): #len(keywordDBd)
        keywordDB = keywordDBd[ik].replace(","," ")
        keywordDB = keywordDB.split()
        _, rate = ComMembList(keywordQ, keywordDB, tol=90)
        if rate > rateRef:
            indx = ik
    return indx