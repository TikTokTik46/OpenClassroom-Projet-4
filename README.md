# OpenClassroom-Projet-4
Projet n°4 : Création d'un programme console Python pour la gestion de tournois d'échecs via le système suisse

<u>Installation du programme</u> :
<br/>Pour installer le programme télécharger le fichier ZIP depuis GitHUB
<br/>https://github.com/TikTokTik46/OpenClassroom-Projet-4.git
<br/>Créer un nouveau dossier et dezipper le contenu telecharger dans ce dossier.
<br/>Créer un environnement virtuel dans ce dossier et entrer la commande suivante dans le terminal de commande (en se placant dans le dossier correspondant et en activant l'environnement virtuel).
<br/>- pip install -r requirements.txt


<u>Lancement et utilisation du programme</u> :
<br/>Lancer l'executable python main.py via un interpréteur Python.
<br/>Choisir l'action souhaitée du menu principale en tappant le chiffre correspondant puis en appuyant sur entrée. Suivre les indications dans le terminal pour utiliser le programme.

<u>Génération des rapports Flake8</u> :
<br/>Ouvrir le terminal de commande et entrer les commande suivante en etant dans le dossier contenant le fichier main.py
<br/> - flake8 controllers --format=html --htmldir=flake-report --max-line-length 119
<br/> - flake8 views --format=html --htmldir=flake-report --max-line-length 119
<br/> - flake8 models --format=html --htmldir=flake-report --max-line-length 119
