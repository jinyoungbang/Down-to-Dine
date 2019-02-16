from flask import Flask, request, jsonify, render_template
import requests
import pprint
import json
import googlemaps
from datetime import datetime
from pyzomato import Pyzomato
import itertools

# sdk and api key for zomato
p = Pyzomato('e2d11e64cba0ac13166aefdeb59df363')
# google maps sdk and api key for google maps
gmaps = googlemaps.Client(key = "AIzaSyBx9Cwhpeg0Kg3GMlYQLHkiXnvozWfDD1E")


app = Flask(__name__)

# main homepage connected to index.html
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def index1():
    # gets user-inputted value of location
    user_text = request.form['location']
    user_price = request.form['price']

    # gets geocode results from user-inputted location
    geocode_result = gmaps.geocode(user_text)

    # latitude and longitude of user-inputted location
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]

    # searches restaurants based on lat and lon
    restaurants = p.search(lat=latitude, lon=longitude, radius="500")

    dict = {}

    # returns
    for i in range(len(restaurants["restaurants"])):
        average_cost = (restaurants["restaurants"][i]["restaurant"]["average_cost_for_two"])/2
        if average_cost < int(user_price):
            dict[i] = (restaurants["restaurants"][i]["restaurant"]["average_cost_for_two"])/2

    return jsonify(dict)


if __name__ == '__main__':
    app.run(debug = True)
