#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 00:23:15 2023

@author: obtic2023
"""
import re
import glob
import spacy
import json
import sklearn
import os

from sklearn.neighbors import DistanceMetric
from sklearn.feature_extraction.text import CountVectorizer

def lire_fichier (chemin):
    with open(chemin) as json_data: 
        dist =json.load(json_data)
    return dist

def get_distances(texte1, texte2, N=1, liste_name =["jaccard", "braycurtis","dice", "cosinus"] ):
    dico = {}
    for metric_name in liste_name :
        dico[metric_name] = []
        liste_resultat_dist2 = []
        for n_max in range(1, N+1):###range([min, default = 0], max, [step, default = 1]) 
            V = CountVectorizer(ngram_range=(1,n_max ), analyzer='char') 
            X = V.fit_transform([texte1, texte2]).toarray()
            if metric_name!= "cosinus" :  
                dist = DistanceMetric.get_metric(metric_name)     
                distance_tab1=dist.pairwise(X)
                liste_resultat_dist2.append(distance_tab1[0][1])
            else: 
                distance_tab1=sklearn.metrics.pairwise.cosine_distances(X) 
                liste_resultat_dist2.append(distance_tab1[0][1])
            dico[metric_name] = liste_resultat_dist2
    return dico


path="../DATA/train_court.json" 
#for chemin in glob.glob("%s/*.json"%path_corpora):
path_dist=lire_fichier(path)
# print(path_dist)

liste_question=[]
liste_reponse=[]
liste_subject=[]
# nlp = spacy.load("fr_core_news_lg")
dic_mots={}   
liste_tok=[] 
liste_nom_fichier=[]
liste_bonne_rep=[]
i=0
for l in path_dist:
    # print(l)
    for key, value in l.items():
        # print (value)
        if key=="question":
            liste_question.append(value)
            
            # print("????????valeur question????????",value)
        if key=="answers":
            liste_reponse.append(value)
            # print("---------valeur réponse---------",value)
        # if key=="subject_name":
        #     liste_subject.append(value)
        #     # print("**********subject_name*******", value)
        
        if key=="correct_answers":
            liste_bonne_rep.append(value)

dico_distance={}
i=0
for q in liste_question:
    # dico_distance[q]={}
    i=i+1
    print("QUESTION??????????",q[:50],"/n QUESTION************", liste_question[i], i)
    

    # distances = get_distances(q,q+1)
    