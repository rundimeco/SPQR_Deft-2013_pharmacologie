# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
#Imports et fonctions

import re
import json
import glob
import pandas as pd
import string as strii

#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_kernels

import spacy
sp = spacy.load("fr_core_news_sm")

def removePunct(string):
    return string.translate(str.maketrans(strii.punctuation, ' '*len(strii.punctuation))) #map punctuation to space

def tokenizer(string):
    spacy_object = sp(string)
    return [word.text for word in spacy_object if word.is_stop == False] #and word.pos_ != "PUNCT" and word.pos_ != "NUM"

def getKeywords(string,liste_mots,liste_keywords):
    keywords = []
    for word in tokenizer(removePunct(string)):
            word = re.sub(" *","",word)
            if len(word) > 1:
                if word.lower() not in liste_mots:
                    keywords.append(word)
                elif word.lower() in liste_keywords:
                    keywords.append(word)
    return keywords

def cosine_similarity(vec,target,liste):
    return pairwise_kernels(vec.transform([target]),liste,metric='cosine')

def writeJson(path,data):
    with open(path,"w",encoding='utf-8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)

def cleanOutputFile(path):
    with open(path, 'w',encoding='utf-8') as f:
        f.write("")         

def writeOutputFile(path,string):
    with open(path, 'a',encoding='utf-8') as f:
        f.write(f"{string}\n")        
        
def openJson(path):
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    return data       


# -

def createResFile(dataset,dataref,min_gram,max_gram,analyzer,seuils):
    
    V = CountVectorizer(lowercase=True,ngram_range=(min_gram,max_gram),analyzer=analyzer)
    X = V.fit_transform(dataref)
    print("Vectorization done")

    counter = 0
    total = len(dataset.keys())

    for key, listes in dataset.items():
        
        good_res_maxi = [""]
        old_maxi= 0
        
        good_res_seuil = {}
        nb_answers = {}

        counter += 1
        print(f"{counter}/{total}",end="\r")

        for i,question_reponse in enumerate(listes):
            question_reponse = " ".join(question_reponse)

            cos = list(cosine_similarity(V,question_reponse,X)[0])
            maxi = max(cos)

            if maxi > old_maxi:
                old_maxi = maxi
                good_res_maxi = [str(i)]
            
            for seuil in seuils:
                
                if str(seuil) not in good_res_seuil:
                    good_res_seuil[str(seuil)] = []
                    
                if str(seuil) not in nb_answers:
                    nb_answers[str(seuil)] = 0
                    
                if max(cos) >= seuil:
                    good_res_seuil[str(seuil)].append(str(i))
                    nb_answers[str(seuil)] += 1

        good_res_maxi = writeOutputFile(f"output/mainTask/BYMAX_{min_gram}-{max_gram}_{analyzer}_taskPrincipale.csv",f"{key};{good_res_maxi}")
        writeOutputFile(f"output/mainTask/BYMAX_{min_gram}-{max_gram}_{analyzer}_taskAnnexe.csv",f"{key};1")
        
        for k,v in good_res_seuil.items():
            good_res = "|".join(v).replace("0","a").replace("1","b").replace("2","c").replace("3","d").replace("4","e")
            writeOutputFile(f"output/mainTask/BYSEUIL_{min_gram}-{max_gram}_{analyzer}_{k}_taskPrincipale.csv",f"{key};{good_res}")
            writeOutputFile(f"output/mainTask/BYSEUIL_{min_gram}-{max_gram}_{analyzer}_{k}_taskAnnexe.csv",f"{key};{nb_answers[k]}")


# +
dataset = openJson("output/similarités/vocByQuestions.json")
#dataset = openJson("output/similarités/test.json")
dataref = [" ".join(liste) for liste in openJson("output/corpusRef/manuelMerckSentencesKeywords.json")][:3]

min_grams = [1]
max_grams = [2,3]
analyzers = ["word","char_wb", "char"]
seuils = [0.6,0.8,0.9]
seuils = [i/20 for i in range(60, 90, 2)]
print("Seuils", seuils)
for min_gram in min_grams:
    for max_gram in max_grams:
        for analyzer in analyzers:
            if "char" in analyzer:
                min_gram+=2
                max_gram+=2
            createResFile(dataset,dataref,min_gram,max_gram,analyzer,seuils)
            print()

# +
#for file in glob.glob("output/mainTask/*.csv"):
#    cleanOutputFile(file)

# +
import glob
import subprocess

cleanOutputFile("output/evaluationQA/results.txt")

for file in glob.glob("output/mainTask/*taskPrincipale.csv"):
    cmd = f"python3 EvaluationQA.py --references='evaluation/train_main.csv' --predictions='{file}'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate() 
    #result = out.split()
    #for lin in result:
        #print(lin)
