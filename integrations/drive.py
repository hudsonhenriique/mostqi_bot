import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials/credentials.json'

FOLDER_ID = '1pTrAtle2a43bywpJIJ-qdI0xvReNSabO'  

def upload_file_to_drive(file_path: str, file_name: str, mime_type='application/json') -> str:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build('drive', 'v3', credentials=credentials)
    
    file_metadata = {
        'name': file_name,
        'parents': [FOLDER_ID]  
    }
    media = MediaFileUpload(file_path, mimetype=mime_type)

    file = service.files().create(
        body=file_metadata, media_body=media, fields='id'
    ).execute()

    file_id = file.get('id')
    file_url = f"https://drive.google.com/file/d/{file_id}/view"

    print(f"✅ Upload feito para o Drive: {file_url}")
    return file_url
