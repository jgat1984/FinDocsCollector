import requests
from bs4 import BeautifulSoup

SEEKING_ALPHA_URL = "https://seekingalpha.com/symbol/{ticker}/earnings/transcripts"

def fetch_earnings_transcripts(ticker):
    url = SEEKING_ALPHA_URL.format(ticker=ticker.upper())
    headers = {"User-Agent": "FinDocsCollector/1.0"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        transcripts = []

        for article in soup.select("li.media"):
            title_tag = article.select_one("a.article-link")
            date_tag = article.select_one("span.date")
            if title_tag and date_tag:
                transcripts.append({
                    "title": title_tag.text.strip(),
                    "link": "https://seekingalpha.com" + title_tag["href"],
                    "date": date_tag.text.strip()
                })
        return transcripts
    except Exception:
        return []
