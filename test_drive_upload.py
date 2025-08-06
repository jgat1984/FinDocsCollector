from collectors.google_drive_uploader import upload_to_google_drive
import os

# Create a test file to upload
test_file = os.path.join(os.getcwd(), "test_upload.txt")
with open(test_file, "w") as f:
    f.write("This is a test upload from FinDocsCollector.")

# Try uploading it to Google Drive
print("🔄 Uploading test file to Google Drive...")
link = upload_to_google_drive(test_file)
print("✅ File uploaded successfully!")
print("🌐 View it here:", link)
