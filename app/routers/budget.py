from fastapi import APIRouter, HTTPException
from app.services.scraper_service import scrape_budget_data, scrape_page_detail

router = APIRouter(prefix="/budget", tags=["Budget"])

@router.get("/scrape")
def scrape_budget():
    """
    Lance le scraping du site boostcameroon et retourne les données collectées.
    """
    data = scrape_budget_data()
    if not data:
        raise HTTPException(
            status_code=503,
            detail="Impossible de récupérer les données. Site inaccessible."
        )
    return {
        "status": "success",
        "nombre_resultats": len(data),
        "donnees": data
    }

@router.get("/scrape/page")
def scrape_page(url: str):
    """
    Scrape le contenu d'une page spécifique de boostcameroun.
    Exemple : /budget/scrape/page?url=https://www.boostcameroon.cm/...
    """
    if "boostcameroon" not in url:
        raise HTTPException(
            status_code=400,
            detail="URL non autorisée — uniquement boostcameroon.cm"
        )
    data = scrape_page_detail(url)
    if not data:
        raise HTTPException(status_code=503, detail="Page inaccessible")
    return data