import requests
from bs4 import BeautifulSoup
from datetime import datetime
import feedparser

YAHOO_MESSAGE_BOARD_URL = "https://finance.yahoo.com/quote/{ticker}/community"
MARKETWATCH_RSS = "https://feeds.marketwatch.com/marketwatch/realtimeheadlines"

headers = {"User-Agent": "FinDocsCollector/1.0"}

def scrape_yahoo_board(ticker, count=5):
    """Try scraping Yahoo Finance community page (may fail due to JS)."""
    url = YAHOO_MESSAGE_BOARD_URL.format(ticker=ticker.upper())
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        posts = []
        threads = soup.find_all("li", limit=count)
        for t in threads:
            content = t.get_text(strip=True)
            if content:
                posts.append({
                    "author": "Unknown",
                    "content": content[:200],
                    "link": url,
                    "date": datetime.utcnow().isoformat()
                })
        return posts
    except Exception:
        return []

def scrape_marketwatch_fallback(count=5):
    """Fallback to MarketWatch RSS headlines."""
    feed = feedparser.parse(MARKETWATCH_RSS)
    return [{
        "author": "MarketWatch",
        "content": entry.title,
        "link": entry.link,
        "date": datetime(*entry.published_parsed[:6]).isoformat() if hasattr(entry, "published_parsed") else datetime.utcnow().isoformat()
    } for entry in feed.entries[:count]]

def get_yahoo_message_board_posts(ticker, count=5):
    """Main function: Yahoo first, then fallback to MarketWatch RSS."""
    posts = scrape_yahoo_board(ticker, count)
    if not posts:
        posts = scrape_marketwatch_fallback(count)
    return posts

if __name__ == "__main__":
    print(get_yahoo_message_board_posts("MSFT"))
