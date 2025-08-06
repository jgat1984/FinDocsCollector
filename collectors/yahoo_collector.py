# collectors/yahoo_collector.py
import yfinance as yf

def fetch_yahoo_data(ticker):
    """
    Fetch price and key high/low data from Yahoo Finance.
    """
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]

        data = {
            "ticker": ticker.upper(),
            "price": round(float(price), 2),
            "7d_high": round(float(stock.history(period="7d")["High"].max()), 2),
            "7d_low": round(float(stock.history(period="7d")["Low"].min()), 2),
            "1m_high": round(float(stock.history(period="1mo")["High"].max()), 2),
            "1m_low": round(float(stock.history(period="1mo")["Low"].min()), 2),
            "3m_high": round(float(stock.history(period="3mo")["High"].max()), 2),
            "3m_low": round(float(stock.history(period="3mo")["Low"].min()), 2),
            "1y_high": round(float(stock.history(period="1y")["High"].max()), 2),
            "1y_low": round(float(stock.history(period="1y")["Low"].min()), 2)
        }
        return data
    except Exception as e:
        return {"ticker": ticker.upper(), "price": None, "error": str(e)}
