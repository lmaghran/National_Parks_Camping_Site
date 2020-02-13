
import requests
import json
import os

api_key= os.environ['REC_API_KEY']
headers = {"apikey": os.environ['REC_API_KEY'], "accept": "application/json"}

# parentid_types=set()

def nps_rec_api_looping_funct(rec_id):
    """Retrieving facility information about each NP with a campground from 
        rec.gov api"""

def api_looping_funct(loop_no):
    """offsets looping for retrieving information in rec.gov"""
    offset_number = str(50*loop_no)
    loop_url = f"https://ridb.recreation.gov/api/v1/organizations/128/recareas?limit=50&offset={offset_number}"
    return loop_url

def looping_over_rec_api():
    """Loops over all National Park areas (Org Code 128) and returns a list of
    dictionaries about each NP"""
    # all_data_file= open("RecGov_json_storage.txt",'w')
    i = 1
    all_data_list =[]

    while i>=1: 
        url = api_looping_funct(i)
        print(url)
        response = requests.get(url, headers=headers)
        json_resp= response.json()
        site_list_data= json_resp["RECDATA"]
        
        for each_site in site_list_data:
            all_data_list.append(each_site)
        i+=1

        if json_resp["RECDATA"] == []:
            break

    return all_data_list
    

nps_list= looping_over_rec_api()

#adds this data to a seed file
with open("nps_seed_info.txt",'w') as nps_info:
    json.dump(nps_list, nps_info)