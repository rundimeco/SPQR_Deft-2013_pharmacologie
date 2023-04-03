#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 16:36:22 2023

@author: obtic2023
"""
import glob
import json
import spacy
import re
from collections import OrderedDict
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.neighbors import DistanceMetric
from sklearn.feature_extraction.text import CountVectorizer
# import distance
import sklearn



def lire_fichier (chemin):
    with open(chemin) as json_data: 
        dist =json.load(json_data)
    return dist
        
def nom_fichier(chemin):
    for mot in glob.glob(chemin): 
        noms_fichiers = re.split("/", chemin)
#        print("NOM FICHIER",noms_fichiers)
        
        nomsfich = re.split("\.",  noms_fichiers[3])
#        print(nomsfich)
    return nomsfich
        
def stocker(chemin,contenu):                                                    #definition fonction pour stocker fichier en format json
    w=open(chemin,"w")                                                          #ouverture du fichier en mode écriture
    w.write(json.dumps(contenu, indent=2))                                      #écriture du contenu dans le fichier
    w.close()  



#Lexique

path="../DATA/train_court.json" 
#for chemin in glob.glob("%s/*.json"%path_corpora):
path_dist=lire_fichier(path)
# print(path_dist)

liste_question=[]
liste_reponse=[]
liste_subject=[]
nlp = spacy.load("fr_core_news_lg")
dic_mots={}   
liste_tok=[] 
liste_nom_fichier=[]
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

for q in liste_question:
    doc = nlp(q)
    for token in doc:
        liste_tok.append([token.text,token.lemma_, token.pos_])

for r in liste_reponse:
    for keys, values in r.items():
        
        doc = nlp(values)
        for token in doc:
            liste_tok.append([token.text,token.lemma_, token.pos_])
##Frequence
liste_token=[]
for ssl in liste_tok:
    if ssl[-1]=="NOUN":
        liste_token.append(ssl[1])
        print(ssl)
        if len(ssl[1]) > 3:
            if ssl[1] not in dic_mots:
                dic_mots[ssl[1]] = 1
            else:
                dic_mots[ssl[1]] += 1 

new_d = OrderedDict(sorted(dic_mots.items(), key=lambda t: t[0]))

# print(new_d)
## VECTORISATION
Set_00 = set(liste_token)
Liste_00 = list(Set_00)
dic_output = {}
liste_words=[]
matrice=[]

for l in Liste_00:
    if len(l)!=1:
        liste_words.append(l)

# try:
words = np.asarray(liste_words) #So that indexing with a list will work
for w in words:
    liste_vecteur=[]

        
    for w2 in words:
    
            V = CountVectorizer(ngram_range=(2,3), analyzer='char')
#                        dist = DistanceMetric.get_metric("jaccard") 
            X = V.fit_transform([w,w2]).toarray()
#                        distance_tab1=dist.pairwise(X)
            distance_tab1=sklearn.metrics.pairwise.cosine_distances(X) # Distance avec cosinus            
            liste_vecteur.append(distance_tab1[0][1])
        
#    print(liste_vecteur)


#  
    matrice.append(liste_vecteur)
matrice_def=-1*np.array(matrice)
#print(matrice)

##### CLUSTER

###lev_similarity = -1*np.array([[distance.levenshtein(w1,w2) for w1 in words] for w2 in words])   
###affprop = AffinityPropagation(affinity="precomputed", damping= 0.9, random_state = None)
#affprop.fit(lev_similarity)        
affprop = AffinityPropagation(affinity="precomputed", damping= 0.5, random_state = None) 

affprop.fit(matrice_def)
for cluster_id in np.unique(affprop.labels_):
    exemplar = words[affprop.cluster_centers_indices_[cluster_id]]
    cluster = np.unique(words[np.nonzero(affprop.labels_==cluster_id)])
    cluster_str = ", ".join(cluster)
    cluster_list = cluster_str.split(", ")
#                print(" - *%s:* %s" % (exemplar, cluster_str))                
    Id = "ID "+str(i)
    for cle, dic in new_d.items(): 
        if cle == exemplar:
            dic_output[Id] ={}
            dic_output[Id]["Centroïde"] = exemplar
            dic_output[Id]["Freq. centroide"] = dic
            dic_output[Id]["Termes"] = cluster_list
    
    i=i+1
#    print(dic_output)
stocker("train_court_cluster-consinus-2-3-clean.json",dic_output)

# except :        
#     print("**********Non OK***********", path)


#     liste_nom_fichier.append(path)
#     stocker("%s/fichier_non_cluster.json"%liste_nom_fichier)
#     continue 





##Liste séparée question et réponse

        
# liste_tok_q=[] 
# liste_tok_r=[] 
     
# for q in liste_question:
#     doc = nlp(q)
#     for token in doc:
#         liste_tok_q.append([token.text,token.lemma_, token.pos_])

# # for r in liste_reponse:
# #     for keys, values in r.items():
        
# #         doc = nlp(values)
# #         for token in doc:
# #             liste_tok_r.append([token.text,token.lemma_, token.pos_])

# liste_tok.append(liste_tok_q)
# print(len(liste_tok_q))
# # liste_tok.append(liste_tok_r)
# # print(len(liste_tok_r))

# dic_mots_q={}  
# # i=0  

# for ssl in liste_tok_q:
#     if ssl[-1]=="NOUN":
#         print(ssl)
#         if len(ssl[1]) > 3:
#             if ssl[1] not in dic_mots_q:
#                 dic_mots_q[ssl[1]] = 1
#             else:
#                 dic_mots_q[ssl[1]] += 1 
    
# # new_d = OrderedDict(sorted(dic_mots_q.items(), key=lambda t: t[0]))

# # print(new_d)

# dic_mots_r={}  
# for mot in liste_tok_r:
#     if len(mot) > 3:
#         if mot not in dic_mots_r:
#             dic_mots_r[mot] = 1
#         else:
#             dic_mots_r[mot] += 1 
# # new_d = OrderedDict(sorted(dic_mots_r.items(), key=lambda t: t[0]))

# # print(new_d)

