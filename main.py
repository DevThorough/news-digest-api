from fastapi import FastAPI
from dotenv import load_dotenv
from routers.digest import router as digest_router

load_dotenv()  # loads your .env file

app = FastAPI(
    title="News Digest API",
    description="AI-powered daily news summaries",
    version="1.0.0"
)

app.include_router(digest_router)

@app.get("/")
def root():
    return {"message": "News Digest API is running!"}