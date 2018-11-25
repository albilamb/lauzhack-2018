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
        varname="jsmap",
        zoom=5
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
    place1 = request.args.get('place1', '')
    place2 = request.args.get('place2', '')
    place3 = request.args.get('place3', '')
    query = request.args.get('query', '')
    transit_map = []
    transit1 = get_all_search(place1, query)[
        "routes"][0]
    transit_map.append(transit1)
    transit2 = get_all_search(place2, query)[
        "routes"][0]
    transit_map.append(transit2)
    transit3 = get_all_search(place3, query)[
        "routes"][0]
    transit_map.append(transit3)
    return jsonify(transit_map)


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
        indicative1 = get_all_search(place1, c["name"])["routes"][0]
        indicative2 = get_all_search(place1, c["name"])["routes"][0]
        indicative3 = get_all_search(place1, c["name"])["routes"][0]
        if("indicativePrices" in indicative1) and ("indicativePrices" in indicative2) and ("indicativePrices" in indicative3):
            price1 = indicative1["indicativePrices"][0]['price']
            price2 = indicative2["indicativePrices"][0]['price']
            price3 = indicative3["indicativePrices"][0]['price']
            transit_map["name"] = c["name"]
            transit_map["total_price"] = price1 + price2 + price3
            # print("name: " + c["name"] + ", " +
            #       "price: " + str(price1 + price2 + price3))
            transits.append(transit_map)
    if not transits:
        return get_fastest_central(place1, place2, place3)
    else:
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
    payload = {"key": rome2rio_key, "oName": place1, "dName": place2, "noAir": True, "noCar" : True}
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


def get_more_places(pnt):
    lat_lng_str = str(pnt['lat']) + ',' + str(pnt["lng"])
    payload = {"location": lat_lng_str, "radius": 50,
               "type": "airports", "key": "AIzaSyCNa0G19BABRTzrn2AyO6VyClwhM3iilOw"}
    response = requests.get(
        "https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)
    # place = {"name": response.json()['results'][0]["name"], "lat": response.json()['results'][0]["geometry"]["location"]["lat"], "lng": response.json()['results'][0]["geometry"]["location"]["lng"]}
    # print(place)
    data = response.json()
    places = []
    length = len(data['results'])
    if length >= 5:
        for i in range(5):
            dict = {}
            dict = {'lat': data["results"][i]["geometry"]["location"]["lat"], 'lng': data["results"][i]["geometry"]["location"]["lng"],
                    'name': data["results"][i]["name"], "exotic": True}
            places.append(dict)
    else:
        for i in range(length):
            dict = {}
            dict = {'lat': data["results"][i]["geometry"]["location"]["lat"], 'lng': data["results"][i]["geometry"]["location"]["lng"],
                    'name': data["results"][i]["name"], "exotic": True}
            places.append(dict)
    return places


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
    data = response
    places = []
    length = len(data)
    for i in range(length):
        dict = {}
        dict = {'lat': data[i]["lat"], 'lng': data[i]["lng"],
                'name': data[i]["name"]}
        places.append(dict)
    more_places = get_more_places(pnt)
    places = places + more_places
    return places


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


@app.route('/recommended/')
def recommended_route():
    place1 = request.args.get('place1', '')
    place2 = request.args.get('place2', '')
    place3 = request.args.get('place3', '')
    best_location=get_fastest_central(place1, place2, place3)
    route_map=[]
    route1=cent1(place1,best_location)
    route2=cent1(place2,best_location)
    route3=cent1(place3,best_location)
    route_details={}
    route_details['place1']=route1
    route_details['place2']=route2
    route_details['place3']=route3
    route_map.append(route_details)#->best_location
    return jsonify(route_map)
    
def cent1(place1,place2):
    metrics = []
    routes = get_all_search(place1, place2)["routes"]
    for i in range(len(routes)):
        route = {}
        route["id"] = i
        route["name"] = routes[i]["name"]
        route["totalDuration"]  = routes[i]["totalDuration"]
        #route["totalTransitDuration"]  = routes[i]["totalTransitDuration"]
        route["indicativePrice"] = routes[i]["indicativePrices"][0]["price"]
        metrics.append(route)
    #print metrics
    
    length=len(metrics)
    my_dict2=[]
    for i in range(length):
        my_dict2.append({"Duration":metrics[i]['totalDuration'],"Name":metrics[i]['name'].encode('utf-8'),
                         "Price":metrics[i]['indicativePrice']})#,"Id":metrics[i]['id']})
        #output -> {'Duration': 325, 'Price': 167, 'Name': 'Fly Paris CDG to Birmingham, train'}
        
    #print my_dict2
    sorted_list=sorted(my_dict2, key=lambda k: k['Duration'])
    #print sorted_list
    length=len(sorted_list)
    optimised=int(length/2)
    return sorted_list[optimised]
    #print statistics.median(my_dict2[0])#, key=lambda k: k['Duration'])#sorted(my_dict2, key=lambda k: k['Duration'])
