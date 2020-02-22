from jinja2 import StrictUndefined
import requests
from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Campsite, Recreation_area
from server_functions import rec_area_list, get_campsites, get_avail_dictionary, generate_campsite_dictionary

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key= "ABC"

@app.route("/", methods=['GET'])
def homepage():
    """Show the homepage."""
    #A list of all recreation areas that include campsites, in abc order
    rec_areas=rec_area_list()
    
    return render_template("index.html", rec_areas=rec_areas)


@app.route('/api/np_selected')
def return_np_avail():
#    """returns the availibility for campsites in campgrounds in a national park"""

    selected_area= request.args.get('rec_area')
    start_date=request.args.get('start-date')
    end_date=request.args.get('end-date')
    selected_campsites= get_campsites(selected_area)
    avail_json= generate_campsite_dictionary(selected_campsites, start_date, end_date)
    
    return avail_json

@app.route('/api/all_campground_geodata')

def return_all_campsite_geodata():

    all_campsite_list=[]
    all_campsites= Campsite.query.filter(Campsite.facility_id!= None).\
    order_by(Campsite.campsite_name).all()

    for campsite in all_campsites:
        all_campsite_geodata={}
        all_campsite_geodata['campground_name']=campsite.campsite_name
        all_campsite_geodata['facility_id']= campsite.facility_id
        all_campsite_geodata['lat']= campsite.campsite_lat
        all_campsite_geodata['long']= campsite.campsite_long
        all_campsite_list.append(all_campsite_geodata)
    all_campsite_list= jsonify(all_campsite_list)

    return all_campsite_list



if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")