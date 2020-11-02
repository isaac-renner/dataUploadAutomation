import requests
import csv 
import json 

import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('.') 
load_dotenv(os.path.join(project_folder, '.env'))

auth = os.getenv("SEGMENT_AUTH")


data = {
    "action": "identify",
    "userId": "ailo:authz:user:2991",
    "traits.created": "2020-06-25T05:25:37.111Z",
    "traits.firstName": "Sherry",
    "traits.lastName": "Investor",
    "traits.email": "sherry+investor@ailo.io",
    "traits.management_id": [
      "212d90d9-3737-4611-bcc2-aeb13f3401ce"
    ],
    "traits.first_payment_method_added": "2020-08-15T00:55:51.038346Z"
  }
  
def main(): 
    sync_id = open()
    close(sync_id) 

def open(): 
    url = "https://objects-bulk-api.segmentapis.com/v0/start"
    headers = {'Authorization':auth} 
    request = requests.post(url, headers=headers)
    return json.loads(request.content)['sync_id']


def upload(id): 
    url =  "https://objects-bulk-api.segmentapis.com/v0/upload/" + id
    headers = {'Authorization':auth} 



def close(id): 
    url = "https://objects-bulk-api.segmentapis.com/v0/finish/" + id 
    print(url)
    headers = {'Authorization':auth,'Content-Type':'application/json'} 
    request = requests.post(url, headers=headers)
    print(request.content)


