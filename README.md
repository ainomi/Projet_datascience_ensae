# Projet DataScience ENSAE #
## Estimation du prix d'un bien immobilier à Paris selon ses caractéristiques ##
### Réalisé par Maxime Chansat, Anaïs Augé et Jules Hajjar

Ce projet a pour but de construire un ou plusieurs modèles pour estimer le prix d'un bien immobilier dans la ville de Paris. Par "bien immobilier", on entend un logement destiné principalement à l'habitation (comme un appartement, une maison...).
Afin d'obtenir des données d'annonces immobilières, nous avons procédé au webscraping du site suivant : https://www.bienici.com/. Il s'agit d'une plateforme immobilière créée par un consortium regroupant les principaux acteurs du secteur immobilier français (comme ORPI, La Forêt, Nexity, Century 21, Foncia...).
Le projet, sous la forme d'un repo GitHub, est composé d'un notebook nommé "main.ipynb" permettant de dérouler simplement le projet ainsi que d'un script Python nommé "scraping.py" correspondant au code du webscraping de Bien'ici.

Le scraping prenant un certain temps à réaliser sa tâche, il n'est pas exécuté dans le main.ipynb (il est appelé sous forme de commentaires), mais son code est bien entendu consultable dans "scraping.py".
De ce fait, un fichier intermédiaire "listings.csv", correspondant au résultat du scraping, est stocké sur le Datalab du SSP Cloud d'un des membres du groupe.

Afin de correctement exécuter le notebook, voici les prérequis :

- Disposer des packages : selenium, webdriver_manager, csv, time, random, os, pandas, numpy, re, collections, s3fs, geopy, functools, dill, matplotlib, scipy.stats, seaborn, folium, sklearn, xgboost. Ces packages peuvent être installés en exécutant la cellule d'installation des packages sur le notebook principal.
- Si vous êtes sur le SSP Cloud : il se peut que l'exécution du scraping produise une erreur en raison de l'OS du SSP Cloud. Ainsi, si c'est le cas pour vous, veuillez enlever les "#" devant les premières lignes dans le fichier "scraping.py".

Sources de données :

- Le site Bien'ici 
- Le service de géocodage de geopy
- Pour l'introduction sur le marché immobilier parisien : La Chambre des Notaires de Paris : https://paris.notaires.fr
