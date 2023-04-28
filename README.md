* Table of contents
  
  [_TOC_]

# SPQR_Deft-2013_pharmacologie

Les comptes rendus : [ici](./CompteRendu.md)

Le projet est divisé sur 3 tâches essentielles : 
- tâche 1 : la standardisation des questions
- tâche 2 : la création d'une base de données adaptée
- tâche 3 : la correction automatique 

# Tâche 1 : 

la standardisation des questions nécessite plusieurs étapes : 
- analyse préalable des structures des questions posées
- transformation des phrases intérrogatives en phrases affrimatives
- extraction des terms pharmacologiques (médicaux/chimiques)

## Analyse structurelle des questions [DONE]

La structure générale d'une question dans le questionnaire est divisée en 3 parties. La séparation entre ces parties est faite avec une 
virgule ",". Cela nous donne la forme suivante : 

[P_1],[P_2],[P_3]

Les questions du questionnaire ont les composants récurrents suivants : 

- [A]  les mots-clés linguistiques utilisés dans la formulation des questions sont : Parmi, donner, indiquer, cocher, on observe, quelle(s), laquelle(s), séléctionner
- [TF] les mots-clés linguistiques utilisés dans l'affrimation ou la négation sont : exacte(s), juste(s), inexacte(s) fausse(s), vraie(s)
- [1N] la spécification du nombre des réponses possibles est ouverte sauf dans le cas où il est précisé qu'il y qu'une réponse possible
- [IMP] l'indication du nombre des réponses possible peut-être faite d'une manière explicite ou implicite
- [KM,SenKM] l'information médicale dans la question est fournie sous deux formes : un mot-clé médical, une phrase complete avec des mot-clés médicaux
- Parfois, une partie [P_i] est divisé avec : ".",":","?"
- [NEG] phrase en négation


# Tâche 2 : 

la création d'une base de données adaptée.

- utiliser le training set pour contruire un corpus (AutoCorpus)
- utiliser des corpus externes (livre, siteweb,..etc)

## AutoCorpus 85% [DONE] 

La création d'un autoCorpus repose sur la réformulation des questions et leur concatination avec les réponses correspondantes.

Exemple : 

Parmi les bactéries suivantes, une seule ne peut généralement pas être responsable d'une méningite aiguë, laquelle?;Haemophilus influenzae;Streptococcus pneumoniae;Neisseria gonorrhoeae;Neisseria meningitidis;Mycobacterium tuberculosis;c;1

-> Neisseria gonorrhoeae est bactérie, une seule ne peut généralement pas être responsable d'une méningite aiguë.


### Le code proposé par Toufik 
Le code actuel permet de :
- extraire les termes médicaux et les stocke dans une liste 
- detecter et appliquer la négation à une phrase
- détecter masculin / féminin 
- reformuler (>85% des questions du training-set) types de questions et les concaténer avec les réponses. 

Pour plus de détails sur les types des questions, consulter le lien suivant : [ici](./team_TB/note.md)s

## Corpus externe [Julien] 


# Tâche 3 : [In progress]




