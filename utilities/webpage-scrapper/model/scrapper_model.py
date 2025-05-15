from pydantic import BaseModel
from typing import List, Optional

class ScrapeRequest(BaseModel):
    url: str

class ScrapeResponse(BaseModel):
    url: str
    title: str
    authors: List[str]
    publish_date: Optional[str]
    top_image: Optional[str]
    summary: Optional[str]
    keywords: List[str]
    text: str
