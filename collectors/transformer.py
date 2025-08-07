# collectors/transformer.py
import datetime
import statistics

class DataTransformer:
    def __init__(self, raw_data):
        self.data = raw_data

    def enrich_price_data(self):
        price = self.data.get("price")
        highs = [self.data.get("7d_high"), self.data.get("1m_high"),
                 self.data.get("3m_high"), self.data.get("1y_high")]
        lows = [self.data.get("7d_low"), self.data.get("1m_low"),
                self.data.get("3m_low"), self.data.get("1y_low")]

        avg_high = statistics.mean([p for p in highs if p is not None])
        avg_low = statistics.mean([p for p in lows if p is not None])

        trend = "Bullish" if price and price > avg_high else "Bearish"

        self.data["analytics"] = {
            "average_high": round(avg_high, 2),
            "average_low": round(avg_low, 2),
            "trend": trend
        }

    def add_timestamp(self):
        self.data["last_updated"] = datetime.datetime.utcnow().isoformat()

    def run(self):
        self.enrich_price_data()
        self.add_timestamp()
        return self.data

    def transform(self):
        return self.run()
