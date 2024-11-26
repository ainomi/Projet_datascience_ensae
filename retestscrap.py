#!/usr/bin/env python3

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import re
import random
import os

# URL de base de la recherche
BASE_URL = "https://www.bienici.com/recherche/achat/paris-75000?tri=publication-desc"

# Configurer les options de Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')  # Exécuter en arrière-plan sans interface graphique
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--lang=fr-FR')  # Définir la langue en français
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                            "AppleWebKit/537.36 (KHTML, comme Gecko) "
                            "Chrome/112.0.0.0 Safari/537.36")

# Initialiser le WebDriver avec webdriver-manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def extract_listings(url, starting_id):
    """
    Utilise Selenium pour charger la page et extraire les informations de chaque annonce.
    """
    try:
        driver.get(url)

        # Attendre que les annonces soient chargées
        wait = WebDriverWait(driver, 20)

        # Trouver tous les conteneurs d'annonces
        listings = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'div.adOverview.ad-overview-gallery__ad-overview')  # Sélecteur ajusté
        ))
        

        data = []
        listing_id = starting_id  # Commencer l'ID à partir du starting_id

        for listing in listings:
            # Extraire les données requises de chaque annonce
            try:
                # Extraire l'ID de l'annonce
                ad_id = listing.get_attribute('data-realestateadid')
                if not ad_id:
                    ad_id = f"custom_id_{listing_id}"  # Fallback si l'attribut n'est pas trouvé

                # Extraire le titre complet (type, pièces, surface)
                try:
                    title_element = listing.find_element(By.CSS_SELECTOR, 'span.ad-overview-details__ad-title--small')
                    title_text = title_element.text.strip()  # Exemple : "Appartement 5 pièces 97 m²" ou "Studio 30 m²"
                    
                except Exception as e:
                    print(f"Erreur lors de l'extraction du titre : {e}")
                    title_text = ""

                # Initialiser les variables avec 'NaN'
                property_type = "NaN"
                rooms = "NaN"
                area = "NaN"

                # Vérifier le type de bien et extraire les informations en conséquence
                if "pièce" in title_text.lower():
                    # Format avec nombre de pièces, par exemple "Appartement 5 pièces 97 m²"
                    parts = title_text.split()
                    try:
                        property_type = parts[0]  # "Appartement", "Maison", "Duplex", etc.
                        # Trouver l'index de "pièce" ou "pièces"
                        if "pièce" in parts:
                            rooms_index = parts.index("pièce")
                        elif "pièces" in parts:
                            rooms_index = parts.index("pièces")
                        else:
                            rooms_index = -1  # Non trouvé

                        if rooms_index > 0:
                            rooms = parts[rooms_index - 1]
                        else:
                            rooms = "NaN"

                        # La surface devrait être le mot après "pièce(s)"
                        if rooms_index + 2 < len(parts):
                            area_str = parts[rooms_index + 1]  # Par exemple, "97"
                            # Vérifier si le prochain mot est "m²"
                            if parts[rooms_index + 2].lower().startswith("m²"):
                                area = area_str
                            else:
                                area = "NaN"
                        else:
                            area = "NaN"
                    except (ValueError, IndexError) as e:
                        print(f"Erreur lors de l'extraction avec pièces : {e}")
                        property_type = parts[0] if len(parts) > 0 else "NaN"
                        rooms = "NaN"
                        area = "NaN"
                else:
                    # Format sans nombre de pièces, par exemple "Studio 30 m²"
                    parts = title_text.split()
                    try:
                        property_type = parts[0]  # "Studio", "Duplex", etc.
                        # Supposer que la surface est le dernier élément
                        if len(parts) >= 2:
                            area_str = parts[-2]  # Avant "m²"
                            if parts[-1].lower().startswith("m²"):
                                area = area_str
                            else:
                                area = "NaN"
                        else:
                            area = "NaN"
                    except (ValueError, IndexError) as e:
                        print(f"Erreur lors de l'extraction sans pièces : {e}")
                        property_type = "NaN"
                        rooms = "NaN"
                        area = "NaN"

                # Extraire la localisation
                try:
                    location_element = listing.find_element(By.CSS_SELECTOR, 'span.ad-overview-details__address-title--small')
                    location_text = location_element.text.strip()  # Exemple : "75014 Paris 14e (Jean Moulin - Porte d'Orléans)"
                except Exception as e:
                    print(f"Erreur lors de l'extraction de la localisation : {e}")
                    location_text = "NaN"

                # Extraire le prix
                try:
                    price_element = listing.find_element(By.CSS_SELECTOR, 'span.ad-price__the-price')
                    price_text = price_element.text.strip().replace('\xa0', ' ').replace(',', '.')
                except Exception as e:
                    print(f"Erreur lors de l'extraction du prix : {e}")
                    price_text = "NaN"

                # Stocker les données dans un dictionnaire
                data.append({
                    'ID': ad_id,
                    'Type': property_type,
                    'Rooms': rooms,
                    'Location': location_text,
                    'Area': area,
                    'Price': price_text
                })

                listing_id += 1

            except Exception as e:
                print(f"Erreur lors de l'extraction des données de l'annonce : {e}")
                continue

        if data:
            return data, listing_id
        else:
            print("Aucune annonce trouvée.")
            return [], listing_id

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return [], starting_id

def save_to_csv(data, filename="listings.csv"):
    """
    Sauvegarde une liste de dictionnaires dans un fichier CSV.
    """
    if not data:
        print("Aucune donnée à enregistrer.")
        return
    # Vérifier si le fichier existe pour écrire les en-têtes ou non
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline='', encoding='utf-8') as file:
        fieldnames = ['ID', 'Type', 'Rooms', 'Location', 'Area', 'Price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for entry in data:
            writer.writerow(entry)
    

def get_next_page_url(current_url, next_page_number):
    """
    Génère l'URL de la page suivante en ajoutant le paramètre 'page'.
    """
    if next_page_number == 1:
        return current_url
    else:
        if '?' in current_url:
            return f"{current_url}&page={next_page_number}"
        else:
            return f"{current_url}?page={next_page_number}"

def main():
    all_data = []
    page_number = 1
    listing_id = 1  # Initialiser l'ID de l'annonce
    while True:  # Vous pouvez augmenter le nombre de pages ici
        
        url = get_next_page_url(BASE_URL, page_number)
       

        data, listing_id = extract_listings(url, listing_id)
        if not data:
            print("Fin des résultats ou erreur rencontrée.")
            break
        else:
            all_data.extend(data)
            save_to_csv(data)

        page_number += 1

        # Ajouter un délai aléatoire entre les requêtes pour éviter d'être détecté
        sleep_time = random.uniform(2, 5)
        
        time.sleep(sleep_time)

    print(f"\nTotal des annonces collectées : {len(all_data)}")
    driver.quit()

if __name__ == "__main__":
    main()
