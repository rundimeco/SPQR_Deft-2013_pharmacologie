path = "output/evaluationQA/results.txt"
import json

with open(path) as f:
    lignes= f.readlines()

res = {}
for l in lignes:
    dic = eval(l)
    for config, infos in dic.items():
        for score_name, score in infos["score"].items():
            res.setdefault(score_name, [])
            toto =  [round(x, 4) for x in infos["score"].values()]
            res[score_name].append([score, config, toto])

for score_name, liste in res.items():
    print(score_name)
    for res in sorted(liste, reverse=True)[:10]:
        print(res)

