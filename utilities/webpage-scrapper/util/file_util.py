import json
from model.scrapper_model import ScrapeResponse

def save_scraped_data(data: ScrapeResponse, path: str = "scraped_data.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data.dict(), f, ensure_ascii=False, indent=4)
