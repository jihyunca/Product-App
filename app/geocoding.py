import pandas as pd
import re as re
import json
import requests


# MapQuest API Key
apikey = 'qeLyYlV7U0uZFLBBs5QqjacX5Lio4wM1'

def postal_geocode(user_address):
	""" Geocodes the addresses in the data frame that are the closest to user_address """

	data = pd.read_csv(('/Users/KIMJI/Desktop/Product-App/app/geodata.csv'))
	data['LONGITUDE'] = data['LONGITUDE'].astype(float)
	data['LATITUDE'] = data['LATITUDE'].astype(float)
	URL = 'http://open.mapquestapi.com/geocoding/v1/address?key=' + apikey

	PARAMS = {
      "location": user_address
    }


	r = requests.post(url= URL, json = PARAMS)

	r = json.loads(r.text)
	latit  = r['results'][0]['locations'][0]['latLng']['lat']
	longit = r['results'][0]['locations'][0]['latLng']['lng']

 
	stores_to_find = 5

	mile = 0.1
	data = data[(((data['LATITUDE']  <= (latit + mile)) & (data['LATITUDE'] >= (latit-mile)) &
               ((data['LONGITUDE'] >= (longit-mile)) & (data['LONGITUDE'] <= (longit+mile)))))]
	data = data.drop_duplicates(subset=('ADDRESS'), keep='first')
	return(data)


def buildURL (store_addresses):
	""" Builds the URL for the Mapquest POST Request """
	startURL = "https://www.mapquestapi.com/staticmap/v5/map?locations="
	result = "".join("%s||" % address for address in store_addresses)
	endURL = "||&size=300,300&&defaultMarker=marker-7B0099&key=" + apikey
	URL = startURL + result + endURL
	print(URL)
	return URL

def createMap(data, store_list):
	""" produces a map using the MapQuest API with each store in store_list marked """
	store_addresses = []
	for store in store_list:
				store_addresses.append(data['POSTAL_CODE'][data['STORE_ID']==store].iloc[0])

	mapURL = buildURL(store_addresses)
	return mapURL