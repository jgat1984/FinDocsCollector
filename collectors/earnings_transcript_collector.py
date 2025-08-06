# collectors/earnings_transcript_collector.py
import requests
from bs4 import BeautifulSoup

def fetch_earnings_transcript(ticker):
    """
    Attempt to fetch the latest earnings call transcript from Seeking Alpha.
    If blocked or unavailable, returns a placeholder summary.
    """
    try:
        url = f"https://seekingalpha.com/symbol/{ticker}/earnings/transcripts"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return {"summary": "Transcript not available", "link": url}

        soup = BeautifulSoup(response.text, "html.parser")
        # Attempt to grab the first transcript link
        link_tag = soup.find("a", href=True)
        if not link_tag:
            return {"summary": "Transcript not available", "link": url}

        transcript_url = f"https://seekingalpha.com{link_tag['href']}"
        transcript_response = requests.get(transcript_url, headers=headers, timeout=10)

        if transcript_response.status_code != 200:
            return {"summary": "Transcript not available", "link": transcript_url}

        # Extract text (simplified)
        transcript_soup = BeautifulSoup(transcript_response.text, "html.parser")
        paragraphs = transcript_soup.find_all("p")
        text = " ".join([p.text for p in paragraphs[:10]])  # only first 10 paragraphs

        # Return a short summary (basic truncation)
        summary = (text[:500] + "...") if len(text) > 500 else text
        return {"summary": summary, "link": transcript_url}

    except Exception as e:
        return {"summary": f"Error fetching transcript: {e}", "link": None}
