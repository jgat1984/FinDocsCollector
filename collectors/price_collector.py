import yfinance as yf
from datetime import datetime, timedelta

def get_high_low(data, days):
    """Helper function to calculate high/low for a given period."""
    recent = data.tail(days)
    return round(recent['High'].max(), 2), round(recent['Low'].min(), 2)

def get_company_data(ticker):
    """
    Fetch stock price and historical high/lows for the last 7 days, 1 month, 3 months, and 1 year.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")  # fetch 1 year of data
        price = round(stock.info.get("currentPrice", hist['Close'].iloc[-1]), 2)

        # Calculate high/low
        high_7d, low_7d = get_high_low(hist, 7)
        high_1m, low_1m = get_high_low(hist, 30)
        high_3m, low_3m = get_high_low(hist, 90)
        high_1y, low_1y = get_high_low(hist, 252)  # ~252 trading days in a year

        # SEC Filings placeholder (you can integrate your real scraper here)
        sec_filings = [
            {
                "title": "10-K",
                "link": f"https://www.sec.gov/edgar/search/#/q={ticker}",
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        ]

        # News placeholder (real integration comes from your news collector)
        news = [
            {
                "title": f"{ticker} hits new market update",
                "link": f"https://finance.yahoo.com/quote/{ticker}"
            }
        ]

        return {
            "ticker": ticker,
            "price": price,
            "high_7d": high_7d,
            "low_7d": low_7d,
            "high_1m": high_1m,
            "low_1m": low_1m,
            "high_3m": high_3m,
            "low_3m": low_3m,
            "high_1y": high_1y,
            "low_1y": low_1y,
            "sec_filings": sec_filings,
            "news": news
        }

    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker}: {str(e)}"}
