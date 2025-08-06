import requests
from bs4 import BeautifulSoup

YAHOO_BOARD_URL = "https://finance.yahoo.com/quote/{ticker}/community"

def fetch_yahoo_board_posts(ticker):
    url = YAHOO_BOARD_URL.format(ticker=ticker.upper())
    headers = {"User-Agent": "FinDocsCollector/1.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        posts = []

        # Yahoo is JS-heavy, may return empty
        for item in soup.select("li.comment")[:10]:
            author = item.select_one("span.username")
            text = item.select_one("p.comment-body")
            time_posted = item.select_one("time")
            posts.append({
                "author": author.text.strip() if author else "Unknown",
                "text": text.text.strip() if text else "",
                "time": time_posted.get("datetime") if time_posted else ""
            })
        return posts
    except Exception:
        return []
