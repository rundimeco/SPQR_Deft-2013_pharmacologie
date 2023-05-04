# Introduction

Nous souhaitons, étant donné une question de notre jeu de données, trouver toutes les réponses à cette question. Nous procédons par similarité. Pour une question, nous créons 5 listes de mots clefs. Chacune de ces listes de mots clefs est le résultat de la concaténation des mots clefs de la question (Q) et des mots clefs d'une des 5 réponses possibles à la question (Ra,Rb,Rc,Rd,Re). On a donc pour chaque question : 

- Q + Ra
- Q + Rb
- Q + Rc
- Q + Rd
- Q + Re

Pour chaque liste de mots clefs question/réponse (QR), on compare QR à chaque phrase d'un corpus de référence, ou plutôt aux mots clefs de chaque phrases d'un corpus de référence. Le corpus de référence de base est le corpus Merck, que nous avons scrappé depuis internet et découpé en une liste de phrases. Pour chaque phrase, on a créé une liste de mots clefs contenant tous les mots clefs de cette phrase. Ce sont ces listes de mots clefs que nous comparons à QR.

Nous partons du principe que si un QR est vrai (c'est-à-dire que la réponse à une question donnée est vraie), alors on peut retrouver un élément équivalent dans le corpus Merck. Par test de similarité entre QR et le corpus Merck, nous regardons s'il existe des cas ou QR est très proche d'une des phrases du corpus Merck. Si c'est le cas, la similarité sera plus élevée, on nous pourrrons dire que QR est vrai.

Deux méthodes ont été choisies pour le moment afin de retenir des QR vraies : 

- méthode 1 : on définit un seuil (par exemple 0.8). Pour tout QR lié à une question, s'il existe une phrase du manuel Merck pour laquelle ce QR a une similarité supérieure ou égale au seuil (0.8), alors on ajoute ce QR à la liste des bonnes réponse pour la question.
- méthode 2 : on récupère seulement le QR qui a trouvé la plus haute similarité dans le corpus Merck.

# Description des éléments du programme

Retrouvez ci-dessous les spécificités de chaque élément du programme créé.

## data

Contient les datasets "train.csv" et "dev.csv" sur lesquels nous souhaitons réaliser notre évaluation.

## input

Contient tous les fichiers d'input, à savoir :

- le manuel Merck, utilisé comme base de notre corpus de référence
- le corpus "train" reformulé, qui agit comme complément du corpus Merck
- diverses listes de "tri", c'est-à-dire des listes de mots jugés indésirables (qu'on souhaite ne pas prendre en compte lors de nos futures analyses)

## output

Contient plusieurs répertoires :

- Dataset : contient les fichiers de sortie après nettoyage du data qu'on souhaite analyser (eg : si on souhaite analyser "train.csv", on aura dans ce répertoire de sortie un fichier au format json comprenant pour chaque question toutes les possibles listes de mots clefs en fonction des réponses : mots clefs question + mots clefs réponse a, mots clefs question + mots clefs réponse b, ...)
- Merck : contient les fichiers de sortie correspondant au corpus créé à partir du corpus Merck (une liste de phrase et une liste de listes de mots clefs)
- Results : contient un sous répertoire par sortie différente, comprenant des fichiers csv correspondant au format de sortie requis par le DEFT 2023, pouvant être évalués. On en a une multitude à chaque fois car on teste plusieurs paramètres en simultané, afin d'ensuite faire un tri et ne retenir que les sorties avec les meilleurs résultats.

## scripts

Contient les scripts utilisés afin de réaliser ce programme. On retrouve un script propre au nettoyage du dataset, un script propre à la création d'un corpus de référence, un script comprenant la création des fichiers de résultats et un script contenant toutes les fonction créées et utilisées.

# Mode d'emploi du programme

Ce programme a été conçu pour s'exécuter en lignes de commande. Son mode de fonctionnement est simple : on choisit un dataset sur lequel on veut travailler ("train.csv" ou "dev.csv"), une liste de tri (contenues dans "input/listesTri") et la tâche que l'on souhaite réaliser. Pour le moment nous avons deux tâches, que nous abordons ci-après.

## Tâche de création des ressources

Notre travail consiste à comparer deux listes de mots clefs. Pour cela, nous devons créer ces listes de mots clefs : une pour le data d'entrée ("train.csv" ou "dev.csv") et une pour le corpus de référence (manuel Merck). Nous ne connaissons pas de liste de vocabulaire médical assez exhaustive pour comprendre tous les termes médicaux trouvés dans notre data d'entrée ou dans notre corpus de référence. Nous décidons donc de procéder à une approche différente : au lieu de répertorier les tecnolectes médicaux, nous listons les mots communs du français, qui ne sont pas propres à la médecine. Pour chaque question (ou pour chaque phrase), pour chaque mot de cette question (ou phrase), si ce mot est dans la liste des mots communs du français, on ne l'ajoute pas dans notre liste de mots clefs.

Nous réalisons cette tâche sur le data d'entrée et sur le corpus de référence avec la même liste de mots communs à chaque fois. La commande pour exécuter cette tâche est la suivante : 



## Tâche de création des fichiers de résultat

# Questions

est ce que ça vaut le coup de changer de métrique ?
j'ai plusieurs outputs proposés par les membres du projet dont le but est de répondre aux questions du train. Je les teste tous ou un seul suffit, vu qu'ils font tous la même tâche au final ?
fusionner BYMAX et BYSEUIL : comment faire ?
