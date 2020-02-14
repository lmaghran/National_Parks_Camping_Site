import requests
import json
import os

missing_campsite_rec_id_list=[]
np_id_list= []
key_error_set= set()

with open("nps_cleaned_campsite_info.txt") as json_file:
    campsite_data = json.load(json_file)

with open("nps_seed_info.txt") as json_file:
    np_data = json.load(json_file)

for rec_dict in np_data:
    np_id_list.append(rec_dict["RecAreaID"])

for camp_rec_dict in campsite_data:
    if camp_rec_dict["ParentRecAreaID"] not in np_id_list:
        missing_campsite_rec_id_list.append(camp_rec_dict)

with open("Campsite_no_np.txt",'w') as rec_storage_file:
    json.dump(missing_campsite_rec_id_list, rec_storage_file)

print(len(missing_campsite_rec_id_list))
# for i, num in enumerate(campsite_rec_id_list):
#     if num not in np_id_list:
#         key_error_set.add(num)

# print(key_error_set)
# print(len(key_error_set))
