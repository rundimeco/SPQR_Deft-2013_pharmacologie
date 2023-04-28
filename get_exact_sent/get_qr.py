import json
import string
import re

punctuation = string.punctuation.replace("'", '').replace('/', '').replace('.', '')

def remove_words(text):
    reg1='\s*parmi\sles\ssuivantes'
    reg2='laquelle|lesquelles'
    reg3='(indique|trouve|s.{1,2}lectionne|cite|pr.{1,2}cise|donne|coche|reteni)[zr]\s'
    reg4='(((\(*celle(\(*s\)*)*\)*|ou celles)\s*)+)*'
    reg5='(((l[\'’]|la|/|les|ou|\(|\))\s*)+)*'
    reg6='(([\.,;\:]*\s*(laquelle|lesquelles|lesquels)\s*\?|(\u00a0)*\?|[\:,\.;])+)*'
    words_to_remove = [r'\b'+reg3+''+reg4+''+reg5+'(qui\s((est|ou|sont|\)|\()\s*)+)*((proposition|affirmation|r.{1,2}ponse|affirmation)(\(*s\)*)*)*\sexacte(s)*\s*(\(*s\)*)*'+reg6,
                       r'\b((laquelle\sou|\(*ou lesquelles\)*|\(*lesquelle\(*s\)*\)*|laquelle|la ou)\s*)+((de ces|des)+\s(proposition(s)*|affirmations(s)*)(\ssuivantes)*)*\s((est|\(*sont\)*|\(*ou sont\)*)\s*)+exacte(s)*\s*(\(*s\)*)*('+reg1+')*'+reg6,
                       r'\b((quelle|quel)(\(*s*\)*)*\s)+(((est|\(*sont\)*)\s*)+)*(((la ou les|\(ou les\)|la|\(*les\)*|l\'|est l[\'’])\s)+)*(((la|ou|les|est|\(|\)|l\'|est l[\'’])\s*)+)*(celle(\(*s\)*)*)*(\squi\s(est\s*|\(*sont\)*)+)*(\shabituellement)*(r.{1,2}ponse|proposition|affirmation|caract.{1,2}ristique)*(\(*s\)*)*(\ssuivante\(*s\)*)*\s*exacte(s)*\s*(\(*s\)*)*('+reg1+')*'+reg6,
                       r'\bquelle\(*(s)*\)*\s(r.{1,2}ponse|proposition|affirmation|assertion)(\(*s\)*)*('+reg1+')*\s((est|\(*sont\)*)\s*)+exacte(s)*\s*(\(*s\)*)*'+reg6,
                       r'\bparmi\s(la ou les|la\s*\(les\)|les|ces)\s(proposition|affirmation|r.{1,2}ponse|assertion|propri.{1,2}t.{1,2})(\(*s\)*)*\s*(suivante\(*s\)*)*'+reg6,
                       r'((l\'|plusieurs|ou|une|seules|seule|\(|\)|certaine(\(*s\)*)*)\s*)+(((des|de|ces)\s)+((proposition|affirmation|r.{1,2}ponse|affirmation)(\(*s\)*)*)*(\ssuivantes\s)*)*\s*((\(*sont\)*|est)\s*)+\sexacte(s)*\s*(\(*s\)*)*'+reg6,
                       r''+reg6+'',
                       r'^\s+']
    
    words = text.lower().split()
    for substring in words_to_remove:
        text = re.sub(substring,'',text.lower())
    return text

def remove_punctuation(text):
    clean_text = ''.join(char for char in text if char not in punctuation)
    return clean_text

with open('questions.json', 'r') as file_in:
    qr = json.load(file_in)

question_reponse = ""
for phrase in qr:
    question = phrase['question']
    choix = phrase['answers']
    reponses = phrase['correct_answers']
    
    if ' exacte' in question:
       for reponse in reponses:
           qst=remove_words(question)
           question_reponse += qst[0:1].upper()+ qst[1:]+' ' +choix[reponse][0].lower() + choix[reponse][1:] + "\n"
with open("QR.txt", "w") as file_out:
    file_out.write(question_reponse)

print("Extraction terminée (résultat stocké dans le fichier QR.txt)")
