from jinja2 import StrictUndefined
import requests
from flask import Flask, jsonify, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Campsite, Recreation_area



app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.secret_key= "ABC"
headers={'User-Agent': 'Mozilla/5.0', "accept": "application/json" }


@app.route("/", methods=['GET'])
def homepage():
    """Show the homepage."""
    #A list of all recreation areas that include campsites, in abc order
    rec_areas=Recreation_area.query.filter(Recreation_area.campsites != None).\
            order_by(Recreation_area.rec_name).all()

    return render_template("index.html", rec_areas=rec_areas)


@app.route('/api/np_selected')
def return_np_avail():
#    """returns the availibility for campsites"""

    campsite_dictionary={}
    availible_campsite_list=[]
    selected_area= request.args.get('rec_area')
    start_date=request.args.get('start-date')
    end_date=request.args.get('end-date')
    #querying for name of rec area
    rec_area=Recreation_area.query.filter(Recreation_area.rec_name==selected_area).first()
    selected_campsites= rec_area.campsites #all campsites within the national park

    for campsite in selected_campsites: # circling through list of campsites in a National Park
        camp_id= campsite.facility_id
        availibility_url=f'http://www.recreation.gov/api/camps/availability/campground/{camp_id}?start_date={start_date}T00%3A00%3A00.000Z&end_date={end_date}T00%3A00%3A00.000Z'
        avail_response = requests.get(availibility_url, headers=headers)
        avail_json_response= avail_response.json() ### this is a dictionary
        campsite_dictionary[campsite.campsite_name]= avail_json_response
        campsite_dictionary["campground_lat"]= campsite.campsite_lat
        campsite_dictionary["campground_long"]= campsite.campsite_long
        for site in campsite_dictionary[campsite.campsite_name]['campsites']:
            dates_stayed= len(campsite_dictionary[campsite.campsite_name]['campsites'][site]['availabilities'])
            i=0
            for availability in campsite_dictionary[campsite.campsite_name]['campsites'][site]['availabilities']:
                if campsite_dictionary[campsite.campsite_name]['campsites'][site]['availabilities'][availability]=="Available":
                    i+=1

            if i==dates_stayed:
                availible_campsite_list.append(campsite_dictionary[campsite.campsite_name]['campsites'][site])
    campsite_dictionary["availibility_data"]=availible_campsite_list
    
                # if campsite_dictionary[campsite.campsite_name]['campsites'][site]['availabilities']=="Available":
                #     print(campsite_dictionary[campsite.campsite_name]['campsites'][site]['availabilities'])
                #     i+=1
            # for days in campsite_dictionary[campsite.campsite_name]['campsites'][site]['availabilities']:
            #     print(len(campsite_dictionary[campsite.campsite_name]['campsites'][site]['availabilities']))
        
        # # print(avail_json_response['campsites'])
        # for site in avail_json_response["campsites"]:
        #     # print(avail_json_response["campsites"][site])
        #     # all_campsite_availibility= avail_list.append(site)
        #     if avail_json_response["campsites"][site]['type_of_use']== 'Overnight':
        #         campsite_dictionary[camp_id]= (site, avail_json_response["campsites"][site]['availabilities'])
        #         availibility= avail_json_response["campsites"][site]['availabilities']
        #         print(type(availibility))

        #     else:
        #         campsite_dictionary[camp_id]= (site,"Day use only")

    # print(campsite_dictionary)
    # # campsite_dictionary= campsite_dictionary)
    avail_json= jsonify(campsite_dictionary)
    return avail_json


if __name__ == "__main__":

    app.debug = True
    connect_to_db(app)
    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")
