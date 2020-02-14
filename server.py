from jinja2 import StrictUndefined
import requests
from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Campsite, Recreation_area

headers={'User-Agent': 'Mozilla/5.0'}

app = Flask(__name__)

# # Required to use Flask sessions and the debug toolbar
# app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

app = Flask(__name__)


@app.route("/", methods=['GET'])
def homepage():
    """Show the homepage."""
    #A list of all recreation areas that include campsites, in abc order
    rec_areas=Recreation_area.query.filter(Recreation_area.campsites != None).\
            order_by(Recreation_area.rec_name).all()

    return render_template("index.html", rec_areas=rec_areas)


@app.route('/np_selected', methods=['GET'])
def return_np_avail():
#    """returns the availibility for campsites"""
    availibility_list=[]
    selected_area= request.args.get('rec_area')
    start_date=request.args.get('start-date')
    end_date=request.args.get('end-date')
    print(start_date)
    print(end_date)

    rec_area=Recreation_area.query.filter(Recreation_area.rec_name==selected_area).first()
    selected_campsites= rec_area.campsites

    for campsite in selected_campsites:
        camp_id= campsite.facility_id
        availibility_url=f'http://www.recreation.gov/api/camps/availability/campground/{camp_id}?start_date={start_date}T00%3A00%3A00.000Z&end_date={end_date}T00%3A00%3A00.000Z'
        avail_response = requests.get(availibility_url, headers=headers)
        avail_json_response= avail_response.json()
        dict_keys= avail_dict['campsites'].keys()
#########################stopping point- need to format for a better response
        availibility_list.append(avail_json_response) 

    return render_template("np_selected.html", 
                            rec_area=rec_area, 
                            selected_campsites= selected_campsites, 
                            availibility_list= availibility_list)


if __name__ == "__main__":

    # app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
