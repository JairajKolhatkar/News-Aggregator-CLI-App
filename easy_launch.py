#!/usr/bin/env python3
"""
Easy launcher for the Indian News Aggregator
This provides a simple menu-based interface for non-technical users.
"""

import os
import sys
import subprocess
import platform

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table

console = Console()

# Categories and sources from config
from utils.config import CATEGORIES, NEWS_SOURCES

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def show_header():
    """Display the application header."""
    console.print(Panel.fit(
        "🇮🇳 [bold green]Indian News Aggregator[/]",
        subtitle="Get the latest Indian news headlines"
    ))

def show_main_menu():
    """Display the main menu options."""
    table = Table(title="Main Menu", expand=True, box=None)
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    
    table.add_row("1", "View latest headlines")
    table.add_row("2", "View headlines by category")
    table.add_row("3", "View headlines by source")
    table.add_row("4", "View headlines by category and source")
    table.add_row("5", "Exit")
    
    console.print(table)

def show_category_menu():
    """Display the category selection menu."""
    table = Table(title="Select a Category", expand=True, box=None)
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Category", style="white")
    
    for i, category in enumerate(CATEGORIES, 1):
        table.add_row(str(i), category.capitalize())
    
    console.print(table)

def show_source_menu():
    """Display the source selection menu."""
    table = Table(title="Select a News Source", expand=True, box=None)
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Source", style="white")
    
    sources = list(NEWS_SOURCES.keys())
    for i, source_key in enumerate(sources, 1):
        source_name = NEWS_SOURCES[source_key]["name"]
        table.add_row(str(i), source_name)
    
    console.print(table)

def run_news_command(category=None, source=None):
    """Run the news aggregator command with the specified options."""
    # Use the main.py directly instead of the module
    cmd = ["python", "main.py", "headlines"]
    
    if category:
        cmd.extend(["--category", category])
    
    if source:
        cmd.extend(["--source", source])
    
    # Run the command
    try:
        subprocess.run(cmd)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
    
    # Wait for user to press Enter before returning to the menu
    console.print("\n[italic]Press Enter to return to the menu...[/]")
    input()

def main():
    """Main function to run the application."""
    while True:
        clear_screen()
        show_header()
        show_main_menu()
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])
        
        if choice == "1":
            # View latest headlines
            clear_screen()
            show_header()
            console.print("[bold]Fetching latest headlines...[/]")
            run_news_command()
            
        elif choice == "2":
            # View headlines by category
            clear_screen()
            show_header()
            show_category_menu()
            
            cat_choice = IntPrompt.ask("Select a category", choices=[str(i) for i in range(1, len(CATEGORIES) + 1)])
            selected_category = CATEGORIES[cat_choice - 1]
            
            clear_screen()
            show_header()
            console.print(f"[bold]Fetching {selected_category.capitalize()} headlines...[/]")
            run_news_command(category=selected_category)
            
        elif choice == "3":
            # View headlines by source
            clear_screen()
            show_header()
            show_source_menu()
            
            sources = list(NEWS_SOURCES.keys())
            source_choice = IntPrompt.ask("Select a source", choices=[str(i) for i in range(1, len(sources) + 1)])
            selected_source = sources[source_choice - 1]
            
            clear_screen()
            show_header()
            console.print(f"[bold]Fetching headlines from {NEWS_SOURCES[selected_source]['name']}...[/]")
            run_news_command(source=selected_source)
            
        elif choice == "4":
            # View headlines by category and source
            clear_screen()
            show_header()
            show_category_menu()
            
            cat_choice = IntPrompt.ask("Select a category", choices=[str(i) for i in range(1, len(CATEGORIES) + 1)])
            selected_category = CATEGORIES[cat_choice - 1]
            
            clear_screen()
            show_header()
            show_source_menu()
            
            sources = list(NEWS_SOURCES.keys())
            source_choice = IntPrompt.ask("Select a source", choices=[str(i) for i in range(1, len(sources) + 1)])
            selected_source = sources[source_choice - 1]
            
            clear_screen()
            show_header()
            console.print(f"[bold]Fetching {selected_category.capitalize()} headlines from {NEWS_SOURCES[selected_source]['name']}...[/]")
            run_news_command(category=selected_category, source=selected_source)
            
        elif choice == "5":
            # Exit
            clear_screen()
            console.print("[bold green]Thank you for using Indian News Aggregator![/]")
            break

if __name__ == "__main__":
    main() 