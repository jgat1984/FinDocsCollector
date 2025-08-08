import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load from environment or place your service account JSON path here
SERVICE_ACCOUNT_FILE = 'collectors/credentials.json'

# Define the Shared Drive ID and folder ID (both required for service accounts)
SHARED_DRIVE_ID = 'your_shared_drive_id_here'
SHARED_FOLDER_ID = 'your_shared_drive_folder_id_here'

def upload_file_to_drive(file_path, file_name):
    """Uploads a file to Google Drive Shared Folder using Service Account"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=['https://www.googleapis.com/auth/drive']
        )

        service = build('drive', 'v3', credentials=credentials)

        file_metadata = {
            'name': file_name,
            'parents': [SHARED_FOLDER_ID],
            'driveId': SHARED_DRIVE_ID,
            'supportsAllDrives': True
        }

        media = MediaFileUpload(file_path, resumable=True)

        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink',
            supportsAllDrives=True
        ).execute()

        print(f"[✅] File uploaded: {uploaded_file.get('webViewLink')}")
        return uploaded_file

    except Exception as e:
        print(f"[❌] Upload failed: {e}")
        return None
