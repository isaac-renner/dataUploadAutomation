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

import datetime
import time

scopes = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = os.getenv("SSID")

#CSV Setup
DIR = 'metabase/' +  datetime.date.today().strftime("%d-%m-%y") + '/' 

import fnmatch

def upload_file_to_sheets(path=DIR):
    credentials = get_creds()
    API = build('sheets', 'v4', credentials=credentials)
    number_of_files = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]) 
    for i in range(number_of_files): 
        #Required offset becasue there is an instructions page at index 0
        sheet_id = find_sheet_id_by_index(i + 1, API)
        csv_path = path + get_file(i, path) 
        print(sheet_id)
        print(csv_path)
        push_csv_to_gsheet(csv_path,sheet_id, API)

        
def get_file(index, path): 
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, str(index)+"*"): 
            return file 

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

def find_sheet_id_by_index(index, API):
    sheets_with_properties = API \
        .spreadsheets() \
        .get(spreadsheetId=SPREADSHEET_ID, fields='sheets.properties') \
        .execute() \
        .get('sheets')
    for sheet in sheets_with_properties:
        if 'title' in sheet['properties'].keys():
            if sheet['properties']['index'] == index:
                print(index)
                print(sheet['properties']['index'])
                print(sheet['properties']['title'])
                return sheet['properties']['sheetId']
