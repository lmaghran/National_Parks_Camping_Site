from jinja2 import StrictUndefined
import requests
from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Campsite, Recreation_area
import random
from server_functions import rec_area_list, get_campsites, get_avail_dictionary, generate_campsite_dictionary, generate_availability_dictionary, get_nps_code, random_images, get_np_info

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key= "ABC"


@app.route("/", methods=['GET'])
def ran_np_photos():
#A list of all recreation areas that include campsites, in abc order
    rec_areas=rec_area_list()
    random_img_lst= random_images(rec_areas)
    
    return render_template("index.html", rec_areas=rec_areas, random_images= random_img_lst)



@app.route("/np_selected", methods=['GET'])
def get_np():

    rec_areas=rec_area_list()
    selected_area= request.args.get('rec_area')
    np_info= get_np_info(selected_area)
    description= np_info['description']

    return render_template("npselected.html", np_info=np_info, description=description, rec_areas=rec_areas)

@app.route("/api/np", methods=['GET'])
def get_nps_info():
    selected_area= request.args.get('rec_area')
    np_info= get_np_info(selected_area)
    return jsonify(np_info)


@app.route('/api/np_selected')
def return_np_avail():
#    """returns the availability for campsites in campgrounds in a national park"""
    avail_json= generate_availability_dictionary()
    return jsonify(avail_json)



if __name__ == "__main__": 

    app.debug = True #pragma: no cover
    connect_to_db(app) #pragma: no cover
    DebugToolbarExtension(app) #pragma: no cover
    app.run(host="0.0.0.0") #pragma: no cover