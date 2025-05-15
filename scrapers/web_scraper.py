"""
Module for scraping news from Indian news websites.
"""

import concurrent.futures
import datetime
import time
from typing import List, Dict, Any, Optional

import requests
from bs4 import BeautifulSoup

from utils.config import NEWS_SOURCES, REQUEST_TIMEOUT, USER_AGENT
from utils.helpers import clean_text, normalize_news_item, categorize_article

class ScraperError(Exception):
    """Exception raised for scraper errors."""
    pass

def scrape_news_websites(
    source: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Scrape news from Indian news websites.
    
    Args:
        source: The news source to scrape from
        category: The news category to filter by
        limit: Maximum number of news items to return
        
    Returns:
        List of normalized news items
    """
    # If source is specified, scrape only that source
    if source:
        if source in NEWS_SOURCES:
            return scrape_single_source(source, category, limit)
        else:
            return []
    
    # Otherwise, scrape all sources and combine results
    all_news = []
    sources = list(NEWS_SOURCES.keys())
    
    # Use ThreadPoolExecutor to scrape sources in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_source = {
            executor.submit(scrape_single_source, src, category, limit // len(sources) + 1): src
            for src in sources
        }
        
        for future in concurrent.futures.as_completed(future_to_source):
            source_news = future.result()
            all_news.extend(source_news)
    
    # Sort by published date (if available) and limit results
    all_news.sort(
        key=lambda x: x.get("published_at", "Unknown"),
        reverse=True
    )
    
    return all_news[:limit]

def scrape_single_source(
    source: str,
    category: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Scrape a single news source.
    
    Args:
        source: The news source to scrape from
        category: The news category to filter by
        limit: Maximum number of news items to return
        
    Returns:
        List of normalized news items
    """
    source_info = NEWS_SOURCES.get(source, {})
    if not source_info:
        return []
    
    base_url = source_info.get("scrape_url", "")
    if not base_url:
        return []
    
    # Get category-specific URL if category is specified
    if category and category in source_info.get("categories", {}):
        category_path = source_info["categories"][category]
        url = base_url + category_path
    else:
        url = base_url
    
    try:
        # Make request with custom headers
        headers = {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        
        if response.status_code != 200:
            return []
            
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract news based on source
        if source == "the-hindu":
            return scrape_the_hindu(soup, source_info, category, limit)
        elif source == "times-of-india":
            return scrape_times_of_india(soup, source_info, category, limit)
        elif source == "indian-express":
            return scrape_indian_express(soup, source_info, category, limit)
        elif source == "ndtv":
            return scrape_ndtv(soup, source_info, category, limit)
        else:
            return []
            
    except Exception as e:
        # If scraping fails, return empty list
        return []

def scrape_the_hindu(
    soup: BeautifulSoup,
    source_info: Dict[str, Any],
    category: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Scrape news from The Hindu website.
    """
    news_items = []
    base_url = source_info.get("scrape_url", "")
    
    # Find news article elements
    articles = soup.select("div.story-card, div.story-card-33")
    
    for article in articles[:limit]:
        try:
            # Extract title
            title_elem = article.select_one("h3.title, h2.title")
            if not title_elem:
                continue
            title = clean_text(title_elem.text)
            
            # Extract URL
            link_elem = article.select_one("a")
            url = link_elem.get("href", "") if link_elem else ""
            if url and not url.startswith("http"):
                url = base_url + url
                
            # Extract description
            desc_elem = article.select_one("p.intro, div.story-card-33-text")
            description = clean_text(desc_elem.text) if desc_elem else ""
            
            # Extract image
            img_elem = article.select_one("img")
            image_url = img_elem.get("src", "") if img_elem else ""
            
            # Extract date
            date_elem = article.select_one("span.dateline, span.dateTime")
            published_at = clean_text(date_elem.text) if date_elem else datetime.datetime.now().strftime("%d %b %Y")
            
            # Create news item
            item = {
                "title": title,
                "description": description,
                "url": url,
                "urlToImage": image_url,
                "publishedAt": published_at,
                "source": {"name": source_info.get("name", "The Hindu")}
            }
            
            # Determine category if not specified
            if not category or category == "general":
                item_category = categorize_article(title, description)
            else:
                item_category = category
                
            item["category"] = item_category
            
            # Normalize and add to results
            news_items.append(normalize_news_item(item, source_info.get("name", "The Hindu")))
            
        except Exception:
            continue
            
    return news_items

def scrape_times_of_india(
    soup: BeautifulSoup,
    source_info: Dict[str, Any],
    category: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Scrape news from Times of India website.
    """
    news_items = []
    base_url = source_info.get("scrape_url", "")
    
    # Find news article elements
    articles = soup.select("div.main-content div.card-container")
    
    for article in articles[:limit]:
        try:
            # Extract title
            title_elem = article.select_one("span.title")
            if not title_elem:
                continue
            title = clean_text(title_elem.text)
            
            # Extract URL
            link_elem = article.select_one("a")
            url = link_elem.get("href", "") if link_elem else ""
            if url and not url.startswith("http"):
                url = base_url + url
                
            # Extract description
            desc_elem = article.select_one("p.synopsis")
            description = clean_text(desc_elem.text) if desc_elem else ""
            
            # Extract image
            img_elem = article.select_one("img")
            image_url = img_elem.get("src", "") if img_elem else ""
            
            # Extract date
            date_elem = article.select_one("span.date")
            published_at = clean_text(date_elem.text) if date_elem else datetime.datetime.now().strftime("%d %b %Y")
            
            # Create news item
            item = {
                "title": title,
                "description": description,
                "url": url,
                "urlToImage": image_url,
                "publishedAt": published_at,
                "source": {"name": source_info.get("name", "Times of India")}
            }
            
            # Determine category if not specified
            if not category or category == "general":
                item_category = categorize_article(title, description)
            else:
                item_category = category
                
            item["category"] = item_category
            
            # Normalize and add to results
            news_items.append(normalize_news_item(item, source_info.get("name", "Times of India")))
            
        except Exception:
            continue
            
    return news_items

def scrape_indian_express(
    soup: BeautifulSoup,
    source_info: Dict[str, Any],
    category: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Scrape news from Indian Express website.
    """
    news_items = []
    base_url = source_info.get("scrape_url", "")
    
    # Find news article elements
    articles = soup.select("div.article, div.articles")
    
    for article in articles[:limit]:
        try:
            # Extract title
            title_elem = article.select_one("h2.title, h3.title")
            if not title_elem:
                continue
            title = clean_text(title_elem.text)
            
            # Extract URL
            link_elem = article.select_one("a")
            url = link_elem.get("href", "") if link_elem else ""
            if url and not url.startswith("http"):
                url = base_url + url
                
            # Extract description
            desc_elem = article.select_one("p.description, div.synopsis")
            description = clean_text(desc_elem.text) if desc_elem else ""
            
            # Extract image
            img_elem = article.select_one("img")
            image_url = img_elem.get("src", "") if img_elem else ""
            
            # Extract date
            date_elem = article.select_one("div.date, span.date")
            published_at = clean_text(date_elem.text) if date_elem else datetime.datetime.now().strftime("%d %b %Y")
            
            # Create news item
            item = {
                "title": title,
                "description": description,
                "url": url,
                "urlToImage": image_url,
                "publishedAt": published_at,
                "source": {"name": source_info.get("name", "Indian Express")}
            }
            
            # Determine category if not specified
            if not category or category == "general":
                item_category = categorize_article(title, description)
            else:
                item_category = category
                
            item["category"] = item_category
            
            # Normalize and add to results
            news_items.append(normalize_news_item(item, source_info.get("name", "Indian Express")))
            
        except Exception:
            continue
            
    return news_items

def scrape_ndtv(
    soup: BeautifulSoup,
    source_info: Dict[str, Any],
    category: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Scrape news from NDTV website.
    """
    news_items = []
    base_url = source_info.get("scrape_url", "")
    
    # Find news article elements
    articles = soup.select("div.news_item, div.new_storylising, div.story_list")
    
    for article in articles[:limit]:
        try:
            # Extract title
            title_elem = article.select_one("h2.newsHdng, h3.newsHdng, h2.headline")
            if not title_elem:
                continue
            title = clean_text(title_elem.text)
            
            # Extract URL
            link_elem = article.select_one("a")
            url = link_elem.get("href", "") if link_elem else ""
            if url and not url.startswith("http"):
                url = base_url + url
                
            # Extract description
            desc_elem = article.select_one("p.newsCont, div.newsCont, p.description")
            description = clean_text(desc_elem.text) if desc_elem else ""
            
            # Extract image
            img_elem = article.select_one("img")
            image_url = img_elem.get("src", "") if img_elem else ""
            
            # Extract date
            date_elem = article.select_one("span.posted-on, div.posted-on, span.update_date")
            published_at = clean_text(date_elem.text) if date_elem else datetime.datetime.now().strftime("%d %b %Y")
            
            # Create news item
            item = {
                "title": title,
                "description": description,
                "url": url,
                "urlToImage": image_url,
                "publishedAt": published_at,
                "source": {"name": source_info.get("name", "NDTV")}
            }
            
            # Determine category if not specified
            if not category or category == "general":
                item_category = categorize_article(title, description)
            else:
                item_category = category
                
            item["category"] = item_category
            
            # Normalize and add to results
            news_items.append(normalize_news_item(item, source_info.get("name", "NDTV")))
            
        except Exception:
            continue
            
    return news_items 