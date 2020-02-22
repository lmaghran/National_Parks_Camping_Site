from model import connect_to_db, db, Campsite, Recreation_area
from flask import Flask, jsonify, render_template, request
import requests

# def rec_area_list():
#     print(Recreation_area)
#     rec_areas=Recreation_area.query.filter(Recreation_area.campsites != None).\
#             order_by(Recreation_area.rec_name).all()

#     return rec_areas

def rec_area_list():

    rec_areas=Recreation_area.query.filter(Recreation_area.campsites != None).\
            order_by(Recreation_area.rec_name).all()

    return rec_areas

def get_campsites(selected_area):

    #querying for name of rec area
    rec_area=Recreation_area.query.filter(Recreation_area.rec_name==selected_area).first()
    selected_campsites= rec_area.campsites

    return selected_campsites

def get_avail_dictionary(camp_id, start_date, end_date):
    headers={'User-Agent': 'Mozilla/5.0', "accept": "application/json" }
    availibility_url=f'http://www.recreation.gov/api/camps/availability/campground/{camp_id}?start_date={start_date}T00%3A00%3A00.000Z&end_date={end_date}T00%3A00%3A00.000Z'
    avail_json_response = requests.get(availibility_url, headers={'User-Agent': 'Mozilla/5.0', "accept": "application/json" })
    avail_dict_response= avail_json_response.json() ### this is a dictionary

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

    avail_json= jsonify(campsite_dictionary)
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


    jsonify(all_campsite_geodata)
    return 

def all_campsites():
    all_campsites= Campsite.query.filter(Campsite.facility_id!= None).\
    order_by(Campsite.campsite_name).all()

    return all_campsites