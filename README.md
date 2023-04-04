# SPQR_Deft-2013_pharmacologie


## Classification des questions 

La structure générale d'une question dans le questionnaire est divisée en 3 parties en générale. La séparation entre ces parties est faite avec une 
virgule ",". Cela nous donne la forme suivante : 

[P_1],[P_2],[P_3]

### Analyse structurelle des questions : 
Les questions du questionnaire ont les composants récurrents suivants : 

- [A]  les mots-clés linguistiques utilisés dans la formulation des questions sont : Parmi, donner, indiquer, cocher, on observe, quelle(s), laquelle(s), séléctionner
- [TF] les mots-clés linguistiques utilisés dans l'affrimation ou la négation sont : exacte(s), juste(s), inexacte(s) fausse(s), vraie(s)
- [1N] la spécification du nombre des réponses possibles est ouverte sauf dans le cas où il est précisé qu'il y qu'une réponse possible
- [IMP] l'indication du nombre des réponses possible peut-être faite d'une manière explicite ou implicite
- [KM,SenKM] l'information médicale dans la question est fournie sous deux formes : un mot-clé médical, une phrase complete avec des mot-clés médicaux
- Parfois, une partie [P_i] est divisé avec : ".",":","?"
- [NEG] phrase en négation

NB. On peut utiliser les subtitutions ([A],[TF]...etc) pour reclasser les questions d'une manière plus optimale. 

Dans un premier temps, on donne ci-dessous les differents cas de figures des questions : 

### Classe 1 : 

-   [Parmi ][Spécification (nbr+exacte/fausse)][mot-clé médical]
-   [Parmi + mot-clé médical ][Spécification (nbr+exacte/fausse)]
-   [Parmi + Spécification (nbr+exacte/fausse)][mot-clé médical]
-   [Parmi ][Spécification (nbr+exacte/fausse) + mot-clé médical]
-   [Parmi + mot-clé médical][Spécification (nbr+exacte/fausse)+ mot-clé médical]
-   [Parmi + info médicale]

### Classe 2 : 

- [Cocher + Spécification (nbr+exacte/fausse) + ./: + mot-clé médical ]
- [info médicale + . + Cocher + Spécification (nbr+exacte/fausse) ]
- [Cocher + info médicale ]

### Classe 3 : 

- [Indiquer + Spécification (nbr+exacte/fausse) + ? + mot-clé médical ]
- [Indiquer + info médicale ]
- [info médicale + . + Indiquer + Spécification (nbr+exacte/fausse) ]

### Classe 4 : 

- [info médicale][On observe]
- [info médicale][On observe + info médicale 2]

### Classe 5 : 

- [info médicale]
- [mot-clé médical]
- [Spécification genre/type/context (mot-clé médical)][info médicale]
- [context (mot-clé médical) + . + info médical]

### Classe 6 : 

- [Quelle + 1N IMP + NEG info médical ]
- [Quelle + Spécification (exacte/fausse) + ? + info médicale]
- [Quelle + info médicale]
- [Quelle + Spécification (vraie(s)/fausse(s))+ mot-clé médical]
- [Quelle + Spécification (vraie(s)/fausse(s))][mot-clé médical]



**COMPTE RENDU RÉUNION 27 mars 2023**

-Présentation de la classification effectuée par Toufik (il ajoutera le fichier sur GitHub dans le courant de la semaine)
-Présentation de la transformation des questions et des réponses correctes, par le biais des conditions, en phrases pour construction de corpus auto-suffisant - tâche effectuée par Corina (à ajouter le code sur GitHub dans le courant de la semaine)
-Le but est de combiner ces deux tâches pour aboutir à un corpus auquel on ajoutera ensuite les annales fournies. 


-Discussion autour du papier disponible dans le readme => L’équipe des organisateurs a déjà travaillé dessus en utilisant le MedBERT anglais et le BERT français = > le MedBERT anglais s’est avéré plus efficace que le BERT généralisé en français, le score de précision est calculé avec deux métriques : Hamming et EMR. Il est d’approximativement 15% de précision avec EMR et 36-38 avec Hamming (cf. Tableau 2 page 4 papier fourni) :

-Proposition de Caroline suite à l’analyse du tableau : utiliser d’autres métriques pour mesurer les résultats. 
-Conclusion de l’analyse du papier : si Ibtihel, Nour et Oumaima n’ont pas encore travaillé sur les BERTs il faudrait abandonner la tâche car elle a déjà été effectuée par l’équipe. 
-La construction d’un corpus externe ne fonctionne pas non plus, l’équipe a utilisé un corpus wikipedia et un HAL, cela n’a pas donné de résultats (pour plus de précisions consulter le papier)

Nouvelles tâches pour lundi 3 avril à 14h :

1. Andreea => Demander à sont contact en pharmacologie s’il y une similarité entre les questions et les réponses (approche globale sans analyse précise)

2. Toufik   => avancer sur la classification et mettre ensemble son travail avec celui de Corina (il sera expliqué plus en détail sur GitHub)

3. Corina => avancer sur la transformation des questions et réponses correctes en propositions valides. 

4. Gaël et Julien => méthode de similarité entre les question 

5. Laurie => Contacter l’équipe de DEFT 2023 pour des questions concernant le règlement (on n’a pas la certitude des libertés dont on dispose dans la constitution du corpus)

** COMPTE RENDU Réunion 3 avril 2023**

Au niveau de la similarité Caroline et Julien n’ont pas obtenu des résultats concluants, mais pour l’instant cette tâche reste inachevée. Pourtant cela nous amène à réfléchir à 3 types de corpus qu’on pourra concaténer :

1. Le corpus issus des questions et des réponses sur lequel je suis en train de travailler
2. Le livre proposé par Toufik (cf. GitHub) qui reprend des notions clés des questions et des réponses 
3. Un corpus complémentaire qui sera défini cette semaine 

La prochaine réunion aura lieu le 10 avril à 14h.

Tâches à achever avant la réunion : 

1. Réfléchir et implémenter des stratégies concrètes de similarité => Toufik, Julien
2. Créer un corpus complémentaire => Nour, Oumaima
3. Enrichir la classification de Toufik => Nour
4. Travailler sur une ontologie avec MESH => Ibtihel
5. Annotation des entités médicales par suffixes et préfixes pour création de groupes => Caroline 
6. Finaliser construction du corpus à partir des questions et réponses => Corina, Caroline 
7. Analyser les données manuellement et faire tableau pour montrer la présence ou absence de similarités & réaliser un dictionnaire avec les abréviations et leur contenu correspondant => Andrea, Laurie
