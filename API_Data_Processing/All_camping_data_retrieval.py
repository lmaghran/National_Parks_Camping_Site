from flask import Flask, render_template, request
import requests
from pprint import pformat
import os
import json
from sys import argv
from pprint import pprint
from datetime import datetime

facility_dictionary={}
api_key= os.environ['REC_API_KEY']

headers = {"apikey": os.environ['REC_API_KEY'], "accept": "application/json"}

# working url "https://ridb.recreation.gov/api/v1/facilities?limit=50&offset=0&activity=camping"

## API for retrieving Facility IDs

def api_looping_funct(loop_no):
    """offsets looping for retrieving facility IDs in rec.gov"""

    # this is the first part of the url
    offset_number = str(50*loop_no)
    loop_url = f"https://ridb.recreation.gov/api/v1/facilities?limit=50&offset={offset_number}&activity=camping"
    return loop_url


def looping_over_rec_api():
    # all_data_file= open("RecGov_json_storage.txt",'w')
    i = 0
    all_data_list =[]

    while i>=0: 
        url = api_looping_funct(i)
        print(url)
        response = requests.get(url, headers=headers)
        json_resp= response.json()
        site_list_data= json_resp["RECDATA"]
        for each_site in site_list_data:
            all_data_list.append(each_site)
        i += 1

        if json_resp['RECDATA'] == []:
            break

    return all_data_list


all_data= looping_over_rec_api() #gathering all camping data from rec.gov

#Storing all rec.gov data in a text file as a list of dictionaries
with open("RecGov_json_storage.txt",'w') as rec_storage_file:
     json.dump(all_data, rec_storage_file)
