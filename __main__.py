from flask import Flask, request, jsonify, render_template
import requests
import pprint
import json
import googlemaps
from datetime import datetime
from pyzomato import Pyzomato
import random

# sdk and api key for zomato
p = Pyzomato('e2d11e64cba0ac13166aefdeb59df363')
# google maps sdk and api key for google maps
gmaps = googlemaps.Client(key = "AIzaSyBx9Cwhpeg0Kg3GMlYQLHkiXnvozWfDD1E")

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
    user_text = request.form['location']
    user_price = request.form['price']

    geocode_result = gmaps.geocode(user_text)
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]
    restaurants_dict = p.search(lat=latitude, lon=longitude, radius="500")
    average_cost = (restaurants["restaurants"][0]["restaurant"]["average_cost_for_two"])/2
    return jsonify(restaurants_dict)


if __name__ == '__main__':
    app.run(debug = True)


##############################################################################
restaurants_dict = p.search(lat=latitude, lon=longitude, radius="500")

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

    return three_sets

def restaurantsForDay(three_sets):

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
    return dictionary
