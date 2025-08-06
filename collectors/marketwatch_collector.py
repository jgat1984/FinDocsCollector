import requests
from bs4 import BeautifulSoup

MW_BASE = "https://www.marketwatch.com/investing/stock/{ticker}"

def fetch_marketwatch_info(ticker):
    """
    Scrape MarketWatch for at least 5 news headlines (title + link).
    """
    url = MW_BASE.format(ticker=ticker.lower())
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    news = []

    try:
        resp = requests.get(url, headers=headers, timeout=8)
        if resp.status_code != 200:
            raise Exception(f"MarketWatch returned status {resp.status_code}")

        soup = BeautifulSoup(resp.text, "html.parser")
        article_links = soup.select("div.article__content a[href], div.element--article a[href], h3 a[href]")

        for link_tag in article_links:
            title = link_tag.get_text(strip=True)
            link = link_tag.get("href")
            if title and link and link.startswith("http") and len(title) > 10:
                if not any(n["title"] == title for n in news):
                    news.append({"title": title, "link": link})
            if len(news) >= 5:
                break

        if not news:
            raise Exception("No headlines found on MarketWatch")

        print(f"[OK] MarketWatch scraped {len(news)} headlines for {ticker}")
        return news

    except Exception as e:
        print(f"[ERROR] MarketWatch scraping failed for {ticker}: {e}")
        return [{"title": f"{ticker.upper()} - No live news available", "link": url}]
