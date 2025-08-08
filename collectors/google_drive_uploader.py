import os
import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Constants
CREDENTIALS_PATH = "/etc/secrets/credentials.json"  # ✅ Secure path on Render
FOLDER_ID = '1fAwIJq2od7nMYPEojHDBYN3zsdIzpseZ'      # ✅ Your Google Drive folder
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Initialize Google Drive API service
def get_drive_service():
    try:
        print(f"[DEBUG] Looking for credentials at: {CREDENTIALS_PATH}")
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_PATH, scopes=SCOPES
        )
        service = build('drive', 'v3', credentials=creds)
        print("[DEBUG] Google Drive service initialized.")
        return service
    except Exception as e:
        print("[ERROR] Failed to initialize Google Drive service")
        raise e

# Upload file to Google Drive
def upload_file_to_drive(file_path, file_name=None, mime_type=None, folder_id=FOLDER_ID):
    """
    Uploads a file to Google Drive inside the specified folder.
    :param file_path: Local path to the file
    :param file_name: Desired name on Drive (defaults to filename)
    :param mime_type: MIME type (auto-detected if not specified)
    :param folder_id: Drive folder ID
    :return: Uploaded file ID or None
    """
    try:
        print(f"[DEBUG] Starting upload for: {file_path}")
        service = get_drive_service()
        file_name = file_name or os.path.basename(file_path)
        mime_type = mime_type or mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

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
        raise e
