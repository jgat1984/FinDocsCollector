//google_drive_uploader

import os
import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "../credentials.json")  # Adjust path if needed
FOLDER_ID = '1fAwIJq2od7nMYPEojHDBYN3zsdIzpseZ'  # Your actual FinDocsUploads folder ID
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Initialize Drive service
def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)

# Upload file function
def upload_file_to_drive(file_path, file_name=None, mime_type=None, folder_id=FOLDER_ID):
    """
    Uploads a file to Google Drive (into your shared folder).
    :param file_path: Path to the local file
    :param file_name: Custom file name (optional)
    :param mime_type: File type (auto-detected if None)
    :param folder_id: Google Drive folder ID
    :return: File ID or None
    """
    try:
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
        print(f"❌ Upload failed: {e}")
        return None

# Optional test:
# upload_file_to_drive("test_upload.txt")
