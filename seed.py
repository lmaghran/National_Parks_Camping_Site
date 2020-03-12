from sqlalchemy import func
import json
from model import Campsite, Recreation_area, connect_to_db, db
from server import app

# Remove= {'2573', '2621', '2609', '2554', '2617', '2616', '2586', '2576', '2602', '2589'}

def load_campsites(campsite_filename):
    """Load campsite info into database."""
    np_id_list=[]
    print("Campsites")

    with open(campsite_filename) as json_file: 
        camp_file = json.load(json_file)

    with open("API_Data_Processing/nps_seed_info.txt") as json_file:
        np_data = json.load(json_file)

    for rec_dict in np_data:
        np_id_list.append(rec_dict["RecAreaID"])


# np_filename = "API_Data_Processing/nps_seed_info.txt"
# load_np(np_filename)

    for i, camp_dict in enumerate(camp_file):
        if camp_dict["ParentRecAreaID"] in np_id_list:
                facility_id= int(camp_dict["FacilityID"])
                parent_rec_area_id= int(camp_dict["ParentRecAreaID"])
                campsite_name= camp_dict["FacilityName"]
                campsite_lat= float(camp_dict["FacilityLatitude"])
                campsite_long= float(camp_dict["FacilityLongitude"])
                campsite_json_latlong = str(camp_dict["GEOJSON"])
                is_reservable = bool(camp_dict["Reservable"])
                campsite_type = camp_dict["FacilityTypeDescription"]
                campsite_description= camp_dict["FacilityDescription"]

                campsite= Campsite(
                            facility_id= facility_id,
                            parent_rec_area_id= parent_rec_area_id,
                            campsite_name= campsite_name,
                            campsite_lat= campsite_lat,
                            campsite_long= campsite_long,
                            campsite_json_latlong = campsite_json_latlong,
                            is_reservable = is_reservable,
                            campsite_type = campsite_type,
                            campsite_description= campsite_description)


            db.session.add(campsite)

            # provide some sense of progress
            if i % 100 == 0:
                print(i)

            db.session.commit()


def load_np(np_filename):
    """Load national parks info into database."""

    print("National Parks")

    with open(np_filename) as json_file: 
        np_file = json.load(json_file)


    for np_dict in np_file:
        rec_area_id = int(np_dict["RecAreaID"])
        rec_id_name = np_dict["OrgRecAreaID"]
        rec_name= np_dict["RecAreaName"]
        rec_area_des= np_dict["RecAreaDescription"]

        np= Recreation_area(
            rec_area_id = rec_area_id,
            rec_id_name = rec_id_name,
            rec_name= rec_name,
            rec_area_des= rec_area_des
            )

        db.session.add(np)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    campsite_filename = "API_Data_Processing/nps_cleaned_campsite_info.txt"
    np_filename = "API_Data_Processing/nps_seed_info.txt"
    load_np(np_filename)
    load_campsites(campsite_filename)