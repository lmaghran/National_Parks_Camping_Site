from jinja2 import StrictUndefined
import requests
from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Campsite, Recreation_area
from server_functions import rec_area_list, get_campsites, get_avail_dictionary, generate_campsite_dictionary, all_campsites

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
    print(avail_json.keys())
 
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