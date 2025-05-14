

from fastapi import FastAPI
from pydantic import BaseModel
from newspaper import Article
import json
from typing import List, Optional
from fastapi.responses import JSONResponse

app = FastAPI(title="Web Article Scraper", version="1.0")

# Request model for input
class ScrapeRequest(BaseModel):
    url: str

# Response model for output
class ScrapeResponse(BaseModel):
    url: str
    title: str
    authors: List[str]
    publish_date: Optional[str]
    top_image: Optional[str]
    summary: Optional[str]
    keywords: List[str]
    text: str

@app.post("/scrape", response_model=ScrapeResponse)
async def scrape_article(request: ScrapeRequest):
    try:
        url = request.url
        article = Article(url)
        article.download()
        article.parse()

        # Optional: article.nlp() for keywords and summary
        try:
            article.nlp()
        except Exception:
            pass  # In case NLP fails

        data = {
            "url": url,
            "title": article.title,
            "authors": article.authors,
            "publish_date": article.publish_date.isoformat() if article.publish_date else None,
            "top_image": article.top_image,
            "summary": article.summary if hasattr(article, 'summary') else None,
            "keywords": article.keywords if hasattr(article, 'keywords') else [],
            "text": article.text
        }

        # Save to JSON file
        with open("scraped_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return JSONResponse(content=data, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
def root():
    return {"message": "✅ FastAPI Article Scraper is running. Visit /docs to test."}

