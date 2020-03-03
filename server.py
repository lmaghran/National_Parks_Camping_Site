from jinja2 import StrictUndefined
import requests
from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Campsite, Recreation_area
import random
from server_functions import rec_area_list, get_campsites, get_avail_dictionary, generate_campsite_dictionary, all_campsites, generate_availibility_dictionary, get_nps_code, random_images

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key= "ABC"


@app.route("/", methods=['GET'])
def homepage():
    """Show the homepage."""
    #A list of all recreation areas that include campsites, in abc order
    rec_areas=rec_area_list()
    random_img_lst= random_images(rec_areas)
    
    return render_template("index.html", rec_areas=rec_areas, random_images= random_img_lst)


@app.route('/api/np_selected')
def return_np_avail():
#    """returns the availibility for campsites in campgrounds in a national park"""

    avail_json= generate_availibility_dictionary()

    return jsonify(avail_json)

@app.route('/api/all_campground_geodata')

def return_all_campsite_geodata():

    all_campsite_list= all_campsites()
    all_campsite_list = jsonify(all_campsite_list)
    return all_campsite_list



if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")