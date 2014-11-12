import time
from geopy.geocoders import GoogleV3
geolocator = GoogleV3()

with open("restaurant.csv", "r") as datafile:
	data_rows = datafile.read().splitlines()
	
for index, row in enumerate(data_rows):
	data_rows[index] = row.split(",")
	
header = data_rows.pop(0)

nestdict = {}
for index,row in enumerate(data_rows):
	line = {}
	for key, value in zip(header, row):
		line[key]=value
		nestdict[index]=line

GeoJSON_objects=[]
for key in nestdict:
	time.sleep(1)
	try:
		address, (latitude, longitude) = geolocator.geocode("{0} {1} {2}".format(nestdict[key]["Address"],nestdict[key]["City"], nestdict[key]["State"]))
	except:
		print "Unable to find location for" , key 
		
	else:
		object = {
		"type": "Feature", 
		"geometry": {
			"type": "Point", 
			"coordinates" : [
			longitude, 
			latitude
			]
		},
		"properties": {
				"marker-symbol": "restaurant", 
				"name": nestdict[key]["Restaurant"], 
				"address": nestdict[key]["Address"], 
				"cuisine": nestdict[key]["Cuisine"],  
				"price": nestdict[key]["Dollar"],
		}
	}
	
	GeoJSON_objects.append(object)

geo={
		"type":"FeatureCollection", 
		"features": GeoJSON_objects
}

import json

with open("100_restaurants_dc.json", "w") as jsonfile:
	jsonfile.write(json.dumps(geo, indent=4, sort_keys=True)) 