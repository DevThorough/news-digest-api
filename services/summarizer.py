import anthropic
import os
from models import Article

async def summarize_articles(articles: list[Article], topic: str = None) -> str:
    
    # Format the articles into a readable list for the prompt
    headlines_text = ""
    for i, article in enumerate(articles, start=1):
        headlines_text += f"{i}. {article.title} ({article.source})\n"
        if article.description:
            headlines_text += f"   {article.description}\n"

    # Build the topic context for the prompt
    topic_context = f"about {topic}" if topic else "across various topics"

    # Write the prompt
    prompt = f"""You are a professional news editor writing a morning digest newsletter.

Here are today's top headlines {topic_context}:

{headlines_text}

Write a concise 3-4 sentence digest summarizing the most important themes and stories. 
Write in a neutral, informative tone as if addressing a general audience. 
Do not use bullet points — write in flowing prose only."""

    # Call the Anthropic API
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text
    except anthropic.AuthenticationError:
        raise ValueError("Invalid Anthropic API key. Check your .env file.")
    except anthropic.APIConnectionError:
        raise ValueError("Could not connect to Anthropic. Check your internet connection.")
    except anthropic.RateLimitError:
        raise ValueError("Anthropic rate limit hit. Wait a moment and try again.")