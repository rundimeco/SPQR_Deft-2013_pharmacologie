import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

import spacy
import re 
    
def MedTermDectectionv2(qst):
    qst = qst.lstrip()
    liste = "./input/listeMots_fr.txt"
    with open(liste,'r',encoding='utf-8') as f:
        liste_mots = [line.rstrip('\n').lower() for line in f]
    sol = False 
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(qst.lower())
    for token in doc:
        if token.text not in liste_mots:
            sol = True
    
    return sol 

def splitQst(qst):
    fragQst = re.split('[,|?|:|.]', qst)
    return fragQst


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
    qst = qst.replace(Spword, "")
    doc = nlp(qst)
    Noun_cpt =0
    for token in doc:
        if (token.pos_ =="NOUN" and Noun_cpt==0):
            nwNOUN = MOrF(token.lemma_,nlp)
            var = doc[token.i + 1]
            qst = qst.replace(token.text, nwNOUN)
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

# check M or F
nlp = spacy.load("fr_core_news_sm")
def MOrF(mot,nlp):
    
    doc = nlp(mot)
    genre = doc[0].morph.get("Gender")

    genre = " ".join(genre)

    if genre == "Masc":
        return "un "+mot
    else:
        return "une "+mot

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

def isRequestWrongAns(question):
    tokens = word_tokenize(question)
    keywords = ["faux", "incorrect", "fausse", "mauvaise"]#, "ne", "pas"]
    wrong_answer = False
    for keyword in keywords:
        if keyword in tokens:
            wrong_answer = True
            break
    return wrong_answer
