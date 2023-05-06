import re
import os
import json
import glob
import subprocess
import pandas as pd
import string as strii

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_kernels
from sklearn.metrics import DistanceMetric
from sklearn.metrics import pairwise_distances
import scipy.sparse as ss
#import numpy as np

import spacy
sp = spacy.load("fr_core_news_sm")

def isFile(path):
  "confirme si un fichier existe ou non"
  return os.path.isfile(path)

def createFolder(path):
  "création d'un fichier vide au chemin indiqué"
  if not os.path.exists(path):
      os.mkdir(path)

def writeJson(path,data):
    "ouverture et écriture d'un fichier json"
    with open(path,"w",encoding='utf-8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
        
def openJson(path):
    "ouverture et lecture d'un fichier json"
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    return data  

def writeOutputFile(path,string):
    "ouverture et écriture d'un fichier json sans toucher"
    "à son précédent contenu"
    with open(path, 'a',encoding='utf-8') as f:
        f.write(f"{string}\n")    

def cleanOutputFile(path):
    "supression de tout le contenu des fichiers d'un dossier"
    with open(path, 'w',encoding='utf-8') as f:
        f.write("")      

def removePunct(string):
    "suppression des marques de ponctuation dans un string"
    return string.translate(str.maketrans(strii.punctuation, ' '*len(strii.punctuation))) #map punctuation to space

def tokenizer(string):
    "renvoie une liste de mots selon la tokenisation de spacy"
    "(exclu également les stopwords)"
    sp.max_length = 10500000
    spacy_object = sp(string)
    return [word.text for word in spacy_object if word.is_stop == False] #and word.pos_ != "PUNCT" and word.pos_ != "NUM"

def sentenceSplit(string):
    "découpe un texte en liste de phrases"
    sp.max_length = 10500000
    sp.add_pipe('sentencizer')
    spacy_object = sp(string, disable = ['ner', 'parser'])
    return [sentence.text for sentence in spacy_object.sents]

def openListe(path):
    "ouverture d'une liste au format txt"
    with open(path,'r',encoding='utf-8') as f:
        liste = [line.rstrip('\n').lower() for line in f]
    return liste

def getKeywords(string,listeTri):
    "exlcusion et inclusion de mots selon deux listes"
    "afin de créer un vocabulaire exhaustif de mots intéréssants"
    keywords = []
    for word in tokenizer(removePunct(string)):
            word = re.sub(" *","",word)
            if len(word) > 1:
                if word.lower() not in listeTri:
                    keywords.append(word)
    return keywords

def similarity(vec,target,liste,metric='cosine'):
    "renvoie la similarité cosinus entre une target et une liste"
    return pairwise_kernels(vec.transform([target]),liste,metric=metric)[0]

def distMetrics(vec,target,liste,metric='dice'):
    "calcul de plusieurs métriques basiques de sklearn"
    return [ 1-i for i in pairwise_distances(vec.transform([target]).toarray(),liste.toarray(), metric=metric)[0]]
