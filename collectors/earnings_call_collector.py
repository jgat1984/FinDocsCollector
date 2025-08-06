import requests
from bs4 import BeautifulSoup

SA_BASE = "https://seekingalpha.com/symbol/{ticker}/earnings/transcripts"
MF_BASE = "https://www.fool.com/earnings-call-transcripts/{company}/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def fetch_seeking_alpha_transcripts(ticker):
    url = SA_BASE.format(ticker=ticker.upper())
    transcripts = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return transcripts
        soup = BeautifulSoup(resp.text, "html.parser")

        # Extract transcript titles and links
        for item in soup.select("a[data-test-id='post-list-title']")[:5]:
            title = item.get_text(strip=True)
            link = "https://seekingalpha.com" + item.get("href")

            # Try to get preview snippet (first paragraph of the article page)
            preview = ""
            try:
                article = requests.get(link, headers=HEADERS, timeout=10)
                if article.status_code == 200:
                    article_soup = BeautifulSoup(article.text, "html.parser")
                    para = article_soup.select_one("p")
                    preview = para.get_text(strip=True) if para else ""
            except:
                pass

            transcripts.append({"title": title, "link": link, "preview": preview})

    except Exception as e:
        print(f"[ERROR] Seeking Alpha transcripts: {e}")

    return transcripts


def fetch_motley_fool_transcripts(company_name):
    url = MF_BASE.format(company=company_name.lower())
    transcripts = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return transcripts
        soup = BeautifulSoup(resp.text, "html.parser")

        # Motley Fool lists transcripts under <a> with article links
        for item in soup.select("a[href*='/earnings-call-transcript/']")[:5]:
            title = item.get_text(strip=True)
            link = "https://www.fool.com" + item.get("href")
            transcripts.append({"title": title, "link": link, "preview": ""})

    except Exception as e:
        print(f"[ERROR] Motley Fool transcripts: {e}")

    return transcripts


def fetch_earnings_call_transcripts(ticker, company_name=None):
    # Try Seeking Alpha first
    transcripts = fetch_seeking_alpha_transcripts(ticker)
    if transcripts:
        return transcripts

    # If SA fails, fallback to Motley Fool
    if company_name:
        return fetch_motley_fool_transcripts(company_name)

    return []
