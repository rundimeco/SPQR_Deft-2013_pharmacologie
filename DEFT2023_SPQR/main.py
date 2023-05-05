from scripts.functions import *
from scripts.adaptData import *
from scripts.adaptCorpus import *
from scripts.task import *
from scripts.eval import *

def proceed(args):
  
  corpus = "input/Manuel_Merck.json"
  if args.corpus:
    corpus = args.corpus
  c = corpus.split('/')[-1].replace(".json","")

  data = "data/test.csv"
  if args.data:
    data = args.data
  dt = data.split('/')[-1].replace(".csv","")
  
  listeTri = "input/listesTri/liste_mots_reduite.txt"
  if args.listeTri:
    listeTri = args.listeTri
  lt = listeTri.split('/')[-1].replace(".txt","")

  resultsFile = "output/Results/resultsTaskPrincipale_train.txt"
  if args.resultsFile:
    resultsFile = args.resultsFile

  if args.keywords:

    print(f"getting {corpus} keywords...")
    if not isFile(f"output/Corpus/keywords_{c}_{lt}.json"):
      getCorpusKeywords(corpus,listeTri)

    print(f"getting {data} keywords...")
    if not isFile(f"output/Dataset/vocByQuestions_{dt}_{lt}.json"):
      getDataKeywords(data,listeTri)

    print("done !")

  if args.task:

    print("getting similarities...")
    task(corpus,data,listeTri)
    print("done !")

  if args.evalPrincipale:
    taskPrincipale(data)

  if args.evalAnnexe:
    taskAnnexe(data)

  if args.sortEval:
    sortEvals(resultsFile)

if __name__ == "__main__":
	
  import argparse
  parser = argparse.ArgumentParser()

  parser.add_argument("-k", "--keywords", action="store_true", help="Création des ressources selon une liste de mots clefs")
  parser.add_argument("-t", "--task", action="store_true", help="Exécution des similarités et création des fichiers de résultats")
  parser.add_argument("--evalPrincipale",action="store_true", help="Evaluation des résultats de la tâche principale")
  parser.add_argument("--evalAnnexe",action="store_true", help="Evaluation des résultats de la tâche annexe")
  parser.add_argument("-s","--sortEval",action="store_true", help="tri des résultats de la tâche choisie")
  
  parser.add_argument("-l","--listeTri",type=str,help="Liste de tri appliquée")
  parser.add_argument("-d","--data",type=str,help="Train.csv ou dev.csv")
  parser.add_argument("-c","--corpus",type=str,help="Corpus sur lequel on base notre tâche")
  parser.add_argument("-r","--resultsFile",type=str,help="fichier de résultats à trier")

  args = parser.parse_args()
  proceed(args)