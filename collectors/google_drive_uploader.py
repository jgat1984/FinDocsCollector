from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# OAuth scope — allows file upload to user's Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_file_to_drive(file_path, folder_id):
    creds = None

    # Load or request OAuth token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Connect to Drive API
    service = build('drive', 'v3', credentials=creds)

    # Set file metadata and upload
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    print("✅ Upload successful!")
    print("📎 File ID:", file.get('id'))
    print("🔗 View it:", file.get('webViewLink'))

# 🔻 Run uploader
if __name__ == "__main__":
    upload_file_to_drive("msft_data.json", "1fAwlJq2od7nMYPEojHDBYN3zsdIzpseZ")
