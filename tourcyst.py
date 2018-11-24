from flask import Flask, jsonify, request
import requests
from math import cos, sin, atan2, sqrt
import json

app = Flask(__name__)
rome2rio_key = 'yTPnfnRY'


def center_geolocation(geolocations):
    lat = []
    lng = []
    coordinates = {}
    for l in geolocations:
        lat.append(l[0])
        lng.append(l[1])
    coordinates['lat'] = sum(lat)/len(lat)
    coordinates['lng'] = sum(lng)/len(lng)
    return coordinates

@app.route('/auto/')
def autocomplete():
    query = request.args.get('query', '')
    data = get_autocomplete(query)
    return jsonify(data)

@app.route('/search')
def search():
    oName = request.args.get('from', '')
    dName = request.args.get('to', '')
    print(oName, dName)
    if(oName and dName):
      data = get_all_search(oName, dName)
    else:
      data = "Specify from and to locations"
    return jsonify(data)
  
@app.route('/geocode')
def geocode():
    query = request.args.get('query', '')
    data = get_geocode(query)
    return jsonify(data)

def get_geocode(query):
    payload = {"key":rome2rio_key, "query":query}
    response = requests.get("http://free.rome2rio.com/api/1.4/json/Geocode", params=payload)
    return response.json()

def get_all_search(place1, place2):
    payload = {"key":rome2rio_key, "oName" : place1, "dName": place2}
    response = requests.get("http://free.rome2rio.com/api/1.4/json/Search", params=payload)
    data = response.json()
    return data

def get_autocomplete(query):
    payload = {"key":rome2rio_key, "query":query}
    response = requests.get("http://free.rome2rio.com/api/1.4/json/Autocomplete", params=payload)
    data = response.json()
    return data


def find_centriod(place1, place2, place3):
    place1_loc = get_geocode(place1)
    place2_loc = get_geocode(place2)
    place3_loc = get_geocode(place3)
    place1_pair = (place1_loc["places"][0]["lat"], place1_loc["places"][0]["lng"])
    place2_pair = (place2_loc["places"][0]["lat"], place2_loc["places"][0]["lng"])
    place3_pair = (place3_loc["places"][0]["lat"], place3_loc["places"][0]["lng"])
    print(place1_pair, place2_pair, place3_pair)
    central = center_geolocation([place1_pair, place2_pair, place3_pair])
    print(central)
    return central


def get_places(pnt):
    lat_lng_str = str(pnt['lat']) + ',' + str(pnt["lng"])
    payload = {"location": lat_lng_str,"radius":500,"type":"airports","key": "AIzaSyCNa0G19BABRTzrn2AyO6VyClwhM3iilOw"}
    response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)
    print(response.places)
    # return response.json()

# find_centriod("Munich", "Madrid", "Paris")
get_places(find_centriod("Munich", "Madrid", "Paris"))


# # TODO: Rewrite to get_best_destination(place1, place2, place3)
# def get_best_destination():
#     cost_from_place1 = get_cheapest_route('munich', 'rome') + get_cheapest_route('paris', 'rome') + get_cheapest_route('london', 'rome')
#     cost_from_place2 = get_cheapest_route('munich', 'berlin') + get_cheapest_route('paris', 'berlin') + get_cheapest_route('london', 'berlin')
#     cost_from_place3 = get_cheapest_route('munich', 'madrid') + get_cheapest_route('paris', 'madrid') + get_cheapest_route('london', 'madrid')
#     print("Total prices per route: ",cost_from_place1, cost_from_place2, cost_from_place3)
#     print("Cheapest destination is ", 'Madrid', 'which costs ', get_cheapest_route('munich', 'madrid'), get_cheapest_route('paris', 'madrid'), get_cheapest_route('london', 'madrid'), " respectively.")

# get_best_destination()