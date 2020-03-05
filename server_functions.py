from model import connect_to_db, db, Campsite, Recreation_area
from flask import Flask, jsonify, render_template, request
import requests
import os
import random


# def rec_area_list():
#     print(Recreation_area)
#     rec_areas=Recreation_area.query.filter(Recreation_area.campsites != None).\
#             order_by(Recreation_area.rec_name).all()

#     return rec_areas

def rec_area_list():

    rec_areas=Recreation_area.query.filter(Recreation_area.campsites != None).\
            order_by(Recreation_area.rec_name).all()

    return rec_areas

def random_images(rec_areas):
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

    #querying for name of rec area
    rec_area=Recreation_area.query.filter(Recreation_area.rec_name==selected_area).first()
    nps_code= rec_area.rec_id_name

    return nps_code

def get_np_info(selected_area):
    working_Url= "https://developer.nps.gov/api/v1/parks?parkCode=YELL&fields=images&api_key=LhjXYnr7nnTeOSqGDAblu63wpF7a99ml5ahZWzFE"
    nps_api_key= os.environ['NPS_API_KEY']
    headers = {"apikey": os.environ['NPS_API_KEY'], "accept": "application/json"}
    nps_code= get_nps_code(selected_area)
    url = f"https://developer.nps.gov/api/v1/parks?parkCode={nps_code}&fields=images&api_key={nps_api_key}"
    response = requests.get(url, headers=headers)
    json_resp= response.json()
    np_info=json_resp['data'][0]

    return np_info


def get_nps_photos(nps_code):

    working_Url= "https://developer.nps.gov/api/v1/parks?parkCode=YELL&fields=images&api_key=LhjXYnr7nnTeOSqGDAblu63wpF7a99ml5ahZWzFE"
    nps_api_key= os.environ['NPS_API_KEY']
    headers = {"apikey": os.environ['NPS_API_KEY'], "accept": "application/json"}
    url = f"https://developer.nps.gov/api/v1/parks?parkCode={nps_code}&fields=images&api_key={nps_api_key}"
    response = requests.get(url, headers=headers)
    json_resp= response.json()
    image_list=json_resp['data'][0]['images']

    return image_list



def get_campsites(selected_area):

    #querying for name of rec area
    rec_area=Recreation_area.query.filter(Recreation_area.rec_name==selected_area).first()
    selected_campsites= rec_area.campsites

    return selected_campsites

def get_avail_dictionary(camp_id, start_date, end_date):
    headers={'User-Agent': 'Mozilla/5.0', "accept": "application/json" }
    print(start_date)
    print(end_date)
    availibility_url=f'http://www.recreation.gov/api/camps/availability/campground/{camp_id}?start_date={start_date}T00%3A00%3A00.000Z&end_date={end_date}T00%3A00%3A00.000Z'
    avail_json_response = requests.get(availibility_url, headers={'User-Agent': 'Mozilla/5.0', "accept": "application/json" })
    avail_dict_response= avail_json_response.json() ### this is a dictionary

    print(avail_dict_response)
    return avail_dict_response



def generate_campsite_dictionary(selected_campsites, start_date, end_date):

    campsite_dictionary={}
    availible_campsite_list=[]

    for campsite in selected_campsites: # circling through list of campsites in a National Park
        camp_id= campsite.facility_id
        avail_dict= get_avail_dictionary(camp_id, start_date, end_date)
        # campsite_dictionary[campsite.campsite_name]= avail_json_response
        campsite_dictionary[campsite.campsite_name]= {}
        campsite_dictionary[campsite.campsite_name]["campground_lat"]= campsite.campsite_lat
        campsite_dictionary[campsite.campsite_name]["campground_long"]= campsite.campsite_long
        campsite_dictionary[campsite.campsite_name]["campground_id"]= campsite.facility_id
        for site in avail_dict['campsites']:
            dates_stayed= len(avail_dict['campsites'][site]['availabilities'])
            i=0
            for availability in avail_dict['campsites'][site]['availabilities']:
                if avail_dict['campsites'][site]['availabilities'][availability]=="Available":
                    i+=1

            if i==dates_stayed:
                availible_campsite_list.append(avail_dict['campsites'][site])
    
    if len(availible_campsite_list)!=0:
        campsite_dictionary[campsite.campsite_name]["availibility_data"]=availible_campsite_list

    avail_json= campsite_dictionary
    return avail_json


def return_cg_lat_long():
    all_campsites= Campsite.query.filter(Campsite.facility_id!= None).\
            order_by(Campsite.campsite_name).all()

    all_campsite_geodata={}
    for campsite in all_campsites:
        all_campsite_geodata[campsite.campsite_name]={}
        all_campsite_geodata[campsite.campsite_name]['facility_id']= campsite.facility_id
        all_campsite_geodata[campsite.campsite_name]['campsite_lat']= campsite.campsite_lat
        all_campsite_geodata[campsite.campsite_name]['campsite_long']= campsite.campsite_long
        all_campsite_geodata[campsite.campsite_name]['availibility']= 'unknown'


    jsonify(all_campsite_geodata)
    return

def generate_availibility_dictionary():
    ## Returns dictionary for mapping and availibility
    avail_json={}
    availible_campsite_list=[]
    selected_campsites= []
    np_campground_names=[]

    all_campsite_list=[]
    all_campsites= Campsite.query.filter(Campsite.facility_id!= None).order_by(Campsite.campsite_name).all()

    for campsite in all_campsites:
        all_campsite_geodata={}
        all_campsite_geodata['campground_name']=campsite.campsite_name
        all_campsite_geodata['facility_id']= campsite.facility_id
        all_campsite_geodata['lat']= campsite.campsite_lat
        all_campsite_geodata['long']= campsite.campsite_long
        all_campsite_geodata['availibility']= 'unknown'
        all_campsite_list.append(all_campsite_geodata)

    if request.args.get('rec_area') != None:
        selected_area= request.args.get('rec_area')
    if request.args.get('start-date') != None:
        start_date=request.args.get('start-date')
    if request.args.get('end-date') != None:
        end_date=request.args.get('end-date')
        selected_campsites= get_campsites(selected_area)
        avail_json= generate_campsite_dictionary(selected_campsites, start_date, end_date)
        # avail_json['images']= image_list
    for campsite in selected_campsites:
        np_campground_names.append(campsite.campsite_name)
    # renames items based on their availibility
    for campground in all_campsite_list:
        name= campground['campground_name']

        if name in np_campground_names:
            if avail_json[name].get('availibility_data') != None:
                campground["availibility"]= 'Availible for these dates'
            else:
                campground['availibility']= 'Not availible for these dates'
        else:
            campground['availibility']= 'Availibility Unknown'

    avail_json['mapping_list'] = all_campsite_list
    return avail_json