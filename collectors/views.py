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
        print("[DEBUG] Fetching Yahoo Finance data...")
        raw_data = fetch_yahoo_data(ticker)
        print("[DEBUG] Yahoo Finance data fetched successfully")

        # ✅ SEC Filings
        try:
            print("[DEBUG] Fetching SEC filings...")
            raw_data["sec_filings"] = fetch_sec_filings(ticker)
            print(f"[DEBUG] SEC filings fetched: {len(raw_data['sec_filings'])} items")
        except Exception as e:
            print(f"[ERROR] SEC fetch failed: {e}")
            raw_data["sec_filings"] = []

        # ✅ MarketWatch News
        try:
            print("[DEBUG] Fetching MarketWatch news...")
            news_data = fetch_marketwatch_info(ticker)
            print(f"[DEBUG] MarketWatch returned {len(news_data)} articles")
            raw_data["market_news"] = news_data
        except Exception as e:
            print(f"[ERROR] MarketWatch failed: {e}")
            raw_data["market_news"] = []

        # ✅ Earnings Transcript
        try:
            print("[DEBUG] Fetching earnings transcript...")
            raw_data["earnings_transcript"] = fetch_earnings_transcript(ticker)
            print("[DEBUG] Earnings transcript fetched successfully")
        except Exception as e:
            print(f"[ERROR] Earnings transcript failed: {e}")
            raw_data["earnings_transcript"] = {
                "summary": "Transcript not available",
                "link": f"https://seekingalpha.com/symbol/{ticker}/earnings/transcripts"
            }

        # ✅ Transform Data (Analytics, Trends, etc.)
        try:
            print("[DEBUG] Transforming data...")
            transformed = DataTransformer(raw_data).transform()
            raw_data.update(transformed)
            print("[DEBUG] Data transformed successfully")
        except Exception as e:
            print(f"[ERROR] Data transformation failed: {e}")

        return JsonResponse(raw_data, safe=False)

    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        print(traceback.format_exc())
        return JsonResponse({"error": str(e)})


@csrf_exempt
def upload_to_drive(request):
    print("=" * 60)
    print("[DEBUG] upload_to_drive function triggered")

    try:
        if request.method != "POST":
            print("[DEBUG] Invalid HTTP method:", request.method)
            return JsonResponse({"error": "POST request required"}, status=405)

        if not request.FILES.get("file"):
            print("[DEBUG] No file found in request.FILES")
            return JsonResponse({"error": "No file provided"}, status=400)

        uploaded_file = request.FILES["file"]
        print(f"[DEBUG] File received: {uploaded_file.name}, size: {uploaded_file.size} bytes")

        # Save file temporarily
        temp_path = os.path.join("/tmp", uploaded_file.name)
        print(f"[DEBUG] Saving file temporarily to: {temp_path}")
        with open(temp_path, "wb+") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        print("[DEBUG] File saved locally. Starting Google Drive upload...")
        file_id = upload_file_to_drive(temp_path, file_name=uploaded_file.name)
        print(f"[DEBUG] Google Drive upload successful. File ID: {file_id}")

        # Clean up
        os.remove(temp_path)
        print("[DEBUG] Temporary file deleted after upload")

        return JsonResponse({"message": "Upload successful", "file_id": file_id})

    except Exception as e:
        print("[ERROR] Upload failed!")
        print(traceback.format_exc())
        return JsonResponse({
            "error": str(e),
            "traceback": traceback.format_exc()
        }, status=500)
