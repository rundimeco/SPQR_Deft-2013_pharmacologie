# Résumé des travaux effectués

Dans le but des corriger de manière automatique le QCM. 
Nous avons envisagé la méthodologie suivante : 

Nous avons commencé par analysé la structure des questions et de proposer 
une classification aux types des questions possibles.
Cela est pour but de les standardiser sous forme des phrases qui comprennent les questions avec ces réponses et gérer les négations. Ces phrases sont utilisées par la suite pour former une première base de données. Cette dernière est de la forme : 


V_1(i),..,V_n(i),B_1(i,j),..,B_m(i,j);Q(i) + R_j(i) pour j=1:5 et i=1:N 

où N est le nombre de questions dans la base de données et (n,m) les nombre des termes médicaux trouvés dans  Q(i) et R_j(i), respectivement.

## Méthodologie de résolution 

### Test de similarité 
- récupérer les termes médicaux de la question V_1(i),..,V_n(i)
- récupérer pour chaque réponse possible R(i) les termes médicaux B_1(i,j),..,B_m(i,j)
- reformulation sous forme d'une phrase Q(i)+R_j(i)= P(i,j)
- chercher les phrases E(k) les plus similaires dans la base de données en terme de liste des termes médicaux
- appliquer un test de similarité entre les phrases P(i,j) et E(k)

## Classification des questions :

NB. On peut utiliser les subtitutions ([A],[TF]...etc) pour reclasser les questions d'une manière plus optimale. 

Dans un premier temps, on donne ci-dessous les differents cas de figures des questions : 

### Type 1 : 

- [DONE]:   [Parmi ][Spécification (nbr+exacte/fausse)][mot-clé médical]
- [DONE]:   [Parmi + mot-clé médical ][Spécification (nbr+exacte/fausse)]
- [DONE]:   [Parmi + Spécification (nbr+exacte/fausse)][mot-clé médical]
- [DONE]:   [Parmi ][Spécification (nbr+exacte/fausse) + mot-clé médical]
- [DONE]:   [Parmi + mot-clé médical][Spécification (nbr+exacte/fausse)+ mot-clé médical]
- [DONE]:   [Parmi + info médicale]
- [DONE]:   [Concernant + mot-clé médical][Spécification (nbr+exacte/fausse)]

NB: Il faut noter qu'il y a deux types des questions qui commencent par "Concernant" : 
- [DONE]:   [Concernant + mot-clé médical][Spécification (nbr+exacte/fausse)] = rep[Elle est + info médical]
- [DONE]:   [Concernant + info médical][Spécification (nbr+exacte/fausse)] = rep[info médical]

Il va falloir penser à les traiter séparément.

### Type 2 : 

- [Cocher + Spécification (nbr+exacte/fausse) + ./: + mot-clé médical ]
- [info médicale + . + Cocher + Spécification (nbr+exacte/fausse) ]
- [Cocher + info médicale ]

### Type 3 : 

- [Indiquer + Spécification (nbr+exacte/fausse) + ? + mot-clé médical ]
- [Indiquer + info médicale ]
- [info médicale + . + Indiquer + Spécification (nbr+exacte/fausse) ]

### Type 4 : 

- [info médicale][On observe]
- [info médicale][On observe + info médicale 2]

### Type 5 : 

- [DONE]: [info médicale]
- [DONE]: [mot-clé médical]
- [Spécification genre/type/context (mot-clé médical)][info médicale]
- [context (mot-clé médical) + . + info médical]

### Type 6 : 

- [Quelle + 1N IMP + NEG info médical ]
- [Quelle + Spécification (exacte/fausse) + ? + info médicale]
- [Quelle + info médicale]
- [Quelle + Spécification (vraie(s)/fausse(s))+ mot-clé médical]
- [Quelle + Spécification (vraie(s)/fausse(s))][mot-clé médical]