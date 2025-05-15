from newspaper import Article
from model.scrapper_model import ScrapeRequest, ScrapeResponse
import json
from typing import Optional
from datetime import datetime

class ArticleScraperService:
    def scrape(self, request: ScrapeRequest) -> ScrapeResponse:
        article = Article(request.url)
        article.download()
        article.parse()

        try:
            article.nlp()
        except Exception:
            pass  # NLP optional

        response = ScrapeResponse(
            url=request.url,
            title=article.title,
            authors=article.authors,
            publish_date=article.publish_date.isoformat() if article.publish_date else None,
            top_image=article.top_image,
            summary=article.summary if hasattr(article, 'summary') else None,
            keywords=article.keywords if hasattr(article, 'keywords') else [],
            text=article.text
        )

        return response
