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

        # Yahoo Finance
        raw_data = fetch_yahoo_data(ticker)

        # SEC Filings
        try:
            raw_data["sec_filings"] = fetch_sec_filings(ticker)
        except Exception as e:
            print(f"[ERROR] SEC fetch failed: {e}")
            raw_data["sec_filings"] = []

        # MarketWatch
        try:
            raw_data["market_news"] = fetch_marketwatch_info(ticker)
        except Exception as e:
            print(f"[ERROR] MarketWatch failed: {e}")
            raw_data["market_news"] = []

        # Earnings Transcript
        try:
            raw_data["earnings_transcript"] = fetch_earnings_transcript(ticker)
        except Exception as e:
            print(f"[ERROR] Earnings transcript failed: {e}")
            raw_data["earnings_transcript"] = {
                "summary": "Transcript not available",
                "link": f"https://seekingalpha.com/symbol/{ticker}/earnings/transcripts"
            }

        # Transform Data
        try:
            transformed = DataTransformer(raw_data).transform()
            raw_data.update(transformed)
        except Exception as e:
            print(f"[ERROR] Data transformation failed: {e}")

        return JsonResponse(raw_data, safe=False)

    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def upload_to_drive(request):
    print("=" * 60)
    print("[DEBUG] upload_to_drive function triggered")

    try:
        if request.method != "POST":
            return JsonResponse({"error": "POST request required"}, status=405)

        if not request.FILES.get("file"):
            return JsonResponse({"error": "No file provided"}, status=400)

        uploaded_file = request.FILES["file"]
        temp_dir = os.path.join(os.path.dirname(__file__), "temp_uploads")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_path, "wb+") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        file_id = upload_file_to_drive(temp_path, file_name=uploaded_file.name)
        os.remove(temp_path)

        if not file_id:
            return JsonResponse({"error": "Google Drive upload failed"}, status=500)

        return JsonResponse({
            "message": "Upload successful",
            "file_id": file_id
        })

    except Exception as e:
        print("[ERROR] Upload failed:", traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=500)
