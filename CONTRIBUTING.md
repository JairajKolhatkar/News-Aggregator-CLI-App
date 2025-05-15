# Contributing to Indian News Aggregator

Thank you for your interest in contributing to the Indian News Aggregator project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YourUsername/News-Aggregator-CLI-App.git`
3. Create a branch for your feature: `git checkout -b feature-name`

## Development Setup

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Configure your NewsAPI key:
   - Get a free API key from [NewsAPI.org](https://newsapi.org/)
   - Open `utils/config.py` and replace the API key with your actual key

## Code Style

Please follow these coding standards:
- Use PEP 8 style guidelines
- Write docstrings for all functions, classes, and modules
- Add type hints where appropriate
- Keep functions focused on a single responsibility

## Testing

Before submitting a pull request, please test your changes:
- Test with both API and web scraper modes
- Try different categories and sources
- Ensure error handling works correctly

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the documentation if you've added new features
3. The PR should work on the main branch
4. Include a clear description of the changes and their purpose

## Adding New News Sources

To add a new news source:
1. Add the source details to `utils/config.py`
2. Implement a scraper function in `scrapers/web_scraper.py`
3. Test thoroughly with different categories

## Feature Requests

Have an idea for a new feature? Please create an issue with the tag "enhancement" and describe:
- What the feature should do
- Why it would be valuable
- Any implementation ideas you have

## Bug Reports

When reporting bugs, please include:
- A clear description of the bug
- Steps to reproduce
- Expected behavior
- Screenshots if applicable
- Your environment (OS, Python version, etc.)

## Contact

If you have questions or need help, please reach out:
- Email: jairajkolhatkar@gmail.com
- GitHub Issues: https://github.com/JairajKolhatkar/News-Aggregator-CLI-App/issues

Thank you for contributing! 