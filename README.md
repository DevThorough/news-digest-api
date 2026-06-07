# News Digest API

An AI-powered REST API that fetches top news headlines and generates a concise 
daily digest using Claude. Built with FastAPI, httpx, and the Anthropic SDK.

## Features

- Fetch live headlines by topic (technology, sports, business, and more)
- AI-generated news summaries via Claude
- In-memory caching to minimize API calls
- Auto-generated interactive docs via Swagger UI

## Tech Stack

- **FastAPI** — REST API framework
- **httpx** — Async HTTP client
- **Anthropic SDK** — Claude AI summarization
- **NewsAPI** — Live headline data
- **Pydantic** — Data validation

## Setup

### 1. Clone the repo and install dependencies
```bash
git clone https://github.com/yourusername/news-digest-api.git
cd news-digest-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add your API keys
Create a `.env` file in the project root:
NEWS_API_KEY=your_newsapi_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

### 3. Run the server
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive API explorer.

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/headlines` | Raw headlines, optionally filtered by topic |
| GET | `/digest` | AI-generated digest + headlines |
| GET | `/cache` | Current cache status |

## Example Requests

```bash
# Get top 5 technology headlines
curl "http://localhost:8000/headlines?topic=technology&count=5"

# Get a full AI digest on sports news
curl "http://localhost:8000/digest?topic=sports"

# Get a general digest with no topic filter
curl "http://localhost:8000/digest"
```

## Valid Topics

`business` · `entertainment` · `general` · `health` · `science` · `sports` · `technology`