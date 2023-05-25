from scripts.functions import *
from scripts.adaptData import *
from scripts.adaptCorpus import *
from scripts.task import *
from scripts.eval import *

def proceed(args):
  
  corpus = args.corpus
  c = corpus.split('/')[-1].replace(".json","")

  data = args.data
  dt = data.split('/')[-1].replace(".csv","")

  listeTri = args.listeTri
  lt = listeTri.split('/')[-1].replace(".txt","")

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

  parser.add_argument("-k", "--keywords", action="store_true", help="Récupération des mots-clefs. Il faut indiquer un --corpus et/ou un --data. Ne génère rien si les mots-clefs ont déjà étés récupérés.")
  parser.add_argument("-t", "--task", action="store_true", help="Exécution des similarités et création des fichiers de résultats. Il faut indiquer un --corpus et/ou un --data")
  parser.add_argument("--evalPrincipale",action="store_true", help="Evaluation des résultats de la tâche principale. Il faut indiquer un --data.")
  parser.add_argument("--evalAnnexe",action="store_true", help="Evaluation des résultats de la tâche annexe. Il faut indiquer un --data.")
  parser.add_argument("-s","--sortEval",action="store_true", help="tri des résultats de la tâche choisie. Il faut indiquer un --resultFile.")
  
  parser.add_argument("-l","--listeTri",type=str, default="input/listesTri/liste_mots_reduite.txt", help="Liste de tri appliquée")
  parser.add_argument("-d","--data",type=str, default="data/dev.csv", help="Train.csv ou dev.csv ou test.csv.")
  parser.add_argument("-c","--corpus",type=str, default="input/Feedback.json", help="Corpus sur lequel on base notre tâche.")
  parser.add_argument("-r","--resultsFile",type=str, default="output/Results/resultsTaskPrincipale_dev.txt", help="fichier de résultats à trier.")

  args = parser.parse_args()
  proceed(args)
