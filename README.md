# Paris Real Estate Price Prediction

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-FF8000?logo=jupyter)
![Selenium](https://img.shields.io/badge/Selenium-WebScraping-43B02A?logo=selenium)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-XGBoost%20%7C%20Scikit--Learn-yellow)

**Authors**: Maxime Chansat, Anaïs Augé, and Jules Hajjar

## 📖 Overview
This project aims to build predictive machine learning models to estimate the price of residential real estate properties (apartments, houses, etc.) in Paris based on their features.

To train these models, we built a custom web scraper to collect real estate listings from [Bien'ici](https://www.bienici.com/), a major French real estate platform created by a consortium of key industry players (such as ORPI, La Forêt, Nexity, Century 21, and Foncia).

## 🗂️ Project Structure
The repository consists of two core components:
- `main.ipynb`: The primary Jupyter Notebook walking through the entire data science pipeline (Data Exploration, Feature Engineering, Modeling, and Evaluation).
- `scraping.py`: The Python web scraping script built on top of Selenium to extract real estate listings.

> **Note**: For privacy and legal reasons, the pre-scraped dataset is not hosted online. You must execute `scraping.py` beforehand to generate the `listings.csv` dataset required for the main notebook pipeline to run.

## ⚙️ Prerequisites & Installation

To run the notebook and scripts, you need the following Python packages:
- **Data Manipulation & Visualization**: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`
- **Machine Learning**: `scikit-learn`, `xgboost`
- **Web Scraping**: `selenium`, `webdriver_manager`, `chromedriver-autoinstaller`
- **Geocoding & Cloud Services**: `geopy`, `folium`, `s3fs`
- **Utilities**: `dill`

You can install all required dependencies easily using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## 🚀 Usage Guidelines & Known Issues

### 1. Web Scraping (`scraping.py`)
**This script must be executed first** to generate the working dataset.
- **SSP Cloud Users**: Running Selenium on the SSP Cloud OS might produce environmental errors. If you face issues, please follow the commented bypass instructions at the very beginning of the `scraping.py` file.

### 2. Geocoding Constraints (`geopy`)
- If executing on **SSP Cloud**, you may experience timeout exceptions during bulk geocoding requests with `geopy`.
- **Solution**: We highly recommend running the pipeline locally using an IDE such as VSCode or Jupyter on your machine to avoid these cloud-related request timeouts.

## 📊 Data Sources
- **Real Estate Listings**: [Bien'ici](https://www.bienici.com/)
- **Address Geocoding**: `geopy` Python library
- **Paris Market Context**: [La Chambre des Notaires de Paris](https://paris.notaires.fr)

## ⚠️ Disclaimer
**Data Usage Limitation**: The authors are not responsible for the extracted data used in this project. This scraper and pipeline are provided strictly for academic and educational purposes. When utilizing the scraper, ensure you adhere to the target website's Terms of Service and use the tool responsibly.

---
*This codebase was developed as an academic Data Science project at [ENSAE Paris](https://www.ensae.fr/).*
