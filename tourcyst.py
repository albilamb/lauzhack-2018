from flask import Flask, jsonify, request, render_template
from flask_googlemaps import GoogleMaps, Map
import requests
from math import cos, sin, atan2, sqrt
import json
import pandas as pd
import numpy as np

app = Flask(__name__)
rome2rio_key = 'yTPnfnRY'

# Initialize the extension
GoogleMaps(app, key='AIzaSyDC5ccjS1Ig0lO8nzqVWUyNTgHv5PnBfFE')

mymap = Map(
        identifier="view-side",
        lat=46.537504,
        lng=6.613019,
        varname="jsmap"
)

@app.route('/update-marker')
def update_marker():
  lat = request.args.get('lat', '')
  lng = request.args.get('lng', '')
  mymap.add_marker(lat=float(lat), lng=float(lng))
  return jsonify(success=True)

@app.route('/')
def entry():
  
  return render_template('index.html', mymap=mymap)

@app.route('/auto/')
def autocomplete():
    query = request.args.get('query', '')
    data = get_autocomplete(query)
    return jsonify(data)


@app.route('/search')
def search():
    oName = request.args.get('from', '')
    dName = request.args.get('to', '')
    # print(oName, dName)
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


@app.route('/fastestplace/')
def fastestplace():
    place1 = request.args.get('place1', '')
    place2 = request.args.get('place2', '')
    place3 = request.args.get('place3', '')
    data = get_fastest_central(place1, place2, place3)
    # print(data)
    return jsonify(data)


@app.route('/cheapestplace/')
def cheapestplace():
    place1 = request.args.get('place1', '')
    place2 = request.args.get('place2', '')
    place3 = request.args.get('place3', '')
    data = get_cheapest_central(place1, place2, place3)
    # print("hello" + data)
    return jsonify(data)


@app.route('/allplaces/')
def findall():
    place1 = request.args.get('place1', '')
    place2 = request.args.get('place2', '')
    place3 = request.args.get('place3', '')
    data = get_places(find_centriod(place1, place2, place3), place1, place2, place3)
    return jsonify(data)


@app.route('/placedetails/')
def placedetails():
    place = request.args.get('place', '')
    data = get_geocode(place)
    return jsonify(data)


# Helper fuctions

def get_fastest_central(place1, place2, place3):
    central = get_places(find_centriod(place1, place2, place3), place1, place2, place3)
    transits = []
    for c in central:
        transit_map = {}
        transit1 = get_all_search(place1, c["name"])[
            "routes"][0]["totalTransitDuration"]
        transit2 = get_all_search(place2, c["name"])[
            "routes"][0]["totalTransitDuration"]
        transit3 = get_all_search(place3, c["name"])[
            "routes"][0]["totalTransitDuration"]
        transit_map["name"] = c["name"]
        transit_map["total_transit"] = transit1 + transit2 + transit3
        transits.append(transit_map)
    best_location = get_fastest_transit_central(transits)
    return best_location


def get_cheapest_central(place1, place2, place3):
    central = get_places(find_centriod(place1, place2, place3), place1, place2, place3)
    transits = []
    for c in central:
        transit_map = {}
        price1 = get_all_search(place1, c["name"])["routes"][0]["indicativePrices"][0]["price"]
        price2 = get_all_search(place1, c["name"])["routes"][0]["indicativePrices"][0]["price"]
        price3 = get_all_search(place1, c["name"])["routes"][0]["indicativePrices"][0]["price"]
        transit_map["name"] = c["name"]
        transit_map["total_price"] = price1 + price2 + price3
        print("name: " + c["name"] + ", " +
              "price: " + str(price1 + price2 + price3))
        transits.append(transit_map)

    best_location = get_cheapest_transit_central(transits)
    return best_location


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


def get_geocode(query):
    payload = {"key": rome2rio_key, "query": query}
    response = requests.get(
        "http://free.rome2rio.com/api/1.4/json/Geocode", params=payload)
    return response.json()


def get_all_search(place1, place2):
    payload = {"key": rome2rio_key, "oName": place1, "dName": place2}
    response = requests.get(
        "http://free.rome2rio.com/api/1.4/json/Search", params=payload)
    data = response.json()
    return data


def get_autocomplete(query):
    payload = {"key": rome2rio_key, "query": query}
    response = requests.get(
        "http://free.rome2rio.com/api/1.4/json/Autocomplete", params=payload)
    data = response.json()
    return data


def find_centriod(place1, place2, place3):
    place1_loc = get_geocode(place1)
    place2_loc = get_geocode(place2)
    place3_loc = get_geocode(place3)
    place1_pair = (place1_loc["places"][0]["lat"],
                   place1_loc["places"][0]["lng"])
    place2_pair = (place2_loc["places"][0]["lat"],
                   place2_loc["places"][0]["lng"])
    place3_pair = (place3_loc["places"][0]["lat"],
                   place3_loc["places"][0]["lng"])
    # print(place1_pair, place2_pair, place3_pair)
    central = center_geolocation([place1_pair, place2_pair, place3_pair])
    # print(central)
    return central


def get_places(pnt, place1, place2, place3):
    lat_lng_str = str(pnt['lat']) + ',' + str(pnt["lng"])
    payload = {"location": lat_lng_str, "radius": 500, "type": "airports",
               "key": "AIzaSyCNa0G19BABRTzrn2AyO6VyClwhM3iilOw"}

    # response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)
    # place = {"name": response.json()['results'][0]["name"], "lat": response.json()['results'][0]["geometry"]["location"]["lat"], "lng": response.json()['results'][0]["geometry"]["location"]["lng"]}
    # print(place)
    # data = response.json()
    city_list_df = pd.read_csv('biggest_cities.csv', sep=";")
    city_list_df = city_list_df[(city_list_df.name != place1) &
                                (city_list_df.name != place2) &
                                (city_list_df.name != place3)]
    rnge = 5
    l = []
    test_df = city_list_df
    lat_0 = pnt['lat']
    lng_0 = pnt['lng']
    test_df = test_df[(test_df.lat > lat_0 - rnge) &
                      (test_df.lat < lat_0 + rnge)]
    test_df = test_df[(test_df.lng > lng_0 - rnge) &
                      (test_df.lng < lng_0 + rnge)]
    print(test_df)
    possible_pts = test_df.reset_index()
    for index, row in possible_pts.iterrows():
        l += [{'lat': row['lat'], 'lng': row['lng'], 'name': row['name']}]

    response = l
#    data=response.json()
    data = response
    places = []
    length = len(data)
    for i in range(length):
        dict = {}
        dict = {'lat': data[i]["lat"], 'lng': data[i]["lng"],
                'name': data[i]["name"]}
        places.append(dict)
    # print("Places: " + str(data))
    return places

#    return response
#    length=len(data['results'])
#    for i in range(length):
#        dict = {}
#        dict={'lat': data["results"][i]["geometry"]["location"]["lat"], 'lng':data["results"][i]["geometry"]["location"]["lng"],
#                 'name':data["results"][i]["name"]}
#        places.append(dict)
#    print("Places: " + str(places))
#    return places


def get_fastest_transit_central(transits):
    best_transit = transits[0]["total_transit"]
    best_location = transits[0]["name"]
    for i in range(len(transits)):
        if transits[i]["total_transit"] <= best_transit:
            best_transit = transits[i]["total_transit"]
            best_location = transits[i]["name"]
    return best_location


def get_cheapest_transit_central(transits):
    best_transit = transits[0]["total_price"]
    best_location = transits[0]["name"]
    for i in range(len(transits)):
        if transits[i]["total_price"] <= best_transit:
            best_transit = transits[i]["total_price"]
            best_location = transits[i]["name"]
    return best_location


def get_metrics_for_search(place1, place2):
    metrics = []
    routes = get_all_search(place1, place2)["routes"]
    for i in range(len(routes)):
        route = {}
        route["id"] = i
        route["name"] = routes[i]["name"]
        route["totalDuration"] = routes[i]["totalDuration"]
        route["totalTransitDuration"] = routes[i]["totalTransitDuration"]
        route["indicativePrice"] = routes[i]["indicativePrices"][0]["price"]
        metrics.append(route)
    return metrics


def get_recommended_central(place1, place2, place3):
    centrals = get_places(find_centriod(
        place1, place2, place3), place1, place2, place3)
    # TODO: Recommender logic goes here
    return central


# def get_cheapest_route(place1, place2, place3):
#     print("Places: " + str(place1) + " " + str(place2) + " " + str(place3))
#     central = get_places(find_centriod(place1, place2, place3))
#     print("Best fit place: " + str(central))
#     best_cost_from_place1 = get_all_search(place1, central["name"])["routes"][0]["indicativePrices"][0]["price"]
#     best_cost_from_place2 = get_all_search(place2, central["name"])["routes"][0]["indicativePrices"][0]["price"]
#     best_cost_from_place3 = get_all_search(place3, central["name"])["routes"][0]["indicativePrices"][0]["price"]

#     print("Costs from each place is " + str(best_cost_from_place1) + " " + str(best_cost_from_place2) + " " + str(best_cost_from_place3) + " USD respectively")


# def get_fastest_route(place1, place2, place3):
#     print("Places: " + str(place1) + " " + str(place2) + " " + str(place3))
#     central = get_places(find_centriod(place1, place2, place3))
#     print("Best fit place: " + str(central))
#     best_cost_from_place1 = get_all_search(place1, central["name"])["routes"][0]["totalTransitDuration"]
#     best_cost_from_place2 = get_all_search(place2, central["name"])["routes"][0]["totalTransitDuration"]
#     best_cost_from_place3 = get_all_search(place3, central["name"])["routes"][0]["totalTransitDuration"]

#     print("Distances from each place is " + str(best_cost_from_place1) + " " + str(best_cost_from_place2) + " " + str(best_cost_from_place3) + "minutes respectively")


# find_centriod("Munich", "Madrid", "Paris")
# print(get_cheapest_central("Munich", "Madrid", "Paris"))
# get_fastest_route("Munich", "Madrid", "Paris")
# print(get_metrics_for_search("Munich", "Paris"))

# find_centriod("Munich", "Berlin", "Hyderabad")

# # TODO: Rewrite to get_best_destination(place1, place2, place3)
# def get_best_destination():
#     cost_from_place1 = get_cheapest_route('munich', 'rome') + get_cheapest_route('paris', 'rome') + get_cheapest_route('london', 'rome')
#     cost_from_place2 = get_cheapest_route('munich', 'berlin') + get_cheapest_route('paris', 'berlin') + get_cheapest_route('london', 'berlin')
#     cost_from_place3 = get_cheapest_route('munich', 'madrid') + get_cheapest_route('paris', 'madrid') + get_cheapest_route('london', 'madrid')
#     print("Total prices per route: ",cost_from_place1, cost_from_place2, cost_from_place3)
#     print("Cheapest destination is ", 'Madrid', 'which costs ', get_cheapest_route('munich', 'madrid'), get_cheapest_route('paris', 'madrid'), get_cheapest_route('london', 'madrid'), " respectively.")

# get_best_destination()