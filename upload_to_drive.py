import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# === Config ===
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_PICKLE = 'token.pickle'
CSV_FILE = 'filtered_products.csv'
DRIVE_FILENAME = 'Filtered Cannabis Products.csv'

def authenticate():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def upload_file(file_path, drive_filename):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': drive_filename}
    media = MediaFileUpload(file_path, mimetype='text/csv')

    # Search for an existing file with the same name
    response = service.files().list(q=f"name='{drive_filename}' and trashed=false",
                                    spaces='drive',
                                    fields='files(id, name)').execute()
    files = response.get('files', [])

    if files:
        # Replace existing file
        file_id = files[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"🔁 Updated existing file: {drive_filename}")
    else:
        # Upload new file
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"⬆️ Uploaded new file: {drive_filename}")

if __name__ == '__main__':
    if os.path.exists(CSV_FILE):
        upload_file(CSV_FILE, DRIVE_FILENAME)
    else:
        print("❌ CSV file not found. Please run filter_products.py first.")
