from __future__ import print_function
#For Google Auth
import google_auth_oauthlib
import uploadCSVToSheets 
import metabaseSync
import csv

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
SPREADSHEET_ID = os.getenv("SSID")
DIR = 'sheets/' +  datetime.date.today().strftime("%d-%m-%y") + '/' 

def get_sheets_with_export_prefix(API):
    sheets_with_properties = API \
        .spreadsheets() \
        .get(spreadsheetId=SPREADSHEET_ID, fields='sheets.properties') \
        .execute() \
        .get('sheets')
    export_titles = []
    for sheet in sheets_with_properties:
        if 'title' in sheet['properties'].keys():
            if  "Export" in sheet['properties']['title']:
                export_titles.append( sheet['properties']['title'])
    return export_titles

def get_sheet_data(API, sheet_title): 
    return  (API.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=sheet_title).execute())["values"]

def export_sheets(path=DIR): 
    metabaseSync.mkdir(path)
    credentials = uploadCSVToSheets.get_creds()
    API = build('sheets', 'v4', credentials=credentials)
    sheet_titles =  get_sheets_with_export_prefix(API)
    for i in range(len(sheet_titles)):  
        data = get_sheet_data(API, sheet_titles[i])
        with open(path + sheet_titles[i] + ".csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)


path = 'sheets/' +  datetime.date.today().strftime("%d-%m-%y") + '/' 
list_of_files =  [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
number_of_files = len(list_of_files) 
print(list_of_files)
file = 1
for i in range(number_of_files): 
    #Required offset becasue there is an instructions page at index 0
    record_per_file = 100
    csvfilename = open(path + list_of_files[i], 'r').readlines()
    print(str(csvfilename))
    #store header values
    header = csvfilename[0] 
    #remove header from list
    csvfilename.pop(0) 
    #Number of lines to be written in new file
    for j in range(len(csvfilename)):
        if j % record_per_file == 0:
            write_file = csvfilename[j:j+record_per_file]
            write_file.insert(0, header)
            open(path + str('test')+ str(file) + '.csv', 'w+').writelines(write_file)
            file += 1

