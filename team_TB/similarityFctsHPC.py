from fuzzywuzzy import fuzz
import pandas as pd 
import spacy
nlpd = spacy.load("fr_core_news_md")

import json 

from collections import Counter
import re
import numpy as np

def writeJson(path,data):
    with open(path,"w",encoding='utf-8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

def similTestStcs(qst,Stc):

    vectQst = nlpd(qst).vector
    vectStc = nlpd(Stc).vector
    similarity = vectQst.dot(vectStc) / (np.linalg.norm(vectQst) * np.linalg.norm(vectStc))
    
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
    return cpt



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
        if rateA >= taux_sim and rateA !=0:
            rateAP = count_words(keywordQP, keywordA[ikA])
            if rateAP > taux_simP:
                indxStc = ikA
                taux_sim = rateA
                taux_simP = rateAP
    if taux_simP/len(keywordQP)>=0.7:
        taux_simStc = similTestStcs(nwQstp,corpus[indxStc]['sentence'])
    return taux_simStc


# ======== HPC V1 =======================

from multiprocessing import Pool, cpu_count

# def count_words_helper(args):
#     text, word_counter = args
#     for word in word_counter:
#         if re.search(r'\b{}\b'.format(word), text, re.IGNORECASE):
#             word_counter[word] += 1

# def count_words(keywordQ, KwCorpus):
#     word_counter = Counter()
#     for word in keywordQ:
#         word_singular = re.sub(r's$', '', word) 
#         word_plural = word_singular + 's' 
#         word_counter[word] = 0
#         word_counter[word_singular] = 0
#         word_counter[word_plural] = 0

#     args = [(text, word_counter) for text in KwCorpus]
#     with Pool(cpu_count()) as p:
#         p.map(count_words_helper, args)

#     cpt = sum(word_counter.values())
#     return cpt

# ----

def process_subcorpus(subcorpus, keywordQ, keywordQP, nwQstp):
    taux_simStc = 0
    indxStc = 0
    taux_sim = 0
    taux_simP = 0
    keywordA = [item['keywords'] for item in subcorpus]

    for ikA in range(len(keywordA)):
        rateA = count_words(keywordQ, keywordA[ikA])
        if rateA >= taux_sim and rateA !=0:
            rateAP = count_words(keywordQP, keywordA[ikA])
            if rateAP > taux_simP:
                indxStc = ikA
                taux_sim = rateA
                taux_simP = rateAP
    
    if taux_simP/len(keywordQP)>=0.7:
        taux_simStc = similTestStcs(nwQstp,subcorpus[indxStc]['sentence'])
    return taux_simStc

def getRepDB_parallel(keywordQ,keywordQP,corpus,nwQstp):
    num_processes = cpu_count()
    chunk_size = int(np.ceil(len(corpus) / num_processes))
    subcorpora = [corpus[i:i+chunk_size] for i in range(0, len(corpus), chunk_size)]

    results = []
    with Pool(num_processes) as pool:
        for subcorpus in subcorpora:
            result = pool.apply_async(process_subcorpus, (subcorpus, keywordQ, keywordQP, nwQstp))
            results.append(result)
        
        taux_simStc_list = [result.get() for result in results]

    return max(taux_simStc_list)

