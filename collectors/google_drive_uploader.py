from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Path to your credentials.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(BASE_DIR, "../credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "token.pickle")

# Google Drive API scope
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_drive_service():
    """Authenticate and return Google Drive API service."""
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def upload_file_to_drive(file_path, file_name=None, mime_type="application/octet-stream", folder_id=None):
    """
    Uploads a file to Google Drive.
    :param file_path: Local file path
    :param file_name: Optional custom name for file
    :param mime_type: MIME type
    :param folder_id: Optional Google Drive folder ID
    :return: Uploaded file ID
    """
    service = get_drive_service()
    file_metadata = {'name': file_name or os.path.basename(file_path)}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return uploaded_file.get('id')
