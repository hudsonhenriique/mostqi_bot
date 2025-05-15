from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/credentials.json'

# Substitua pelo ID da sua planilha (copie da URL)
SPREADSHEET_ID = '1kIebPDNfv0Xr4dpjY1GSy2Eex7tWA4N3vqo4Syge840'

def append_to_sheet(values: list, range_name='A1'):
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

    return result
