from flask import Flask, request, jsonify, render_template, url_for, redirect
import requests
import pprint
import json
import os
import googlemaps
from datetime import datetime
from pyzomato import Pyzomato
import random

# sdk and api key for zomato
p = Pyzomato('e2d11e64cba0ac13166aefdeb59df363')
# google maps sdk and api key for google maps
gmaps = googlemaps.Client(key = "AIzaSyBx9Cwhpeg0Kg3GMlYQLHkiXnvozWfDD1E")


def getAllPrices(restaurants_dict):
    array = []
    for i in range(len(restaurants_dict["restaurants"])-1):
        array += [restaurants_dict["restaurants"][i]["restaurant"]["average_cost_for_two"]]

    return array

def find3Numbers(A, arr_size, sum):
    three_sets = []
    # Fix the first element as A[i]
    for i in range( 0, arr_size-2):

        # Fix the second element as A[j]
        for j in range(i + 1, arr_size-1):

            # Now look for the third number
            for k in range(j + 1, arr_size):
                if A[i] + A[j] + A[k] < sum:
                    three_sets +=  [[i, j, k]]



app = Flask(__name__)

# main homepage connected to index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST', 'GET'])
def begin():
    return render_template('begin.html')




@app.route('/begin', methods=['POST', 'GET'])
def index1():
    # gets user-inputted value of location
    user_text = request.form['location']
    user_price = request.form['price']

    geocode_result = gmaps.geocode(user_text)
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]
    restaurants = p.search(lat=latitude, lon=longitude, radius="500")
    average_cost = (restaurants["restaurants"][0]["restaurant"]["average_cost_for_two"])/2

    return render_template('begin.html')


@app.route('/results', methods=['POST','GET'])
def results():

    #print(request.form)
    user_text = request.form['location']
    user_price = request.form['price']

    geocode_result = gmaps.geocode(user_text)
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]
    restaurants_dict = p.search(lat=latitude, lon=longitude, radius="1000")
    average_cost = (restaurants_dict["restaurants"][0]["restaurant"]["average_cost_for_two"])/2

    array = []
    for i in range(len(restaurants_dict["restaurants"])-1):
        array += [restaurants_dict["restaurants"][i]["restaurant"]["average_cost_for_two"]]

    #print(array)

    three_sets = []

    arr_size = len(array)

    # Fix the first element as A[i]
    for i in range(0, arr_size-2):
        # Fix the second element as A[j]
        for j in range(i + 1, arr_size-1):
            # Now look for the third number
            for k in range(j + 1, arr_size):
                if array[i] + array[j] + array[k] <= int(user_price) * 2:
                    three_sets +=  [[i, j, k]]

    #print(three_sets)
    #print(array)
    #print(arr_size)

    dictionary = {}
    count = 0

    for i in range(len(three_sets)):
        dictionary[i] = {}
        for j in [[0, 'morning'],[1, 'lunch'], [2, 'dinner']]:
            name = restaurants_dict["restaurants"][three_sets[i][j[0]]]["restaurant"]["name"]
            cost = restaurants_dict["restaurants"][three_sets[i][j[0]]]["restaurant"]["average_cost_for_two"] / 2
            location = restaurants_dict["restaurants"][three_sets[i][j[0]]]["restaurant"]["location"]["address"]
            dictionary[i][j[1]] = {}
            dictionary[i][j[1]]["name"] = name
            dictionary[i][j[1]]["location"] = location
            dictionary[i][j[1]]["cost"] = cost

    random_num = random.randrange(0, len(three_sets)-1)
    name1 = dictionary[random_num]["morning"]["name"]
    name2 = dictionary[random_num]["lunch"]["name"]
    name3 = dictionary[random_num]["dinner"]["name"]
    cost1 = dictionary[random_num]["morning"]["cost"]
    cost2 = dictionary[random_num]["lunch"]["cost"]
    cost3 = dictionary[random_num]["dinner"]["cost"]
    location1 = dictionary[random_num]["morning"]["location"]
    location2 = dictionary[random_num]["lunch"]["location"]
    location3 = dictionary[random_num]["dinner"]["location"]

    geocode_loc1 = gmaps.geocode(location1)
    place_id_1 = geocode_loc1[0].get("place_id")
    geocode_loc2 = gmaps.geocode(location2)
    place_id_2 = geocode_loc2[0].get("place_id")
    geocode_loc3 = gmaps.geocode(location3)
    place_id_3 = geocode_loc3[0].get("place_id")

    return render_template('result.html', name1 = name1, name2 = name2, name3 = name3, cost1=cost1, cost2=cost2, cost3=cost3, location1=location1, location2=location2, location3=location3, place_id_1=place_id_1, place_id_2=place_id_2, place_id_3=place_id_3)

@app.errorhandler(400)
def page_not_found(error):
    return render_template('error.html'), 400

if __name__ == '__main__':
    app.run(debug=True)


##############################################################################
