from __future__ import print_function
#For Google Auth
import google_auth_oauthlib
import uploadCSVToSheets 

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
 
scopes = ['https://www.googleapis.com/auth/spreadsheets']



# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1Ph2LX-go4dcKNHezHD8DUtNP2fFO2C2gUPktBLvaPvQ'
DIR = 'metabase/' +  datetime.date.today().strftime("%d-%m-%y") + '/' 

def get_sheets_with_export_prefix(API):
    sheets_with_properties = API \
        .spreadsheets() \
        .get(spreadsheetId=SPREADSHEET_ID, fields='sheets.properties') \
        .execute() \
        .get('sheets')
    export_ids = []
    for sheet in sheets_with_properties:
        if 'title' in sheet['properties'].keys():
            if  "Export" in sheet['properties']['title']:
                export_ids.append( sheet['properties']['sheetId'])
    return export_sheets

def export_sheets(path=DIR): 
    credentials = uploadCSVToSheets.get_creds()
    API = build('sheets', 'v4', credentials=credentials)
    print(get_sheets_with_export_prefix(API))

export_sheets()
