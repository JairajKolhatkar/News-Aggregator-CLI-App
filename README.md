# Indian News Aggregator CLI App

A command-line tool to fetch and display the latest Indian news headlines from popular Indian news sources.

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/JairajKolhatkar/News-Aggregator-CLI-App)

## Features

- Fetch news from multiple Indian news sources (The Hindu, Times of India, Indian Express, NDTV)
- Filter news by source and category
- Beautiful terminal UI using Rich
- Fallback between NewsAPI and web scraping
- Categorization of news articles
- User-friendly menu-based interface

## Installation

1. Clone this repository:
```
git clone https://github.com/JairajKolhatkar/News-Aggregator-CLI-App.git
cd news_aggregator
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Configure your NewsAPI key:
   - Get a free API key from [NewsAPI.org](https://newsapi.org/)
   - Open `utils/config.py` and replace the API key with your actual key

## Usage

### For Non-Technical Users

1. On Windows: Double-click the `start_news.bat` file
2. On Mac/Linux: Open terminal in this folder and type: `python easy_launch.py`
3. Use the menu to navigate and select options by typing the corresponding number

### For Developers

Run the main script:

```
python main.py headlines
```

#### Options

- `--source` or `-s`: Specify a news source (the-hindu, times-of-india, indian-express, ndtv)
- `--category` or `-c`: Filter by category (general, politics, business, sports, entertainment, technology, health, science)
- `--limit` or `-l`: Number of headlines to display (default: 10)
- `--use-api/--use-scraper`: Use NewsAPI or web scraper (default: use API)

#### Examples

Fetch 5 headlines from The Hindu:
```
python main.py headlines --source the-hindu --limit 5
```

Fetch sports news using web scraper:
```
python main.py headlines --category sports --use-scraper
```

Fetch business news from Times of India:
```
python main.py headlines --source times-of-india --category business
```

## Project Structure

- `main.py`: Entry point for the CLI application
- `easy_launch.py`: User-friendly menu-based interface
- `api/`: Modules for API integration
  - `news_api.py`: NewsAPI integration
- `scrapers/`: Web scraping modules
  - `web_scraper.py`: Web scraper for Indian news websites
- `utils/`: Utility modules
  - `config.py`: Configuration settings
  - `helpers.py`: Helper functions

## Screenshots

![Indian News Aggregator CLI](https://raw.githubusercontent.com/JairajKolhatkar/News-Aggregator-CLI-App/main/screenshots/main_menu.png)

## Future Enhancements

1. **Mobile App Integration**: Develop a mobile app version for Android and iOS
2. **Email Notifications**: Add feature to send daily news digests via email
3. **Sentiment Analysis**: Implement sentiment analysis to categorize news as positive, negative, or neutral
4. **Personalized News Feed**: Allow users to save preferences and get personalized news
5. **Voice Integration**: Add text-to-speech functionality to read news headlines
6. **Social Media Sharing**: Enable sharing news articles directly to social media
7. **Offline Mode**: Add capability to save news for offline reading
8. **Regional Language Support**: Add support for major Indian languages
9. **News Summarization**: Implement AI-based summarization of news articles
10. **Topic Clustering**: Group similar news stories together

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
See [CONTRIBUTING.md](CONTRIBUTING.md) for more information.

## Contact

For bugs, feature requests, or other inquiries:
- Email: jairajkolhatkar@gmail.com
- GitHub Issues: https://github.com/JairajKolhatkar/News-Aggregator-CLI-App/issues


