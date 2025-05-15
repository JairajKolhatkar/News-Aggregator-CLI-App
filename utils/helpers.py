"""
Helper functions for the news aggregator.
"""

import re
import datetime
from typing import Dict, Any, Optional

def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and special characters.
    """
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def format_date(date_str: str, input_format: Optional[str] = None) -> str:
    """
    Format date string to a standardized format.
    
    If input_format is None, try to parse the date using various formats.
    """
    if not date_str:
        return "Unknown"
    
    try:
        if input_format:
            dt = datetime.datetime.strptime(date_str, input_format)
        else:
            # Try common formats
            formats = [
                "%Y-%m-%dT%H:%M:%SZ",  # ISO format (2023-05-15T14:30:00Z)
                "%Y-%m-%d %H:%M:%S",   # Standard format (2023-05-15 14:30:00)
                "%d %b %Y %H:%M",      # 15 May 2023 14:30
                "%d %B %Y",            # 15 May 2023
                "%d-%m-%Y",            # 15-05-2023
                "%d/%m/%Y"             # 15/05/2023
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                return date_str  # Return original if no format matches
        
        # Format to a standard output
        return dt.strftime("%d %b %Y, %H:%M")
        
    except Exception:
        return date_str

def normalize_news_item(item: Dict[Any, Any], source: str) -> Dict[str, Any]:
    """
    Normalize news item data from different sources into a standard format.
    """
    normalized = {
        "id": item.get("id", item.get("url", ""))[:50],
        "title": clean_text(item.get("title", "")),
        "description": clean_text(item.get("description", "")),
        "content": clean_text(item.get("content", "")),
        "url": item.get("url", ""),
        "source": item.get("source", {}).get("name", source),
        "category": item.get("category", "general"),
        "published_at": format_date(item.get("publishedAt", "")),
        "image_url": item.get("urlToImage", "")
    }
    
    return normalized

def categorize_article(title: str, content: str) -> str:
    """
    Attempt to categorize an article based on its title and content.
    
    Returns a category from the CATEGORIES list.
    """
    # Simple keyword-based categorization
    keywords = {
        "politics": ["election", "minister", "government", "parliament", "political", "bjp", "congress", "modi"],
        "business": ["economy", "market", "stock", "finance", "business", "company", "trade", "rupee"],
        "sports": ["cricket", "ipl", "sport", "match", "player", "team", "tournament", "athlete"],
        "entertainment": ["movie", "film", "actor", "actress", "bollywood", "cinema", "star", "celebrity"],
        "technology": ["tech", "technology", "digital", "software", "app", "computer", "internet", "cyber"],
        "health": ["health", "medical", "doctor", "hospital", "disease", "covid", "vaccine", "medicine"],
        "science": ["science", "research", "scientist", "study", "discovery", "space", "nasa", "isro"]
    }
    
    text = (title + " " + content).lower()
    
    # Count keyword matches for each category
    category_scores = {category: 0 for category in keywords}
    
    for category, category_keywords in keywords.items():
        for keyword in category_keywords:
            if keyword.lower() in text:
                category_scores[category] += 1
    
    # Find category with highest score
    max_score = 0
    best_category = "general"
    
    for category, score in category_scores.items():
        if score > max_score:
            max_score = score
            best_category = category
    
    return best_category 