import requests
import json
import os

json_set=set()

with open("nps_seed_info.txt") as json_file:
    data = json.load(json_file)

for rec_dict in data:
    json_set.add(rec_dict["RecAreaID"])

print(len(json_set))