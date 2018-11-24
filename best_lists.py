# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 00:02:35 2018

@author: albil
"""

import numpy as np
import pandas as pd

#def get_places(pnt):
#    lat_lng_str = str(pnt['lat']) + ',' + str(pnt["lng"])
#    payload = {"location": lat_lng_str,"radius":500,"type":"airports","key": "AIzaSyCNa0G19BABRTzrn2AyO6VyClwhM3iilOw"}
#    response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=payload)
#    data=response.json()
#    #print data
#    length=len(data['results'])
#    for i in range(length):
#        my_dict={'lat': data["results"][i]["geometry"]["location"]["lat"], 'lng':data["results"][i]["geometry"]["location"]["lng"], 
#                 'name':data["results"][i]["name"].encode('utf-8')}
#        print my_dict

city_list_df = pd.read_csv('biggest_cities.csv', sep =";")

lat_0 = 46.519654
lng_0 = 6.632273400000031

def close_main_cities(lat_0, lng_0, city_list_df):
    point = {'lat': lat_0, 'long':lng_0, 'name':'lausanne'}
    range = 5

    test_df = city_list_df
    test_df = test_df[(test_df.lat >lat_0 - range) & (test_df.lat <lat_0 + range)]
    test_df = test_df[(test_df.lng >lng_0 - range) & (test_df.lng <lng_0 + range)]
    possible_pts = test_df.reset_index()
    l=[]
    for index,row in possible_pts.iterrows():
        l += [{'lat': row['lat'], 'lng': row['lng'], 'name': row['name']}]
    return l
    
close_cities = close_main_cities(lat_0, lng_0, city_list_df)


#    l+=line
#    in

#possible_pts_dict = possible_pts.to_dict('index')
#possible_pts_list = np.array(possible_pts_dict.items())
#vals = np.fromiter(possible_pts_dict.values(), dtype=float)
