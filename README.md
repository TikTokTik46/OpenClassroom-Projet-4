# OpenClassroom-Projet-4
Projet n°4 : Création d'un programme console Python pour la gestion de tournois d'échecs via le système suisse

Installation du programme :


Lancement et utilisation du programme :
Lancer l'executable python main.py via un interpréteur Python.
Choisir l'action souhaitée en tappant le chiffre correspondant puis en appuyant sur entré.

Génération des rapports Flake8 :
Ouvrer le terminal de commande et entrer les commande suivante en etant dans le dossier contenant le fichier main.py
flake8 controllers --format=html --htmldir=flake-report
flake8 views --format=html --htmldir=flake-report
flake8 models --format=html --htmldir=flake-report
