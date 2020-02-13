import requests
import json

nps_campsite_list= []
# parentid_types=set()

#opening the entire rec.gov campsite id dataset
with open("RecGov_json_storage.txt") as json_file: 
    data = json.load(json_file)


#Retrieving all of the NPS campgrounds (there are only 255), there are no null 
#ParentOrgIDs:
for rec_dict in data:
    if rec_dict["ParentOrgID"] == "128":
        
        accessable=rec_dict["FacilityAdaAccess"]

        if accessable.title()=="Y":
            rec_dict["FacilityAdaAccess"]=True
        
        elif accessable.title()=="N":
            rec_dict["FacilityAdaAccess"]=False

        nps_campsite_list.append(rec_dict)

print(len(nps_campsite_list))

with open("nps_cleaned_campsite_info.txt",'w') as cleaned_rec_storage_file:
    json.dump(nps_campsite_list, cleaned_rec_storage_file)