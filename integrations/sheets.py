from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/credentials.json'

SPREADSHEET_ID = '1kIebPDNfv0Xr4dpjY1GSy2Eex7tWA4N3vqo4Syge840'  

def append_to_sheet(values: list, range_name='A1'):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )

        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()

        body = {'values': [values]}

        result = sheet.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()

        print(f"✅ Dados adicionados à planilha: {result}")
        return result
    except Exception as e:
        print(f"❌ Erro ao adicionar dados à planilha: {e}")
        return None
