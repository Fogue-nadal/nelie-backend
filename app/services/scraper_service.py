import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL de base du site
BASE_URL = "https://www.boostcameroon.cm/"

# En-têtes pour simuler un vrai navigateur
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def get_page(url: str) -> BeautifulSoup | None:
    """
    Télécharge une page web et la prépare pour être analysée.
    Retourne None si la page est inaccessible.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Lève une erreur si code HTTP != 200
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Erreur lors de l'accès à {url} : {e}")
        return None

def scrape_budget_data() -> list[dict]:
    """
    Scrape les données budgétaires principales du site boostcameroun.
    Retourne une liste de dictionnaires contenant les données trouvées.
    """
    soup = get_page(BASE_URL)
    if not soup:
        return []

    results = []

    # Cherche tous les blocs de données budgétaires
    # (on affinera ces sélecteurs après analyse du site)
    sections = soup.find_all(["section", "div", "article"])

    for section in sections:
        text = section.get_text(strip=True)
        # Filtre les sections qui parlent de budget/finance
        if any(mot in text.lower() for mot in ["budget", "fcfa", "milliard", "dépense", "recette"]):
            results.append({
                "contenu": text[:500],  # Limite à 500 caractères
                "source": BASE_URL,
                "date_collecte": datetime.now().isoformat()
            })

    return results

def scrape_page_detail(url: str) -> dict:
    """
    Scrape le contenu détaillé d'une page spécifique.
    Utilisé pour aller chercher les détails d'un projet ou d'une dépense.
    """
    soup = get_page(url)
    if not soup:
        return {}

    # Extrait le titre de la page
    title = soup.find("h1") or soup.find("h2")
    title_text = title.get_text(strip=True) if title else "Sans titre"

    # Extrait le contenu principal
    content = soup.find("main") or soup.find("article") or soup.find("body")
    content_text = content.get_text(separator=" ", strip=True) if content else ""

    return {
        "titre": title_text,
        "contenu": content_text[:2000],  # Limite à 2000 caractères
        "url": url,
        "date_collecte": datetime.now().isoformat()
    }