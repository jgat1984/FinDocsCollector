import os
import mimetypes
import traceback
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Render will place credentials.json in /opt/render/project/src/
CREDENTIALS_PATH = os.path.abspath(os.path.join(BASE_DIR, "credentials.json"))
FOLDER_ID = '1fAwIJq2od7nMYPEojHDBYN3zsdIzpseZ'  # ✅ Your actual folder
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    try:
        print(f"[DEBUG] Looking for credentials at: {CREDENTIALS_PATH}")
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH, scopes=SCOPES
        )
        print("[DEBUG] Google Drive credentials loaded successfully")
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print("[ERROR] Failed to initialize Google Drive service")
        print(traceback.format_exc())
        raise e  # Let the calling function catch and log it

def upload_file_to_drive(file_path, file_name=None, mime_type=None, folder_id=FOLDER_ID):
    """
    Uploads a file to Google Drive inside a specified folder.
    Returns the uploaded file ID if successful.
    """
    try:
        service = get_drive_service()

        file_name = file_name or os.path.basename(file_path)
        mime_type = mime_type or mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

        file_metadata = {
            'name': file_name,
            'parents': [folder_id],
        }

        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

        print(f"[DEBUG] Uploading file: {file_name} (MIME: {mime_type})")
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        print(f"✅ Uploaded: {file_name}")
        print(f"🔗 View it here: {uploaded_file['webViewLink']}")

        return uploaded_file.get('id')

    except Exception as e:
        print("[ERROR] Upload failed!")
        print(traceback.format_exc())
        return None
