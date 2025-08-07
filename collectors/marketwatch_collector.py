import requests
from bs4 import BeautifulSoup
import feedparser

def fetch_marketwatch_info(ticker):
    try:
        url = f"https://www.marketwatch.com/investing/stock/{ticker.lower()}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/115.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"[WARN] MarketWatch scraping failed: Status {response.status_code}")
            raise Exception("Blocked by MarketWatch")

        soup = BeautifulSoup(response.text, "html.parser")

        headlines = []
        articles = soup.select("div.region--primary .article__content")[:5]

        for article in articles:
            title_tag = article.find("a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag["href"]
                headlines.append({"title": title, "link": link})

        if headlines:
            return headlines
        else:
            raise Exception("No headlines scraped")

    except Exception as e:
        print(f"[ERROR] MarketWatch scraping failed for {ticker}: {e}")
        print("[INFO] Falling back to RSS feed")

        # RSS Fallback (top stories)
        feed_url = "https://feeds.marketwatch.com/marketwatch/topstories/"
        feed = feedparser.parse(feed_url)
        fallback_news = []

        for entry in feed.entries[:5]:
            fallback_news.append({
                "title": entry.title,
                "link": entry.link
            })

        return fallback_news
