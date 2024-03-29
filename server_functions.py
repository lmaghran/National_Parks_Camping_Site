from model import connect_to_db, db, Campsite, Recreation_area
from flask import Flask, jsonify, render_template, request
import requests
import os
import random
from datetime import datetime, date

def rec_area_list():

    rec_areas=Recreation_area.query.filter(Recreation_area.campsites != None).\
            order_by(Recreation_area.rec_name).all()

    return rec_areas

def random_images(rec_areas):
    """Gets random images for front screen carousel"""
    random_images=[]

    while len(random_images)<9:
        Recreation_area.query.filter(Recreation_area.campsites != None).\
        order_by(Recreation_area.rec_name).all()
        random_np= random.choice(rec_areas)
        random_id= random_np.rec_id_name
        image_list=get_nps_photos(random_id)
        random_images+=image_list

    return random_images[:7]


def get_nps_code(selected_area):
    """Gets the NPS code of a recreation area"""

    #querying for name of rec area
    rec_area=Recreation_area.query.filter(Recreation_area.rec_name==selected_area).first()
    nps_code= rec_area.rec_id_name

    return nps_code

def get_np_info(selected_area):
    """Retrieves dictionary from NPS API from NPS code"""

    nps_api_key= os.environ['NPS_API_KEY']
    headers = {"apikey": os.environ['NPS_API_KEY'], "accept": "application/json"}
    nps_code= get_nps_code(selected_area)
    url = f"https://developer.nps.gov/api/v1/parks?parkCode={nps_code}&fields=images&api_key={nps_api_key}"
    response = requests.get(url, headers=headers)
    json_resp= response.json()
    np_info=json_resp['data'][0]

    return np_info


def get_nps_photos(nps_code):
    """Finds each photo in a dictionary from NPS"""

    working_Url= "https://developer.nps.gov/api/v1/parks?parkCode=YELL&fields=images&api_key=LhjXYnr7nnTeOSqGDAblu63wpF7a99ml5ahZWzFE"
    nps_api_key= os.environ['NPS_API_KEY']
    headers = {"apikey": os.environ['NPS_API_KEY'], "accept": "application/json"}
    url = f"https://developer.nps.gov/api/v1/parks?parkCode={nps_code}&fields=images&api_key={nps_api_key}"
    response = requests.get(url, headers=headers)
    json_resp= response.json()
    image_list=json_resp['data'][0]['images']

    return image_list



def get_campsites(selected_area):
    """Retrieves the list of campsites for each recreation area"""

    #querying for name of rec area
    rec_area=Recreation_area.query.filter(Recreation_area.rec_name==selected_area).first()
    selected_campsites= rec_area.campsites

    return selected_campsites

def get_avail_dictionary(camp_id, start_date, end_date):
    """Returns availability JSON from Recreation.gov"""
    headers={'User-Agent': 'Mozilla/5.0', "accept": "application/json" }
    availability_url=f'http://www.recreation.gov/api/camps/availability/campground/{camp_id}?start_date={start_date}T00%3A00%3A00.000Z&end_date={end_date}T00%3A00%3A00.000Z'
    print(availability_url)
    avail_json_response = requests.get(availability_url, headers={'User-Agent': 'Mozilla/5.0', "accept": "application/json" })
    avail_dict_response= avail_json_response.json() ### this is a dictionary

    return avail_dict_response



def generate_campsite_dictionary(selected_campsites, start_date, end_date):
    """Generates the campsite dictionary of availability based on recreation.gov api response"""
    campsite_dictionary={}
    available_campsite_list=[]

    for campsite in selected_campsites: # circling through list of campsites in a National Park
        camp_id= campsite.facility_id
        avail_dict= get_avail_dictionary(camp_id, start_date, end_date)
        campsite_dictionary[campsite.campsite_name.title()]= {}
        campsite_dictionary[campsite.campsite_name.title()]["campground_id"]= campsite.facility_id
        for site in avail_dict['campsites']:
            dates_stayed= len(avail_dict['campsites'][site]['availabilities'])
            i=0
            for availability in avail_dict['campsites'][site]['availabilities']:
                if avail_dict['campsites'][site]['availabilities'][availability]=="Available":
                    i+=1
            if i==dates_stayed:
                available_campsite_list.append(avail_dict['campsites'][site])
    if len(available_campsite_list)!=0:
        campsite_dictionary[campsite.campsite_name.title()]["availability_data"]=available_campsite_list
    avail_json= campsite_dictionary
    return avail_json


def datetime_formatting(date):
    """Formats datetime for display in availability tab"""
    date= datetime.strptime(date, '%Y-%m-%d')
    date=date.strftime("%m/%d/%Y")
    return date


def generate_availability_dictionary():
    ## Returns dictionary for mapping and availability
    avail_json={}
    available_campsite_list=[]
    selected_campsites= []
    np_campground_names=[]

    all_campsite_list=[]
    all_campsites= Campsite.query.filter(Campsite.facility_id!= None).order_by(Campsite.campsite_name).all()

    for campsite in all_campsites:
        all_campsite_geodata={}
        all_campsite_geodata['campground_name']=campsite.campsite_name.title()
        all_campsite_geodata['facility_id']= campsite.facility_id
        all_campsite_geodata['lat']= campsite.campsite_lat
        all_campsite_geodata['long']= campsite.campsite_long
        all_campsite_geodata['availability']= 'unknown'
        all_campsite_list.append(all_campsite_geodata)

    if request.args.get('rec_area') != None:
        selected_area= request.args.get('rec_area')

    if (request.args.get('end-date') != None) and (request.args.get('start-date') != None):
        start_date=request.args.get('start-date')
        end_date=request.args.get('end-date')
        selected_campsites= get_campsites(selected_area)
        avail_json= generate_campsite_dictionary(selected_campsites, start_date, end_date)
        avail_json['rec_area']= selected_area
        start_date= datetime_formatting(start_date)
        end_date= datetime_formatting(end_date)
        avail_json['dates']= (start_date, end_date)

    for campsite in selected_campsites:     # renames items based on their availability
        np_campground_names.append(campsite.campsite_name.title())

    for campground in all_campsite_list:
        name= campground['campground_name']

        if name in np_campground_names:
            if avail_json[name].get('availability_data') != None:
                campground["availability"]= f"Available from {start_date} through {end_date}"
            else:
                campground['availability']= f"Not available from {start_date} through {end_date}"
        else:
            campground['availability']= 'Availability Unknown'
    avail_json['mapping_list'] = all_campsite_list

    return avail_json