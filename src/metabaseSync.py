import requests
import csv 
import json
import datetime
import time

import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('.') 
load_dotenv(os.path.join(project_folder, '.env'))

headingToken = os.getenv("SESSIONID")

questions_to_export = [
    56, 
    55, 
    61, 
    62, 
    57,
    65,
    66, 
    170, 
    70, 
    72
]   

#def createSet(question_id=none, csv_name=none,sheet_name=none):
#    return {"question": question_id,"csv": csv_name, "sheet_name": sheet_name} 

path = 'metabase/' +  datetime.date.today().strftime("%d-%m-%y") + '/' 

def mkdir(): 
    if not os.path.exists(path):
        os.makedirs(path)
        print("Directory " , path,  " Created ")
    else:
        print("Directory " , path,  " already exists")

def main(): 
    mkdir()
    for i in range( len(questions_to_export)): 
        url = 'https://metabase.ailo.io/api/card/' + str(questions_to_export[i]) 
        headers = {'X-Metabase-Session':headingToken} 
        name_request = requests.get(url, headers=headers)
        csv_request = requests.post(url+'/query/csv', headers=headers)
        f = open(path + str(i) + "_" + json.loads(name_request.text)["name"]+'.csv', "x")
        f.write(csv_request.text)
        f.close
        print(  json.loads(name_request.text)["name"] + " done" )      

main()
