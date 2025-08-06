import yfinance as yf

def get_stock_price(ticker):
    """
    Fetch current stock price using Yahoo Finance.
    Returns: float or None if unavailable.
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        if not data.empty:
            return round(data['Close'].iloc[-1], 2)
        return None
    except Exception:
        return None

if __name__ == "__main__":
    print(get_stock_price("MSFT"))
