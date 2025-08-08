# google_drive_uploader.py

import os
import mimetypes
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "../credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")  # Will be created after first login
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = '1fAwIJq2od7nMYPEojHDBYN3zsdIzpseZ'  # Your My Drive folder

# Get authorized Google Drive service using OAuth
def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

# Upload file function
def upload_file_to_drive(file_path, file_name=None, mime_type=None, folder_id=FOLDER_ID):
    """
    Uploads a file to your personal Google Drive folder.
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

# Optional test run
# upload_file_to_drive("test_upload.txt")
