from .functions import *

def getCorpusKeywords(corpus,listeTri):
    "extraction des mots clefs d'un corpus de référence"
    "corpus : string"
    "listeTri : string"

    #variables de nommage
    c = corpus.split('/')[-1].replace(".json","")
    lt = listeTri.split('/')[-1].replace(".txt","")

    #ouverture des fichiers
    corp = openJson(corpus)
    listeTri = openListe(listeTri)

    #initialisation de la liste de mots clefs
    corpKeywords = []

    #récupération des mots clefs
    for sentence in corp:
        keywords = getKeywords(sentence,listeTri)
        keywords_clean = [x.strip(' ') for x in list(set(keywords)) if x !=""]
        corpKeywords.append(keywords_clean)

    #on retire les listes avec moins de deux éléments
    corpKeywords_clean = [i for i in corpKeywords if len(i) >= 2]

    #sauvegarde du résultat
    writeJson(f"output/Corpus/keywords_{c}_{lt}.json",corpKeywords_clean)