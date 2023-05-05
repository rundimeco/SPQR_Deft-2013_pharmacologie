from .functions import *

def taskPrincipale(data):
    dt = data.split('/')[-1].replace(".csv","")
    cleanOutputFile(f"output/Results/resultsTaskPrincipale_{dt}.txt")
    for file in glob.glob(f"output/Results/{dt}/*/*taskPrincipale.csv"):
        c = file.split('/')[3]
        if file.split('/')[2] == dt:
            cmd = f"python3 scripts/EvaluationQA.py --references='input/evaluation/{dt}Principale.csv' --predictions='{file}' --data='{dt}' --corpus='{c}'"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate() 
            result = out.split()
            for lin in result:
                print(lin)

def taskAnnexe(data):
    dt = data.split('/')[-1].replace(".csv","")
    cleanOutputFile(f"output/Results/resultsTaskAnnexe_{dt}.txt")
    for file in glob.glob(f"output/Results/{dt}/*/*taskAnnexe.csv"):
        if file.split('/')[2] == dt:
            cmd = f"python3 scripts/EvaluationClassification.py --references='input/evaluation/{dt}Annexe.csv' --predictions='{file}' --data='{dt}'"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            out, err = p.communicate() 
            result = out.split()
            for lin in result:
                print(lin)

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
