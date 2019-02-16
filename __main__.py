from flask import Flask, request, jsonify, render_template
import requests
import pprint
import json
import googlemaps
from datetime import datetime
from pyzomato import Pyzomato

#sdk and api key for zomato
p = Pyzomato('e2d11e64cba0ac13166aefdeb59df363')
# google maps sdk and api key for google maps
gmaps = googlemaps.Client(key = "AIzaSyBx9Cwhpeg0Kg3GMlYQLHkiXnvozWfDD1E")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def index1():
    text = request.form['text']
    geocode_result = gmaps.geocode(text)
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]
    restaurants = p.search(lat=latitude, lon=longitude, radius="500")
    return jsonify(restaurants)

@app.route('/averageprice')
def index2():
    restaurants = p.search(q="Boston")
    return restaurants["restaurants"][0]["restaurant"]["average_cost_for_two"]

if __name__ == '__main__':
    app.run()
