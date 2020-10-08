import requests
import csv 
import json

import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('.') 
load_dotenv(os.path.join(project_folder, '.env'))

headingToken = os.getenv("SESSIONID")
print(headingToken)

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


for i in range( len(questions_to_export)): 
    url = 'https://metabase.ailo.io/api/card/' + str(questions_to_export[i]) 
    headers = {'X-Metabase-Session':headingToken} 

    csv_request = requests.post(url+'/query/csv', headers=headers)
    f = open('metabase/'+json.loads(name_request.text)["name"]+'.csv', "w")
    f.write(csv_request.text)
    f.close

print('done')
