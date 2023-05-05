from optparse import OptionParser
import glob
import os
import tqdm
import json

def get_parser():
    parser = OptionParser()
    parser.add_option("-d", "--data", dest="data", help="""Données train/dev""", type="string", default="dev")
    parser.add_option("-t", "--taskAnnexe", help="Traiter la tâche Annexe (par défaut c'est la principale", action="store_true", default = False)
    return parser.parse_args()

def taskPrincipale(data):
  #os.make_dirs("tmp", exist_ok = True)
  dic_res = {}
  for path_csv in tqdm.tqdm(glob.glob(f"output/Results/*/*/*taskPrincipale.csv")):
    out_json = f"{path_csv}.json"
    if os.path.exists(out_json)==False:
      cmd = f"python3 scripts/EvaluationQA.py --references='input/evaluation/{data}Principale.csv' --predictions='{path_csv}' --data='{data}'"
      os.system(cmd)
    with open(out_json) as f:
      res_file = eval(f.read())
    for cle, val in res_file.items():
      if type(val) is str:#version osef
        continue
      for nom_metrique, resultat in val["score"].items():
        dic_res.setdefault(nom_metrique, {"globale" : []})
        this_res = [round(resultat, 5), str(val)]
        dic_res[nom_metrique]["globale"].append(this_res)
        for param, valeur in val.items():
          if param =="score":
            continue
          dic_res[nom_metrique].setdefault(param, [])
          this_res = [round(resultat, 5), f"{param}={valeur}", str(val)]
          dic_res[nom_metrique][param].append(this_res)

  for mesure, dic_mesure in dic_res.items():
    for categorie, liste_res in dic_mesure.items():
      print("-"*20)
      print(categorie, mesure)
      print("-"*20)
      for r in sorted(liste_res, reverse=True)[:5]:
        print(r)


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
    taskPrincipale(o.data)
  else:
    print("Eval Task Annexe non faite")
