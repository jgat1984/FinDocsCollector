from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import traceback

from .yahoo_collector import fetch_yahoo_data
from .sec_collector import fetch_sec_filings
from .marketwatch_collector import fetch_marketwatch_info
from .earnings_transcript_collector import fetch_earnings_transcript
from .transformer import DataTransformer
# from .google_drive_uploader import upload_file_to_drive  # Upload currently hidden

@csrf_exempt
def company_data_view(request, ticker):
    """Main API endpoint: Fetches data from collectors, transforms it, returns JSON"""
    try:
        print("=" * 50)
        print(f"[INFO] Request received for ticker: {ticker}")

        # ✅ Yahoo Finance data
        raw_data = fetch_yahoo_data(ticker)

        # ✅ SEC Filings
        try:
            raw_data["sec_filings"] = fetch_sec_filings(ticker)
        except Exception as e:
            print(f"[WARN] Failed to fetch SEC filings: {e}")
            raw_data["sec_filings"] = []

        # ✅ MarketWatch headlines
        try:
            raw_data["news"] = fetch_marketwatch_info(ticker)
        except Exception as e:
            print(f"[WARN] Failed to fetch MarketWatch headlines: {e}")
            raw_data["news"] = []

        # ✅ Earnings transcripts
        try:
            raw_data["earnings_transcript"] = fetch_earnings_transcript(ticker)
        except Exception as e:
            print(f"[WARN] Earnings transcript fetch failed: {e}")
            raw_data["earnings_transcript"] = {}

        # ✅ Transform the raw data
        transformed_data = DataTransformer.transform(raw_data)

        return JsonResponse(transformed_data, safe=False)

    except Exception as e:
        print(f"[ERROR] {e}")
        traceback.print_exc()
        return JsonResponse({"error": "Internal server error."}, status=500)
