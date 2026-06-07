from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.news import fetch_headlines
from services.summarizer import summarize_articles
from models import Article, DigestResponse
import time

router = APIRouter(prefix="", tags=["News"])


@router.get("/headlines", response_model=list[Article])
async def get_headlines(
    topic: Optional[str] = Query(None, description="Category: business, entertainment, health, science, sports, technology"),
    count: int = Query(10, ge=1, le=20, description="Number of headlines to return")
):
    try:
        articles = await fetch_headlines(topic=topic, count=count)
        return articles
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/digest", response_model=DigestResponse)
async def get_digest(
    topic: Optional[str] = Query(None, description="Category: business, entertainment, health, science, sports, technology"),
    count: int = Query(10, ge=1, le=20, description="Number of articles to summarize")
):
    try:
        articles = await fetch_headlines(topic=topic, count=count)
        summary = await summarize_articles(articles, topic=topic)

        return DigestResponse(
            topic=topic,
            article_count=len(articles),
            summary=summary,
            articles=articles
        )
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    
@router.get("/cache", tags=["Meta"])
def get_cache_status():
    from services.news import _cache, CACHE_TTL_SECONDS
    status = {}
    for (topic, count), (timestamp, articles) in _cache.items():
        age_seconds = int(time.time() - timestamp)
        status[f"topic={topic}, count={count}"] = {
            "article_count": len(articles),
            "age_seconds": age_seconds,
            "expires_in_seconds": max(0, CACHE_TTL_SECONDS - age_seconds)
        }
    return {"cached_queries": status, "total": len(status)}