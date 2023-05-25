# À propos

Ce répertoire contient les scripts que nous avons utilisé pour le challenge DEFT 2023 (https://deft2023.univ-avignon.fr/#format). Le but était de trouver toutes les réponses des questions d'un jeu de données fournit pour l'occasion par les organisateurs du DEFT (FrenchMedMCQA).

# DEFT2023

Nous souhaitons, étant donné une question de notre jeu de données, trouver toutes les réponses à cette question. Nous procédons par similarité. Pour une question, nous créons 5 listes de mot-clefs. Chacune de ces listes de mot-clefs est le résultat de la concaténation des mot-clefs de la question (Q) et des mot-clefs d'une des 5 réponses possibles à la question (R1,R2,R3,R4,R5). On a donc pour chaque question : 

- Q + R1
- Q + R2
- Q + R3
- Q + R4
- Q + R5

Pour chaque paire question / réponse (QR), on compare QR à chaque phrase d'un corpus de référence. Nous avons créés 5 corpus de référence au total, dont la création est détaillée dans notre article. Nous partons du principe que si une QR est vraie (c'est-à-dire que la réponse à une question donnée est vraie), alors on peut retrouver un élément équivalent dans l'un des corpus. Par test de similarité entre QR et nos corpus, nous regardons s'il existe des cas ou QR est très proche d'une des phrases du corpus Merck. Si c'est le cas, la similarité sera plus élevée et nous pourrrons dire que QR est vraie.

Trois méthodes ont été mises en place afin de retenir des QR vraies : 

- Méthode BYSEUIL : on récupère toutes les QR d'une question qui ont une similarité dans le corpus Merck au dessus d'un seuil donné ;
- Méthode BYMAX : on récupère seulement la QR d'une question qui a trouvé la plus haute similarité dans le corpus Merck ;
- Méthode BYFUSION : on récupère d'abord la QR d'une question avec la plus haute similarité dans le corpus Merck, puis toutes les QR avec une similarité supérieure à un seuil donné.

# Installation

Pour installer DEFT2023, vous devez avoir **Python 3.x** et **pip** d'installés. Clonez ce repértoire sur votre ordinateur. Ouvrez votre terminal et allez dans le dossier DEFT2023 (où se situe le script **main.py**). Une fois dans le dossier, lancez la commande suivante :

```
pip install -r requirements.txt
```

Additionnellement, il vous faut installer une ressource supplémentaire pour Spacy :

```
python -m spacy download fr_core_news_sm
```

# Utilisation

Le programme s'exécute en lignes de commandes uniquement. Nous avons générés préalablement divers fichiers disponibles dans ce répertoire.

## Récupération des mot-clefs 

La première étape est de récupérer tous les mot-clefs des paires QR ainsi que les mot-clefs des corpus de référence créés. Pour cela, il faut utiliser la commande suivante :

```
python main.py --keywords --data data/[DATA_HERE] --corpus input/[CORPUS_HERE]
```

Vous pouvez également lancer la commande avec seulement un **--data** ou un **--corpus**. Si les mot-clefs d'une ressource ont déjà été générés, la commande ne fait rien.

## Calcul des similarités

La prochaine étape est d'effectuer un calcul de similarité entre le corpus de mot-clefs issu des paires QR et les mot-clefs issu du corpus de référence. La commande est la suivante :

```
python main.py --task --data data/[DATA_HERE] --corpus input/[CORPUS_HERE]
```

Si vous avez bien générés au préalable les mot-clefs des paires et du corpus de référence que vous indiquez, vous devriez voir des fichiers se générer dans **output/Results/[DATA_HERE]/**. Il s'agit de fichiers CSV contenant l'id d'une question et les réponses estimées. Ces fichiers sont générés selon différents paramètres. Pour modifier les paramètres avec lesquels on génère nos sorties, il faut ligne 94 du script **scripts/task.py**. Si des fichiers de sortie ont déjà été générés pour les paires QR et le corpus de référence, la commande les remplace.

## Sortie des résultats

Nous pouvons maintenant récupérer l'Hamming score et l'Exact Match Ratio (EMR) de chaque fichier CSV. Pour se faire, exécutez la commande suivante :

```
python main.py --evalPrincipale --data data/[DATA_HERE]
```

Est renvoyé un fichier au format TXT dans **output/Results/**. Si vous souhaitez également effectuer la tâche annexe du DEFT 2023, lancez la commande suivante :

```
python main.py --evalAnnexe --data data/[DATA_HERE]
```

## Tri des résultats

Une fois les fichiers de résultats générés, nous pouvons renvoyer les meilleurs résultats à l'aide de la commande suivante :

```
python main.py --sortEval --resultFile output/Results/[RESULTFILE_HERE]
```

Où **resultFile** est le nom du fichier TXT généré à l'étape précédente. La console affiche ainsi un classement selon l'Hamming score et un classement selon l'EMR.
