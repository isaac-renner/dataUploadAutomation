import requests
import csv 
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('./my-project-dir') 
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

url = 'https://metabase.ailo.io/api/card/65/query/csv' 
headers = {'X-Metabase-Session':SheadingToken} 
    
r = requests.post(url, headers=headers)

f = open('metabase/autoWithdraw.csv', 'w')
f.write(r.text)
f.close
print('done')
