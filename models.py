from pydantic import BaseModel
from typing import Optional

class Article(BaseModel):
    title: str
    source: str
    url: str
    description: Optional[str] = None

class DigestResponse(BaseModel):
    topic: Optional[str] = None
    article_count: int
    summary: str
    articles: list[Article]