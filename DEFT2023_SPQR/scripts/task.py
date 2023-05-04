from .functions import *

def createResFile(c,dt,lt,dataset,dataref,min_gram,max_gram,analyzer,seuils,metric='cosine'):
    "fonction complémentaire de task, qui effectue les similarités et range les résultats"

    V = CountVectorizer(lowercase=True,ngram_range=(min_gram,max_gram),analyzer=analyzer)
    X = V.fit_transform(dataref)
    print("Vectorization done")

    counter = 0
    total = len(dataset.keys())

    for key, listes in dataset.items():
        
        good_res_maxi = []
        old_maxi = 0
        
        good_res_seuil = {}
        nb_answers = {}

        counter += 1
        print(f"{counter}/{total}",end="\r")

        for i,question_reponse in enumerate(listes):
            question_reponse = " ".join(question_reponse)

            cos = list(similarity(V,question_reponse,X,metric)[0])
            maxi = max(cos)

            if maxi >= old_maxi:
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

        good_res_maxi = good_res_maxi[0].replace("0","a").replace("1","b").replace("2","c").replace("3","d").replace("4","e")
        writeOutputFile(f"output/Results/{dt}/{c}_{dt}_{lt}/BYMAX_{min_gram}-{max_gram}_{analyzer}_taskPrincipale.csv",f"{key};{good_res_maxi}")
        writeOutputFile(f"output/Results/{dt}/{c}_{dt}_{lt}/BYMAX_{min_gram}-{max_gram}_{analyzer}_taskAnnexe.csv",f"{key};1")
        
        for k,v in good_res_seuil.items():
            good_res = "|".join(v).replace("0","a").replace("1","b").replace("2","c").replace("3","d").replace("4","e")
            writeOutputFile(f"output/Results/{dt}/{c}_{dt}_{lt}/BYSEUIL_{min_gram}-{max_gram}_{analyzer}_{k}_taskPrincipale.csv",f"{key};{good_res}")
            writeOutputFile(f"output/Results/{dt}/{c}_{dt}_{lt}/BYSEUIL_{min_gram}-{max_gram}_{analyzer}_{k}_taskAnnexe.csv",f"{key};{nb_answers[k]}")

            good_res_fusion = good_res
            nb_answers_fusion = nb_answers[k]
            if nb_answers_fusion == 0:
                good_res_fusion = good_res_maxi
                nb_answers_fusion = 1

            writeOutputFile(f"output/Results/{dt}/{c}_{dt}_{lt}/BYFUSION_{min_gram}-{max_gram}_{analyzer}_{k}_taskPrincipale.csv",f"{key};{good_res_fusion}")
            writeOutputFile(f"output/Results/{dt}/{c}_{dt}_{lt}/BYFUSION_{min_gram}-{max_gram}_{analyzer}_{k}_taskAnnexe.csv",f"{key};{nb_answers_fusion}")


def task(corpus,data,listeTri):
    "création de fichiers de résultats selon divers paramètres"
    "corpus : string"
    "data : string"
    "listeTri : string"

    #variables de nommage
    c = corpus.split('/')[-1].replace(".json","")
    dt = data.split('/')[-1].replace(".csv","")
    lt = listeTri.split('/')[-1].replace(".txt","")
    
    #création des fichiers nécéssaires et nettoyage
    createFolder(f"output/Results/{dt}/")
    createFolder(f"output/Results/{dt}/{c}_{dt}_{lt}/")
    for file in glob.glob(f"output/Results/{dt}/{c}_{dt}_{lt}/*.csv"):
        cleanOutputFile(file)

    #ouverture des fichiers
    dataset = openJson(f"output/Dataset/vocByQuestions_{dt}_{lt}.json")
    dataref = [" ".join(liste) for liste in openJson(f"output/Corpus/keywords_{c}_{lt}.json")]

    #initialisation des paramètres
    min_grams = [1]
    max_grams = [2,3]
    analyzers = ["char_wb"]
    seuils = [0.5,0.6,0.7,0.8,0.9]

    #boucle d'exécution selon les paramètres
    for min_gram in min_grams:
        for max_gram in max_grams:
            for analyzer in analyzers:
                createResFile(c,dt,lt,dataset,dataref,min_gram,max_gram,analyzer,seuils)
                print()