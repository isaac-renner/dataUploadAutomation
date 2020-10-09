from __future__ import print_function
#For Google Auth
import google_auth_oauthlib

#.env files
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('.') 
load_dotenv(os.path.join(project_folder, '.env'))

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
scopes = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1Ph2LX-go4dcKNHezHD8DUtNP2fFO2C2gUPktBLvaPvQ'
RANGE_NAME = 'A:E'

#CSV Setup
csv_path = '/Users/isaacrenner/Documents/automation/metabase/09-10-20/Auto Pay Rent Enabled Since.csv' 


def main():
    credentials = get_creds()
    API = build('sheets', 'v4', credentials=credentials)

    sheet_id = find_sheet_id_by_name('Import Legal Entities', API)
    push_csv_to_gsheet(csv_path,sheet_id, API)

def get_creds(): 
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def push_csv_to_gsheet(csv_path, sheet_id, API):
    with open(csv_path, 'r') as csv_file:
        csvContents = csv_file.read()
    body = {
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": sheet_id,
                    "rowIndex": "0",  # adapt this if you need different positioning
                    "columnIndex": "0", # adapt this if you need different positioning
                },
                "data": csvContents,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
            }
        }]
    }
    request = API.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body)
    response = request.execute()
    return response

def find_sheet_id_by_name(sheet_name, API):
    sheets_with_properties = API \
        .spreadsheets() \
        .get(spreadsheetId=SPREADSHEET_ID, fields='sheets.properties') \
        .execute() \
        .get('sheets')

    for sheet in sheets_with_properties:
        if 'title' in sheet['properties'].keys():
            if sheet['properties']['title'] == sheet_name:
                return sheet['properties']['sheetId']


if __name__ == '__main__':
    main()
