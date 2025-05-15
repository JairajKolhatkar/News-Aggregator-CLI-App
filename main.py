#!/usr/bin/env python3
"""
Indian News Aggregator CLI App
A command-line tool to fetch and display the latest Indian news headlines.
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress

from api.news_api import fetch_news_from_api
from scrapers.web_scraper import scrape_news_websites
from utils.config import CATEGORIES, NEWS_SOURCES

console = Console()

@click.group()
def cli():
    """Indian News Aggregator - Get the latest Indian news headlines."""
    pass

@cli.command()
@click.option('--source', '-s', type=click.Choice(NEWS_SOURCES.keys()), help='News source to fetch from')
@click.option('--category', '-c', type=click.Choice(CATEGORIES), help='News category to filter by')
@click.option('--limit', '-l', default=10, help='Number of headlines to display')
@click.option('--use-api/--use-scraper', default=True, help='Use NewsAPI or web scraper')
def headlines(source, category, limit, use_api):
    """Fetch and display the latest Indian news headlines."""
    with Progress() as progress:
        task = progress.add_task("[green]Fetching news...", total=1)
        
        try:
            if use_api:
                news_items = fetch_news_from_api(source=source, category=category, limit=limit)
            else:
                news_items = scrape_news_websites(source=source, category=category, limit=limit)
                
            progress.update(task, completed=1)
            
            if not news_items:
                console.print(Panel("No news found matching your criteria.", 
                                    title="Error", 
                                    border_style="red"))
                return
                
            display_news(news_items, source, category)
            
        except Exception as e:
            progress.update(task, completed=1)
            console.print(Panel(f"Error: {str(e)}", 
                                title="Error", 
                                border_style="red"))

def display_news(news_items, source=None, category=None):
    """Display news items in a formatted table."""
    title = "Latest Indian News"
    if source:
        title += f" from {source}"
    if category:
        title += f" - {category.capitalize()}"
    
    table = Table(title=title, expand=True)
    
    table.add_column("Source", style="cyan", no_wrap=True)
    table.add_column("Title", style="white", no_wrap=False)
    table.add_column("Category", style="green")
    table.add_column("Published", style="yellow")
    
    for item in news_items:
        table.add_row(
            item.get('source', 'Unknown'),
            item.get('title', 'No title'),
            item.get('category', 'General'),
            item.get('published_at', 'Unknown')
        )
    
    console.print(table)
    
    # Display detailed view option
    console.print("\nUse [bold cyan]news-aggregator read [ID][/] to read the full article")

if __name__ == '__main__':
    console.print(Panel.fit("🇮🇳 [bold green]Indian News Aggregator[/]", 
                           subtitle="Get the latest Indian news headlines"))
    cli() 