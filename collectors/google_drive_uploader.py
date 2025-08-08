import os
import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import traceback

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "../credentials.json")  # Adjust path if needed
FOLDER_ID = '1fAwIJq2od7nMYPEojHDBYN3zsdIzpseZ'  # Your actual FinDocsUploads folder ID
SCOPES = ['https://www.googleapis.com/auth/drive.file']


# Initialize Drive service with debug
def get_drive_service():
    print("[DEBUG] Entering get_drive_service()")
    print(f"[DEBUG] Looking for credentials at: {CREDENTIALS_PATH}")
    try:
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH, scopes=SCOPES
        )
        print("[DEBUG] Credentials loaded successfully")
        service = build('drive', 'v3', credentials=creds)
        print("[DEBUG] Google Drive service built successfully")
        return service
    except Exception as e:
        print("[ERROR] Failed to initialize Google Drive service")
        print(traceback.format_exc())
        raise e


# Upload file function with detailed logs
def upload_file_to_drive(file_path, file_name=None, mime_type=None, folder_id=FOLDER_ID):
    """
    Uploads a file to Google Drive (into your shared folder).
    :param file_path: Path to the local file
    :param file_name: Custom file name (optional)
    :param mime_type: File type (auto-detected if None)
    :param folder_id: Google Drive folder ID
    :return: File ID or None
    """
    print("=" * 60)
    print("[DEBUG] Starting upload_file_to_drive()")
    print(f"[DEBUG] file_path: {file_path}")
    print(f"[DEBUG] Provided file_name: {file_name}")
    print(f"[DEBUG] Provided mime_type: {mime_type}")
    print(f"[DEBUG] Target folder ID: {folder_id}")

    try:
        # Step 1: Connect to Google Drive API
        print("[DEBUG] Connecting to Google Drive API...")
        service = get_drive_service()

        # Step 2: Prepare file metadata
        file_name = file_name or os.path.basename(file_path)
        mime_type = mime_type or mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        print(f"[DEBUG] Final file name: {file_name}")
        print(f"[DEBUG] Detected MIME type: {mime_type}")

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        # Step 3: Prepare file upload stream
        print(f"[DEBUG] Preparing MediaFileUpload for {file_path}...")
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        # Step 4: Upload to Google Drive
        print("[DEBUG] Uploading file to Google Drive...")
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        # Step 5: Upload complete
        print(f"✅ Upload successful: {file_name}")
        print(f"🔗 View it here: {uploaded_file.get('webViewLink')}")
        return uploaded_file.get('id')

    except Exception as e:
        print("[ERROR] Upload failed!")
        print(traceback.format_exc())
        return None
