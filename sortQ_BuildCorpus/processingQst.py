import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def MedTermDectection(phrase):
    # Charger le modèle BERT pré-entraîné pour la classification de phrases
    tokenizer = AutoTokenizer.from_pretrained("tblard/tf-allocine")
    model = AutoModelForSequenceClassification.from_pretrained("tblard/tf-allocine", from_tf=True)

    # Définir une phrase à tester
    # phrase = "Parmi les affirmations suivantes, une seule est fausse, indiquer laquelle."
    # phrase = "La douleur thoracique est un symptôme courant de l'infarctus du myocarde."

    # Tokenizer la phrase
    inputs = tokenizer(phrase, return_tensors="pt")

    # Faire passer les tokens dans le modèle pour obtenir les prédictions
    outputs = model(**inputs)
    predictions = torch.softmax(outputs.logits, dim=1).detach().numpy()[0]

    # La probabilité que la phrase contienne des termes scientifiques est la deuxième classe
    probabilite = predictions[1]

    # Si la probabilité est supérieure à un certain seuil, on considère que la phrase contient des termes scientifiques
    seuil = 0.43
    if probabilite > seuil:
        print("La phrase contient des termes scientifiques.")
        return True
    else:
        print("La phrase ne contient pas de termes scientifiques.")
        return False

import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

def isRequestWrongAns(question):
    # Tokenize the question
    tokens = word_tokenize(question)

    # Check if the question contains a keyword that indicates a wrong answer
    keywords = ["faux", "incorrect", "fausse", "mauvaise", "ne", "pas"]
    wrong_answer = False
    for keyword in keywords:
        if keyword in tokens:
            wrong_answer = True
            break
    return wrong_answer

# phrase = "Parmi les affirmations suivantes, une seule est fausse, indiquer laquelle."
# # phrase = "Parmi les bactéries suivantes, une seule ne peut généralement pas être responsable d'une méningite aiguë, laquelle?"
# # print(isRequestWrongAns(test))
# MedTermDectection(phrase)