import requests
from bs4 import BeautifulSoup

# ✅ Function to fetch live SEC filings
def fetch_sec_filings(ticker):
    try:
        # Convert ticker to CIK (EDGAR requires CIK or ticker) – using SEC search endpoint
        # Here we use the ticker directly, EDGAR will resolve it
        base_url = (
            f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}"
            "&type=&dateb=&owner=exclude&count=10&output=atom"
        )

        headers = {
            "User-Agent": "FinDocsCollector/1.0 (your_email@example.com)"
        }

        # ✅ Fetch Atom XML feed
        response = requests.get(base_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "xml")
        filings = []

        # ✅ Parse the last 10 filings
        for entry in soup.find_all("entry")[:10]:
            title = entry.find("title").text if entry.find("title") else "N/A"
            link = entry.find("link")["href"] if entry.find("link") else "#"
            date = entry.find("updated").text.split("T")[0] if entry.find("updated") else "N/A"

            filings.append({
                "title": title,
                "date": date,
                "link": link
            })

        return filings if filings else []

    except Exception as e:
        # ✅ Fail gracefully
        return [{"title": "Error fetching SEC filings", "date": "", "link": str(e)}]
