import httpx
import os
import time
from models import Article

NEWS_API_BASE_URL = "https://newsapi.org/v2/top-headlines"

_cache: dict = {}
CACHE_TTL_SECONDS = 900 

async def fetch_headlines(topic: str = None, count: int = 10) -> list[Article]:
    api_key = os.getenv("NEWS_API_KEY")

    # Check cache first
    cache_key = (topic, count)
    if cache_key in _cache:
        timestamp, cached_articles = _cache[cache_key]
        if time.time() - timestamp < CACHE_TTL_SECONDS:
            print(f"Cache hit for {cache_key}")
            return cached_articles
        
    print(f"Cache miss for {cache_key} — fetching from NewsAPI")

    # Build the query parameters
    params = {
        "apiKey": api_key,
        "country": "us",
        "pageSize": count,
    }

    # If a topic was provided, add it as a category
    if topic:
        params["category"] = topic

    # Make the async HTTP request
    try:    
        async with httpx.AsyncClient() as client:
            response = await client.get(NEWS_API_BASE_URL, params=params)
            response.raise_for_status()  # raises an error if the request failed
            data = response.json()
    except httpx.HTTPStatusError as e:
        raise ValueError(f"NewsAPI returned an error: {e.response.status_code}")
    except httpx.RequestError:
        raise ValueError("Could not connect to NewsAPI. Check your internet connection.")


    # Parse each article into our clean Article model
    articles = []
    for item in data.get("articles", []):
        article = Article(
            title=item.get("title", "No title"),
            source=item.get("source", {}).get("name", "Unknown"),
            url=item.get("url", ""),
            description=item.get("description")
        )
        articles.append(article)

    # Store in cache
    _cache[cache_key] = (time.time(), articles)
    
    return articles