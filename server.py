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

    all_campsite_list= all_campsites()
    if request.args.get('rec_area') != None:
        selected_area= request.args.get('rec_area')

    if request.args.get('start-date') != None:
        start_date=request.args.get('start-date')

    if request.args.get('end-date') != None:
        end_date=request.args.get('end-date')

        selected_campsites= get_campsites(selected_area)
        avail_json= generate_campsite_dictionary(selected_campsites, start_date, end_date)


    all_campsite_list= all_campsites()

    for campsite in all_campsite_list:
        if campsite["campground_name"] in selected_campsites:      
            
            if avail_json[campsite.campsite_name].get("availibility_data") != None:
                campsite["availibility"]= 'Availible for these dates'
/////////////////////////////////////////////////////////////////////////////////Stopped here

            else:
                all_campsite_geodata['availibility']= 'Not availible for these dates'

        else:
            all_campsite_geodata['availibility']= 'Availibility Unknown'

    avail_json['mapping_list'] = all_campsite_list
 
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