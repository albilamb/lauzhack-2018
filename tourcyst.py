from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)
rome2rio_key = 'yTPnfnRY'
 
@app.route('/auto/')
def autocomplete():
    query = request.args.get('query', '')
    data = get_autocomplete(query)
    return data

@app.route('/search')
def search():
    oName = request.args.get('from', '')
    dName = request.args.get('to', '')
    print(oName, dName)
    if(oName and dName):
      data = get_all_search(oName, dName)
    else:
      data = "Specify from and to locations"
    return data
  
@app.route('/geocode')
def geocode():
    query = request.args.get('query', '')
    data = get_geocode(query)
    return data

def get_geocode(query):
    payload = {"key":rome2rio_key, "query":query}
    response = requests.get("http://free.rome2rio.com/api/1.4/json/Geocode", params=payload)
    response = response.json()
    return response

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

def get_cheapest_route(place1, place2):
    search_data = get_all_search(place1, place2)
    price = search_data["routes"][0]["indicativePrices"][0]['price']
    return price


# # TODO: Rewrite to get_best_destination(place1, place2, place3)
# def get_best_destination():
#     cost_from_place1 = get_cheapest_route('munich', 'rome') + get_cheapest_route('paris', 'rome') + get_cheapest_route('london', 'rome')
#     cost_from_place2 = get_cheapest_route('munich', 'berlin') + get_cheapest_route('paris', 'berlin') + get_cheapest_route('london', 'berlin')
#     cost_from_place3 = get_cheapest_route('munich', 'madrid') + get_cheapest_route('paris', 'madrid') + get_cheapest_route('london', 'madrid')
#     print("Total prices per route: ",cost_from_place1, cost_from_place2, cost_from_place3)
#     print("Cheapest destination is ", 'Madrid', 'which costs ', get_cheapest_route('munich', 'madrid'), get_cheapest_route('paris', 'madrid'), get_cheapest_route('london', 'madrid'), " respectively.")

# get_best_destination()