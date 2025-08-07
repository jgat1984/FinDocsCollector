import requests
from bs4 import BeautifulSoup

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
            print(f"[ERROR] MarketWatch request failed: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        headlines = []
        articles = soup.select("div.region--primary .article__content")[:5]

        for article in articles:
            title_tag = article.find("a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag["href"]
                headlines.append({
                    "title": title,
                    "link": link
                })

        return headlines

    except Exception as e:
        print(f"[ERROR] fetch_marketwatch_info failed: {e}")
        return []
