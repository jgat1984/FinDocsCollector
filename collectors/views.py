from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import traceback
import tempfile
import os

from .yahoo_collector import fetch_yahoo_data
from .sec_collector import fetch_sec_filings
from .marketwatch_collector import fetch_marketwatch_info
from .earnings_transcript_collector import fetch_earnings_transcript
from .transformer import DataTransformer
from .google_drive_uploader import upload_file_to_drive


def company_data_view(request, ticker):
    """Main API endpoint: Fetches data from collectors, transforms it, returns JSON"""
    try:
        print("=" * 50)
        print(f"[INFO] Request received for ticker: {ticker}")

        # ✅ Yahoo Finance
        raw_data = fetch_yahoo_data(ticker)

        # ✅ SEC Filings
        try:
            raw_data["sec_filings"] = fetch_sec_filings(ticker)
        except Exception as e:
            print("[ERROR] SEC Collector failed:", e)
            raw_data["sec_filings"] = []

        # ✅ MarketWatch News
        try:
            raw_data["market_news"] = fetch_marketwatch_info(ticker)
        except Exception as e:
            print("[ERROR] MarketWatch Collector failed:", e)
            raw_data["market_news"] = [{"title": "No live news available", "link": "#"}]

        # ✅ Earnings Transcript
        try:
            raw_data["earnings_transcript"] = fetch_earnings_transcript(ticker)
        except Exception as e:
            print("[ERROR] Transcript Collector failed:", e)
            raw_data["earnings_transcript"] = {"summary": "Not available", "link": None}

        # ✅ Data Transformation
        try:
            transformer = DataTransformer(raw_data)
            transformed = transformer.run()
        except Exception as e:
            print("[ERROR] Transformer failed:", e)
            transformed = raw_data

        return JsonResponse(transformed, safe=False)

    except Exception as e:
        print("[FATAL ERROR] company_data_view failed:", e)
        print(traceback.format_exc())
        return JsonResponse({"error": str(e)}, status=500)


# ❌ REMOVE THIS OLD FUNCTION – IT CAUSED THE ERROR
# @csrf_exempt
# def upload_to_drive(request):
#     """(Deprecated) Old Google Drive upload that passes InMemoryUploadedFile directly."""
#     return JsonResponse({"error": "This endpoint is deprecated. Use /api/upload/ instead."}, status=410)


# ✅ Old CORRECT UPLOAD ENDPOINT
@csrf_exempt
def upload_to_drive(request):
    """Handles Google Drive file uploads using a temp file path (correct approach)."""
    print("[DEBUG] upload_to_drive_view endpoint hit")

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        print(f"[DEBUG] Received file: {uploaded_file.name}, size: {uploaded_file.size} bytes")

        try:
            # ✅ Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            print(f"[DEBUG] Temp file saved at: {tmp_path}")

            # ✅ Upload to Google Drive
            try:
                file_id = upload_file_to_drive(tmp_path, uploaded_file.name)
                print(f"[DEBUG] Google Drive returned file ID: {file_id}")
                os.remove(tmp_path)
                return JsonResponse({"message": "File uploaded successfully", "file_id": file_id})
            except Exception as e:
                os.remove(tmp_path)
                error_msg = f"Google Drive Upload Failed: {str(e)}"
                print("[DEBUG] ERROR:", error_msg)
                print("[DEBUG] Traceback:\n", traceback.format_exc())
                return JsonResponse({"error": error_msg}, status=500)

        except Exception as e:
            error_msg = f"Internal Server Error: {str(e)}"
            print("[DEBUG] ERROR:", error_msg)
            print("[DEBUG] Traceback:\n", traceback.format_exc())
            return JsonResponse({"error": error_msg}, status=500)

    print("[DEBUG] No file provided or incorrect HTTP method")
    return JsonResponse({"error": "No file provided"}, status=400)
