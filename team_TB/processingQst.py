# import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import re 
import spacy
nlp = spacy.load("fr_core_news_sm")
# import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
import json

# Delete between parenthesis
def del_betParenthese(qst):
    matchs = re.findall(r'\((.*?)\)', qst)
    for i in range(len(matchs)):
        if (MedTermDectector(matchs[i],False)):
            qst = qst.replace('('+matchs[i]+')',matchs[i])
    return re.sub(r'\([^()]*\)','', qst)

# save new words
def saveNwWords(qst):
    if '(' in qst or ')' in qst:
        qst = qst.replace('(','')
        qst = qst.replace(')','')
    qst = qst.lstrip()
    qst = qst.rstrip()
    # Ouverture du fichier contenant la liste des mots
    with open('./input/listeMotsFR_Auto.txt', 'r') as f:
        liste_mots = f.read().splitlines()
    # Vérification des mots de la phrase
    # nlp = spacy.load("fr_core_news_sm")
    doc = nlp(qst)
    for mot in doc:
        nwMot = mot.lemma_
        nwMot = nwMot.lower()
        if nwMot not in liste_mots:
            # Ajout du mot au fichier s'il n'existe pas déjà
            with open('./input/listeMotsFR_Auto.txt', 'a') as f:
                f.write(nwMot + '\n')

# Recover fragements with medical/technical terms 
def recoverMedFrag(fragQst,icpt,nwQst,Spword):
    Spword2 = False 
    ListMed = []
    # Récupérer les fragements qui contiennent les infos médicales uniquements 
    isthereMedTerm,ListMed = MedTermDectector(fragQst[icpt],True)
    if (isthereMedTerm): # if it finds a medical term
        var = fragQst[icpt] 
        indx = var.find("concernant")
        if indx==0:
            nwQst = nwQst + ','
        elif indx>0:
            nwQst = nwQst + var[indx:]+','
        else:
            if icpt ==0: # if it's the first fragement
                var = var.split()
                if var[0]=="Parmi":
                    Spword = True
                    # apply changes 
                    fragQst[icpt] = gestionSPword(fragQst[icpt],var[0])
            fragQst[icpt],Spword2 = Check_QuiInSentence(fragQst[icpt])
            nwQst = nwQst + ' ' + fragQst[icpt]
    else:
        fragQst[icpt],Spword2 = Check_QuiInSentence(fragQst[icpt])
        if Spword2:
            nwQst = nwQst + ' ' + fragQst[icpt]
        # save the non-medical words
        saveNwWords(fragQst[icpt])
        # verify the existance of "qui"+"est"-"exact/inexact/vrai/faux"
    if Spword2 or Spword :
        Spword = True 
    return nwQst,Spword,ListMed

def RecoverListMed(qst):
    listMed = []
    qst = qst.lstrip()
    qst = qst.rstrip()
    # liste = "./input/listeMots_fr.txt"
    liste = "./input/listeMotsFR_Auto.txt"
    with open(liste,'r',encoding='utf-8') as f:
        liste_mots = [line.rstrip('\n').lower() for line in f]
    doc = nlp(qst.lower())
    for token in doc:
        if token.text not in liste_mots and token.lemma_ not in listMed and not "":
            listMed.append(token.text)
    if listMed==[]:
        listMed = ['']
    return listMed

# Detection of "Qui" in a sentence
def Check_QuiInSentence(qst):
    indx = qst.find("qui")
    existQui = False
    if indx != -1 and not any(word in qst for word in ["exact","exacte","exactes", "inexact", "inexactes", "vrai", "vraie", "faux"]):
        if not (MedTermDectector(qst[0:indx],False)[0]):
            qst = qst[indx:]
            existQui = True
    # elif indx !=-1 and any(word in qst for word in ["s'applique"]):
    return qst, existQui

# Detection of medical terms in sentence 
def MedTermDectector(qst,RecMedTerm):
    # if '(' in qst or ')' in qst:
    #     qst = qst.replace('(','')
    #     qst = qst.replace(')','')
    listMed = []
    qst = qst.lstrip()
    qst = qst.rstrip()
    liste = "./input/listeMotsFR_Auto.txt"
    # liste = "./input/listeMots_fr.txt"
    with open(liste,'r',encoding='utf-8') as f:
        liste_mots = [line.rstrip('\n').lower() for line in f]
    sol = False 
    doc = nlp(qst.lower())
    for token in doc:
        if RecMedTerm == True and token.lemma_ not in liste_mots and token.lemma_ not in listMed and not "":
            listMed.append(token.lemma_)
            sol = True
    return sol,listMed

def MedTermDectectorv3(qst,RecMedTerm):
    # if '(' in qst or ')' in qst:
    #     qst = qst.replace('(','')
    #     qst = qst.replace(')','')
    listMed = []
    qst = qst.lstrip()
    qst = qst.rstrip()
    liste_mots = openJson("./input/keywordsMesh_modified.json")
    # with open(liste,'r',encoding='utf-8') as f:
    #     liste_mots = [line.rstrip('\n').lower() for line in f]
    sol = False 
    doc = nlp(qst.lower())
    for token in doc:
        if token.text!=' ' and RecMedTerm == True and token.text in liste_mots and not "": 
            listMed.append(token.text)
            sol = True
    return sol,listMed

def openJson(path):
    with open(path,'r',encoding='utf-8') as f:
        data = json.load(f)
    return data  

def splitQst(qst):
    fragQst = re.split('[,|?|:|.]', qst)
    return fragQst

# apply a negation
def appliquer_negation(phrase):
    phrase = phrase[0].lower() + phrase[1:]
    pattern = re.compile(r'\b(peu|pas)\b', flags=re.IGNORECASE)
    matches = pattern.findall(phrase)

    if matches:
        if 'peu' in matches:
            phrase = re.sub(r'\bpeu\b', 'très', phrase, flags=re.IGNORECASE)

        if 'pas' in matches:
            phrase = re.sub(r'\bpas\b', 'très', phrase, flags=re.IGNORECASE)

        if 'ne' not in phrase and 'pas' not in phrase:
            pattern = re.compile(r'\b[a-z]+[aeiouy](ons|ez|ent|ais|ait|aient|erai|eras|erons|erez|eront)\b', flags=re.IGNORECASE)
            match = pattern.search(phrase)

            if match:
                verbe = match.group()
                phrase = re.sub(verbe, 'ne {} pas'.format(verbe), phrase, count=1, flags=re.IGNORECASE)
    return phrase


def gestionSPword(qst,Spword):
    if Spword == "Parmi":
        qst = qst.replace("Parmi les", "")
        qst = qst.replace("Parmi ces", "")
    doc = nlp(qst)
    Noun_cpt =0
    for token in doc:
        if (token.pos_ =="NOUN" and Noun_cpt==0):
            nwNOUN = MOrF(token.lemma_)
            qst = qst.replace(token.text, nwNOUN)
            if len(doc)> token.i+1:
                var = doc[token.i + 1]
                if (var.pos_=="ADJ" and var.lemma_ != "suivant"):
                    qst = qst.replace(var.text, var.lemma_)
                    Noun_cpt = Noun_cpt +1
        elif (token.lemma_ =="suivant"):
            qst = qst.replace(token.text,"")
    return qst.rstrip()

def replaceAtFront(nwmot):
    if nwmot.endswith('s') or nwmot in ['ils', 'elles']:
        return nwmot+' sont des '
    else:
        return nwmot+' est '


def MOrF(mot):
    doc = nlp(mot)
    genre = doc[0].morph.get("Gender")
    genre = " ".join(genre)
    if genre == "Masc":
        return "un "+mot
    else:
        return "une "+mot

# Dectect if it's require a wrong answer
def isRequestWrongAns(question):
    tokens = word_tokenize(question)
    keywords = ["faux", "incorrect", "fausse", "mauvaise"]#, "ne", "pas"]
    wrong_answer = False
    for keyword in keywords:
        if keyword in tokens:
            wrong_answer = True
            break
    return wrong_answer

def writeJson(path,data):
    with open(path,"w",encoding='utf-8') as f:
        json.dump(data,f,indent=4,ensure_ascii=False)