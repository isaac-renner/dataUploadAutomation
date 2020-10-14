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
def mkdir(path=path): 
    if not os.path.exists(path):
        os.makedirs(path)
        print("Directory " , path,  " Created ")
    else:
        print("Directory " , path,  " already exists")


def metabase_requests(question_number): 
    url = 'https://metabase.ailo.io/api/card/' + str(question_number) 
    headers = {'X-Metabase-Session':headingToken} 
    name_request = requests.get(url, headers=headers)
    csv_request = requests.post(url+'/query/csv', headers=headers)
    return ( json.loads(name_request.text)["name"], csv_request.text) 


def fetch_and_save_questions(question_number_array=questions_to_export): 
    mkdir()
    for i in range( len(question_number_array)): 
        responses = metabase_requests(question_number_array[i])
        f = open(path + str(i) + "_" + responses[0] +'.csv', "x")
        f.write(responses[1])
        f.close
        print( responses[0] + " done" )      
