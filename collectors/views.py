from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import os
import traceback

from .yahoo_collector import fetch_yahoo_data
from .sec_collector import fetch_sec_filings
from .marketwatch_collector import fetch_marketwatch_info
from .earnings_transcript_collector import fetch_earnings_transcript
from .transformer import DataTransformer
from .google_drive_uploader import upload_file_to_drive

@csrf_exempt
def company_data_view(request, ticker):
    try:
        print("=" * 60)
        print(f"[INFO] Request received for ticker: {ticker}")

        # ✅ Yahoo Finance Data
        raw_data = fetch_yahoo_data(ticker)

        # ✅ SEC Filings
        try:
            raw_data["sec_filings"] = fetch_sec_filings(ticker)
        except Exception as e:
            print(f"[ERROR] SEC fetch failed: {e}")
            raw_data["sec_filings"] = []

        # ✅ MarketWatch News
        try:
            news_data = fetch_marketwatch_info(ticker)
            print("[DEBUG] MarketWatch returned:", news_data)
            raw_data["market_news"] = news_data
        except Exception as e:
            print(f"[ERROR] MarketWatch failed: {e}")
            raw_data["market_news"] = []

        # ✅ Earnings Transcript
        try:
            raw_data["earnings_transcript"] = fetch_earnings_transcript(ticker)
        except Exception as e:
            print(f"[ERROR] Earnings transcript failed: {e}")
            raw_data["earnings_transcript"] = {
                "summary": "Transcript not available",
                "link": f"https://seekingalpha.com/symbol/{ticker}/earnings/transcripts"
            }

        # ✅ Transform Data (Analytics, Trends, etc.)
        try:
            transformed = DataTransformer(raw_data).transform()
            raw_data.update(transformed)
        except Exception as e:
            print(f"[ERROR] Data transformation failed: {e}")

        return JsonResponse(raw_data, safe=False)

    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        return JsonResponse({"error": str(e)})

@csrf_exempt
def upload_to_drive(request):
    try:
        if request.method == "POST" and request.FILES.get("file"):
            uploaded_file = request.FILES["file"]

            # Save file temporarily
            temp_path = os.path.join("/tmp", uploaded_file.name)
            with open(temp_path, "wb+") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Upload to Google Drive
            file_id = upload_file_to_drive(temp_path, file_name=uploaded_file.name)

            # Clean up
            os.remove(temp_path)

            return JsonResponse({"message": "Upload successful", "file_id": file_id})

        return JsonResponse({"error": "No file provided"}, status=400)

    except Exception as e:
        print("[ERROR] Upload failed:", traceback.format_exc())
        return JsonResponse({"error": "Internal server error"}, status=500)
