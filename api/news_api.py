"""
Module for fetching news from NewsAPI.
"""

import time
from typing import List, Dict, Any, Optional

import requests
from newsapi import NewsApiClient

from utils.config import NEWS_API_KEY, NEWS_SOURCES, MAX_RETRIES, REQUEST_TIMEOUT
from utils.helpers import normalize_news_item, categorize_article

class NewsAPIError(Exception):
    """Exception raised for NewsAPI errors."""
    pass

def fetch_news_from_api(
    source: Optional[str] = None, 
    category: Optional[str] = None, 
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Fetch news from NewsAPI with specified filters.
    
    Args:
        source: The news source to fetch from
        category: The news category to filter by
        limit: Maximum number of news items to return
        
    Returns:
        List of normalized news items
    """
    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        
        # Build query parameters - Using everything endpoint instead of top-headlines
        query_params = {
            "language": "en",
            "pageSize": limit,
            "sortBy": "publishedAt"
        }
        
        # Add source if specified
        if source:
            source_id = NEWS_SOURCES.get(source, {}).get("api_id")
            if source_id:
                query_params["sources"] = source_id
        
        # Add India-specific keywords to ensure relevance
        query_terms = ["India", "Indian", "Delhi", "Mumbai", "Bangalore"]
        
        # Add category-specific terms if category is specified
        if category and category != "general":
            category_terms = {
                "politics": ["politics", "government", "election", "minister", "parliament"],
                "business": ["business", "economy", "market", "finance", "stock"],
                "sports": ["sports", "cricket", "ipl", "match", "tournament"],
                "entertainment": ["entertainment", "bollywood", "movie", "film", "actor"],
                "technology": ["technology", "tech", "digital", "software", "app"],
                "health": ["health", "medical", "doctor", "hospital", "disease"],
                "science": ["science", "research", "scientist", "study", "discovery"]
            }
            if category in category_terms:
                query_terms.extend(category_terms[category])
        
        # Combine query terms with OR operator
        query_params["q"] = " OR ".join(query_terms)
        
        # Try to fetch news with retries
        for attempt in range(MAX_RETRIES):
            try:
                # Use everything endpoint instead of top-headlines
                response = newsapi.get_everything(**query_params)
                break
            except Exception as e:
                if attempt < MAX_RETRIES - 1:
                    time.sleep(1)  # Wait before retrying
                    continue
                else:
                    # If all retries fail, try fallback method
                    return fetch_news_fallback(source, category, limit)
        
        # Process results
        articles = response.get("articles", [])
        
        if not articles:
            # If no results, try fallback method
            return fetch_news_fallback(source, category, limit)
        
        # Normalize news items
        news_items = []
        for article in articles[:limit]:
            source_name = article.get("source", {}).get("name", "Unknown")
            
            # Categorize if not specified
            if not category or category == "general":
                article_category = categorize_article(
                    article.get("title", ""), 
                    article.get("description", "")
                )
                article["category"] = article_category
            else:
                article["category"] = category
                
            news_items.append(normalize_news_item(article, source_name))
            
        return news_items
        
    except Exception as e:
        # If NewsAPI fails, try fallback method
        return fetch_news_fallback(source, category, limit)

def fetch_news_fallback(
    source: Optional[str] = None, 
    category: Optional[str] = None, 
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Fallback method for fetching news when NewsAPI fails.
    Uses a direct HTTP request to the NewsAPI endpoint.
    """
    try:
        # Build URL and parameters - Using everything endpoint instead of top-headlines
        url = "https://newsapi.org/v2/everything"
        
        params = {
            "apiKey": NEWS_API_KEY,
            "language": "en",
            "pageSize": limit,
            "sortBy": "publishedAt"
        }
        
        # Add source if specified
        if source:
            source_id = NEWS_SOURCES.get(source, {}).get("api_id")
            if source_id:
                params["sources"] = source_id
                
        # Add India-specific keywords
        query_terms = ["India", "Indian", "Delhi", "Mumbai", "Bangalore"]
        
        # Add category-specific terms if category is specified
        if category and category != "general":
            category_terms = {
                "politics": ["politics", "government", "election", "minister", "parliament"],
                "business": ["business", "economy", "market", "finance", "stock"],
                "sports": ["sports", "cricket", "ipl", "match", "tournament"],
                "entertainment": ["entertainment", "bollywood", "movie", "film", "actor"],
                "technology": ["technology", "tech", "digital", "software", "app"],
                "health": ["health", "medical", "doctor", "hospital", "disease"],
                "science": ["science", "research", "scientist", "study", "discovery"]
            }
            if category in category_terms:
                query_terms.extend(category_terms[category])
        
        # Combine query terms with OR operator
        params["q"] = " OR ".join(query_terms)
        
        # Make request
        response = requests.get(
            url, 
            params=params, 
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code != 200:
            raise NewsAPIError(f"API request failed with status code {response.status_code}")
            
        data = response.json()
        articles = data.get("articles", [])
        
        # Normalize news items
        news_items = []
        for article in articles[:limit]:
            source_name = article.get("source", {}).get("name", "Unknown")
            
            # Categorize if not specified
            if not category or category == "general":
                article_category = categorize_article(
                    article.get("title", ""), 
                    article.get("description", "")
                )
                article["category"] = article_category
            else:
                article["category"] = category
                
            news_items.append(normalize_news_item(article, source_name))
            
        return news_items
        
    except Exception as e:
        # If all methods fail, return empty list
        return [] 