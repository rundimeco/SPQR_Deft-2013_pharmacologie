NB. On peut utiliser les subtitutions ([A],[TF]...etc) pour reclasser les questions d'une manière plus optimale. 

Dans un premier temps, on donne ci-dessous les differents cas de figures des questions : 

### Type 1 : 

- [DONE]:   [Parmi ][Spécification (nbr+exacte/fausse)][mot-clé médical]
- [DONE]:   [Parmi + mot-clé médical ][Spécification (nbr+exacte/fausse)]
- [DONE]:   [Parmi + Spécification (nbr+exacte/fausse)][mot-clé médical]
-   [Parmi ][Spécification (nbr+exacte/fausse) + mot-clé médical]
-   [Parmi + mot-clé médical][Spécification (nbr+exacte/fausse)+ mot-clé médical]
- [DONE]:   [Parmi + info médicale]
- [DONE]:   [Concernant + mot-clé médical][Spécification (nbr+exacte/fausse)]

NB: Il faut noter qu'il y a deux types des questions qui commencent par "Concernant" : 
- [Concernant + mot-clé médical][Spécification (nbr+exacte/fausse)] = rep[Elle est + info médical]
- [Concernant + info médical][Spécification (nbr+exacte/fausse)] = rep[info médical]

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