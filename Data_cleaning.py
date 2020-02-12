from flask import Flask, render_template, request
import requests
from pprint import pformat
import os
import json
from sys import argv
from pprint import pprint
from datetime import datetime

reservable_campsite_list=[]
all_fac_types=set()

with open("RecGov_json_storage.txt") as json_file:
    data = json.load(json_file)

for i, rec_dict in enumerate(data): # there is only one "Kiosk" and it doesn't have a campground
    if rec_dict["FacilityTypeDescription"] == "Kiosk": 
        data.pop(i)

    elif rec_dict["FacilityTypeDescription"] == "Construction Camp site": #Only one- need to remove
        data.pop(i)

    # if rec_dict["FacilityTypeDescription"] == "Permit": #Only two- these are non-reservable cabins, leaving them in

    #if rec_dict["FacilityTypeDescription"] == "Facility": #1611 of these, leaving them in

with open("cleaned_reservable_campsite_info.txt",'w') as cleaned_rec_storage_file:
    json.dump(data, cleaned_rec_storage_file)

