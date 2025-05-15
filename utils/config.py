"""
Configuration settings for the news aggregator.
"""

# API key for NewsAPI.org (replace with your own key)
NEWS_API_KEY = "YOUR_API_KEY_HERE"  # Get your free API key from https://newsapi.org/register

# News categories
CATEGORIES = [
    "general",
    "politics",
    "business",
    "sports",
    "entertainment",
    "technology",
    "health",
    "science"
]

# News sources with their respective URLs for API and scraping
NEWS_SOURCES = {
    "the-hindu": {
        "name": "The Hindu",
        "api_id": "the-hindu",
        "scrape_url": "https://www.thehindu.com/",
        "categories": {
            "general": "/news/national/",
            "politics": "/news/national/politics/",
            "business": "/business/",
            "sports": "/sport/",
            "entertainment": "/entertainment/",
            "technology": "/sci-tech/technology/",
            "health": "/sci-tech/health/",
            "science": "/sci-tech/science/"
        }
    },
    "times-of-india": {
        "name": "Times of India",
        "api_id": "the-times-of-india",
        "scrape_url": "https://timesofindia.indiatimes.com/",
        "categories": {
            "general": "/india/",
            "politics": "/india/politics/",
            "business": "/business/",
            "sports": "/sports/",
            "entertainment": "/entertainment/",
            "technology": "/technology/",
            "health": "/life-style/health-fitness/",
            "science": "/science/"
        }
    },
    "indian-express": {
        "name": "Indian Express",
        "api_id": "the-indian-express",
        "scrape_url": "https://indianexpress.com/",
        "categories": {
            "general": "/india/",
            "politics": "/political-pulse/",
            "business": "/business/",
            "sports": "/sports/",
            "entertainment": "/entertainment/",
            "technology": "/technology/",
            "health": "/lifestyle/health/",
            "science": "/science/"
        }
    },
    "ndtv": {
        "name": "NDTV",
        "api_id": "ndtv",
        "scrape_url": "https://www.ndtv.com/",
        "categories": {
            "general": "/india/",
            "politics": "/india-news/politics/",
            "business": "/business/",
            "sports": "/sports/",
            "entertainment": "/entertainment/",
            "technology": "/gadgets/",
            "health": "/health/",
            "science": "/science/"
        }
    }
}

# Maximum number of retries for API calls
MAX_RETRIES = 3

# Timeout for requests (in seconds)
REQUEST_TIMEOUT = 10

# User agent for web scraping
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" 