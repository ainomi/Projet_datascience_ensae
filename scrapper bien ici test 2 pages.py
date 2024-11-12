from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time
import re
import random

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

def extract_prices(url):
    """
    Utilise Selenium pour charger la page et extraire tous les prix des annonces.
    """
    try:
        driver.get(url)
        
        # Attendre que les annonces soient chargées
        wait = WebDriverWait(driver, 20)
        
        # Localiser les éléments contenant les prixdzqpdpkdpqdl
        prix_elements = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'span.ad-price__the-price')  # Ajuste ce sélecteur si nécessaire
        ))
        
        print(f"Nombre d'éléments de prix trouvés : {len(prix_elements)}")
        
        prices = []
        for prix_element in prix_elements:
            prix_text = prix_element.text.strip().replace('\xa0', ' ').replace(',', '.')
            print(f"Prix trouvé dans l'élément : {prix_text}")
            # Vérifier si le prix correspond au format attendu
            if re.match(r'^\d{1,3}(?: \d{3})* €$', prix_text):
                prices.append(prix_text)
                print(f"Prix cible ajouté : {prix_text}")
        
        if prices:
            return prices
        else:
            print("Aucun prix cible trouvé dans les annonces.")
            return []
        
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return []

def save_to_csv(prices, filename="prix_annonces.csv"):
    """
    Sauvegarde une liste de prix dans un fichier CSV.
    """
    if not prices:
        print("Aucun prix à enregistrer.")
        return
    with open(filename, "a", newline='', encoding='utf-8') as file:  # Utiliser 'a' pour ajouter
        writer = csv.writer(file)
        for price in prices:
            writer.writerow([price])
    print(f"{len(prices)} prix enregistré(s) dans {filename}")

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
    all_prices = []
    page_number = 1
    while page_number<3:
        print(f"\n--- Scraping de la page {page_number} ---")
        url = get_next_page_url(BASE_URL, page_number)
        print(f"URL de la page courante : {url}")
        
        prices = extract_prices(url)
        if not prices:
            print("Fin des résultats ou erreur rencontrée.")
            break
        else:
            all_prices.extend(prices)
            save_to_csv(prices)
        
        page_number += 1
        
        # Ajouter un délai aléatoire entre les requêtes pour éviter d'être détecté
        sleep_time = random.uniform(2, 5)
        print(f"Attente de {sleep_time:.2f} secondes avant la prochaine requête...")
        time.sleep(sleep_time)
    
    print(f"\nTotal des prix collectés : {len(all_prices)}")
    driver.quit()

if __name__ == "__main__":
    main()