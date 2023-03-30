[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
# Améliorez une application Web Python par des tests et du débogage
-------------------------------------------------------------------

## TABLE DES MATIERES
---------------------

* Introduction
* Pré-requis
* Installation
* Démarrage
* Rapport de test
* Rapport de performance
* Rapport Flake8

## INTRODUCTION
---------------

Ce projet consiste à améliorer l'application web de la société Gûdlft par des tests et du débogage. 
L'application permettra aux clubs d'inscrire des athlètes aux compétitions organisées au sein de la division.
Actuellement, les clubs gagnent des points via la mise en place et le déroulement des compétitions. Chaque club peut voir son solde actuel et échanger des points pour inscrire des athlètes à de futures compétitions, à raison d'un point par inscription. Chaque compétition aura un nombre limité d'inscriptions, et chaque club ne peut inscrire qu'un maximum de 12 athlètes.

### Cahier des charges:

*Les secrétaires des clubs de l'organisation pourront utiliser leur adresse électronique
pour se connecter et consulter la liste des compétitions à venir.
    * Ils pourront ensuite sélectionner une compétition et utiliser leurs points pour acheter des places.
    * Ils devraient voir un message confirmant le nombre de places achetées, ou un message indiquant que le concours est complet. Les points utilisés doivent être déduits du total précédent.
    * Ils ne doivent pas pouvoir réserver plus de places que celles disponibles ou
plus de 12 places dans une compétition (afin de garantir l'équité envers les autres clubs).
* Les secrétaires des clubs pourront se déconnecter
* Par souci de transparence, il devrait y avoir un tableau public, en lecture seule, des
totaux de points indiquant le nombre de points disponibles pour chaque club. Il ne
devrait pas être nécessaire de se connecter au site pour voir la page.
* Compte tenu du nombre d'utilisateurs potentiels, il faut réduire au minimum les temps de construction et de rendu ; il ne devrait pas falloir plus de 5 secondes pour récupérer une liste de compétitions, et pas plus de 2 secondes pour mettre à jour le total de points

### Informations complémentaires:

https://github.com/OpenClassrooms-Student-Center/Python_Testing


## Pré-requis
-------------

* Installer Python 3 : [Téléchargement Python 3](https://www.python.org/downloads/)
* Installer git : [Téléchargement Git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)


## Installation
---------------

### 1. Télécharger le projet sur votre répertoire local : 
```
git clone https://github.com/MarcOutt/Python_Testing.git
```
### 2. Mettre en place un environnement virtuel :
* Créer l'environnement virtuel: `python -m venv venv`
* Activer l'environnement virtuel :
    * Windows : `venv\Scripts\activate.bat`
    * Unix/MacOS : `source venv/bin/activate`
    
### 3. Installer les dépendances du projet
```
pip install -r requirements.txt
```


## Démarrage
* Lancer le script à l'aide de la commande suivante : `python server.py`
* Pour acceder au le site, veuillez entrer l'adresse ci-dessous dans le navigateur : http://127.0.0.1:5000/
* Afin de tester les différentes fonctionalités du site, connectez-vous avec un des 3 comptes: "john@simplylift.co", "admin@irontemple.com" et "kate@shelifts.co.uk".


## Rapport de test
-----------------
Les tests concernant les fonctionnalités de l'application ont été réalisé avec pytest, la couverture de test est de 98 %. Le rapport des tests peut être trouvé dans la branche QA du projet.


## Rapport de performance
--------------------------
Afin de nous assurez que le temps de chargement ne dépasse pas 5 secondes et que les mises à jour ne prennent pas plus de 2 secondes, un test de performance a été effectué avec Locust pour 6 utilisateurs.


## Rapport FLAKE8
------------------
L'application est conforme à la norme PEP8, elle ne présente aucune erreur dans le rapport flake8.

### Pour générer un nouveau rapport: 
* Ouvrir l'invite de commande ( se reporter à la rubrique installation)
* Lancer votre environnement virtuel ( se reporter à la rubrique installation)
* Rentrer le code suivant:

```bash
flake8 --exclude=.env/ --max-line-length=119 --format=html --htmldir=flake8-rapport
``` 

* Aller dans le dossier flake8-rapport
* Ouvrir le fichier index

