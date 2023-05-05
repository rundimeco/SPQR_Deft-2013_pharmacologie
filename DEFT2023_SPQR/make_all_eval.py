from optparse import OptionParser
import glob
import os
import tqdm
import json
import re

def get_parser():
    parser = OptionParser()
    parser.add_option("-d", "--data", dest="data", help="""Données train/dev""", type="string", default="dev")
    parser.add_option("-t", "--taskAnnexe", help="Traiter la tâche Annexe (par défaut c'est la principale", action="store_true", default = False)
    parser.add_option("-j", "--json_only", help="Traiter uniquement les jsons déjà formés (=oublie les csv qui n'ont pas été évalués)", action="store_true", default = False)
    return parser.parse_args()

def taskPrincipale(options):
  log = open("reading_errors.log", "w")
  stats_errors ={"read":0, "not_found":0}
  data = options.data
  #os.make_dirs("tmp", exist_ok = True)
  dic_res = {}
  res_files = glob.glob(f"output/Results/{data}/*/*taskPrincipale.csv")
  print(len(res_files), "csv files to process")
  for path_csv in tqdm.tqdm(res_files):
    out_json = f"{path_csv}.json"
    name_corpus = re.split("/", path_csv)[-2]
    seuil = re.findall("0\.[0-9]{1,2}", re.split("/", path_csv)[-1])[0]
    if os.path.exists(out_json)==False:
      cmd = f"python3 scripts/EvaluationQA.py --references='input/evaluation/{data}Principale.csv' --predictions='{path_csv}' --data='{data}'"
      os.system(cmd)
      if options.json_only==True:
        print("json only activé")
        break
    if os.path.exists(out_json)==False:
        log.write(f"Fichier introuvable : {out_json}\n")
        stats_errors["not_found"]+=1
        continue
    with open(out_json) as f:
      try:
        res_file = eval(f.read())
      except:
        log.write(f"fichier illisible avec eval(): {out_json}\n")
        stats_errors["not_found"]+=1
        continue
    for cle, val in res_file.items():
      if type(val) is str:#version osef
        continue
      val["corpus"] = name_corpus
      val["seuil"] = seuil
      for nom_metrique, resultat in val["score"].items():
        dic_res.setdefault(nom_metrique, {"globale" : []})
        for param, valeur in val.items():
          if param =="score":
            continue
          dic_res[nom_metrique].setdefault(f"{param}={valeur}", [])
          this_res = [round(resultat, 5), f"{param}={valeur}", str(val)]
          dic_res[nom_metrique][f"{param}={valeur}"].append(this_res)
        this_res = [round(resultat, 5), str(val)]
        dic_res[nom_metrique]["globale"].append(this_res)

  for mesure, dic_mesure in dic_res.items():
    for categorie, liste_res in dic_mesure.items():
      print("-"*20)
      print(categorie, mesure)
      print("-"*20)
      for r in sorted(liste_res, reverse=True)[:5]:
        print(r)
  log.close()
  print(stats_errors)
def sortEvals(resultsFile):
    with open(resultsFile) as f:
        lignes= f.readlines()
    res = {}
    for l in lignes:
        dic = eval(l)
        dic.pop("version")
        for config, infos in dic.items():
            for score_name, score in infos["score"].items():
                res.setdefault(score_name, [])
                toto =  [round(x, 4) for x in infos["score"].values()]
                res[score_name].append([score, config, toto])
    for score_name, liste in res.items():
        print(score_name)
        for res in sorted(liste, reverse=True)[:10]:
            print(res)

if __name__=="__main__":
  #import sys
  #sortEvals(sys.argv[1])
  o, _ = get_parser()
  if o.taskAnnexe == False:
    taskPrincipale(o)
  else:
    print("Eval Task Annexe non faite")
  print(o)
