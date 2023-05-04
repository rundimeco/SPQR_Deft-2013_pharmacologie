from .functions import *

def getDataKeywords(data,listeTri):
    "extraction des mots clefs d'un dataset"
    "data : string"
    "listeTri : string"

    #variables de nommage
    dt = data.split('/')[-1].replace(".csv","")
    lt = listeTri.split('/')[-1].replace(".txt","")

    #ouverture des fichiers
    listeTri = openListe(listeTri)
    df = pd.read_csv(data,delimiter=";")

    #récupération des colonnes importantes
    questions = df["question"]
    ids = df["id"]

    #initialisation du dictionnaire de mots clefs
    vocByQuestions = {}

    #récupération des mots clefs pour chaque duo question/réponse
    for i in range(len(df)):
        vocByQuestions[ids[i]] = []
        keywords_q = getKeywords(questions[i],listeTri)
        for element in ["answers."+l for l in "abcde"]:
            keywords = getKeywords(df[element][i],listeTri)
            if len(keywords) < 1:
                keywords = ["NULL"] #pour les réponses sans mots clef
            vocByQuestions[ids[i]].append(keywords_q+keywords)

    #sauvegarde du résultat
    writeJson(f"output/Dataset/vocByQuestions_{dt}_{lt}.json",vocByQuestions)