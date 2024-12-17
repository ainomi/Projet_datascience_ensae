import pandas as pd

#chemin_du_fichier = "/Users/anaisauge/Downloads/listings.csv"
df = pd.read_csv(listings.csv)
df.head()

pip install geopy

# Extraire la colonne contenant les informations sur les quartiers ou adresses
# En me basant sur le nom de la colonne, je vais essayer de cibler la bonne colonne
df_quartiers = df.iloc[:, 3]
# Afficher les premières valeurs de cette colonne pour vérifier
df_quartiers.head()

### EXTRAIRE LES COORDONNÉES GRAPHIQUES D'UNE LOCALISATION ###
import geopy
from geopy.geocoders import Nominatim
# Création d'un objet géocodeur Nominatim
geolocator = Nominatim(user_agent="my_geocoder")
# Géocodage d'une adresse
location = geolocator.geocode("75001 Paris 1er")
# Affichage des informations de localisation


### Créer une liste unique des quartiers/adresses ###
# Extraire la colonne contenant les quartiers/adresses
df_quartiers = df.iloc[:, 3]
# Créer une liste des adresses uniques
list_quartiers_uniques = df_quartiers.unique()
# Afficher les premières adresses uniques pour vérification
print(list_quartiers_uniques)  # Affiche les 10 premières adresses uniques
len(list_quartiers_uniques)


### PRENDRE *TOUTES* LES COORDONNÉES GRAPHIQUES ###
from geopy.geocoders import Nominatim
import time

# Créer un objet géocodeur Nominatim
geolocator = Nominatim(user_agent="my_geocoder")

# Fonction pour obtenir les coordonnées géographiques d'une adresse
def obtenir_coordonnees(adresse):
    try:
        location = geolocator.geocode(adresse, timeout=5)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Erreur pour {adresse}: {e}")
        return None, None

# Extraire seulement les premières adresses uniques
list_quartiers_uniques_3 = ['75003 Paris 3e', '75013 Paris 13e', '75010 Paris 10e'] # ENTRER À LA MAIN EN ATTENDANT
# Créer un dictionnaire pour stocker les adresses et leurs coordonnées
coordonnees_dict = {}

# Obtenir les coordonnées pour les 10 premières adresses
for adresse in list_quartiers_uniques_10:
    lat, lon = obtenir_coordonnees(adresse)
    coordonnees_dict[adresse] = (lat, lon)
    
    # Ajouter une pause pour éviter un blocage par le serveur
    time.sleep(1)  # Pause de 1 seconde entre les requêtes

# Afficher les coordonnées pour les 3 adresses
print("\nCoordonnées des 3 premières adresses :")
for adresse, coord in coordonnees_dict.items():
    print(f"Adresse: {adresse}, Latitude: {coord[0]}, Longitude: {coord[1]}")

### CREATION DE LA CARTE ###
pip install folium
import folium

# Coordonnées des adresses
coordonnees = [
    {"adresse": "75003 Paris 3e", "latitude": 48.864212, "longitude": 2.360936},
    {"adresse": "75013 Paris 13e", "latitude": 48.8290105, "longitude": 2.3636124},
    {"adresse": "75010 Paris 10e", "latitude": 48.876225, "longitude": 2.3595209},
]

# Initialiser la carte centrée sur Paris
carte = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Ajouter des points sur la carte pour les adresses avec coordonnées
for lieu in coordonnees:
    if lieu["latitude"] is not None and lieu["longitude"] is not None:
        folium.Marker(
            location=[lieu["latitude"], lieu["longitude"]],
            popup=lieu["adresse"],  # Texte affiché lorsqu'on clique sur le point
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(carte)

# Sauvegarder la carte dans un fichier HTML
carte.save("carte_paris_points.html")
print("Carte créée : carte_paris_points.html")
