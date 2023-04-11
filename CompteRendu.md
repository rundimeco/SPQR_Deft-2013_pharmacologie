

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
