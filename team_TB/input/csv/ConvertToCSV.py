import json

import pandas as pd

for subset in ["train","dev"]:
    
    f_json = open(f"./json/{subset}.json","r")
    data = json.load(f_json)
    f_json.close()
    
    df = pd.DataFrame(
        [[d["id"], d["question"], d["answers"]["a"], d["answers"]["b"], d["answers"]["c"], d["answers"]["d"], d["answers"]["e"], "|".join(d["correct_answers"]), str(d["nbr_correct_answers"])] for d in data],
        columns=[
            "id",
            "question",
            "answers.a",
            "answers.b",
            "answers.c",
            "answers.d",
            "answers.e",
            "correct_answers",
            "nbr_correct_answers"
        ]
    )

    df.to_csv(f"./csv/{subset}.csv", sep=';', index=False)
