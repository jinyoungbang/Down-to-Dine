from flask import Flask, request, jsonify, render_template
import requests
import pprint
import json
import googlemaps
from datetime import datetime
from pyzomato import Pyzomato

p = Pyzomato('e2d11e64cba0ac13166aefdeb59df363')
gmaps = googlemaps.Client(key = "AIzaSyBx9Cwhpeg0Kg3GMlYQLHkiXnvozWfDD1E")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text


@app.route('/location')
def index1():
    restaurants = p.search(lat="42.350301", lon="-71.102678", radius="500")
    return jsonify(restaurants)

@app.route('/averageprice')
def index2():
    restaurants = p.search(q="Boston")
    return restaurants["restaurants"][0]["restaurant"]["average_cost_for_two"]

@app.route('/googletesting')
def index3():
    geocode_result = gmaps.geocode('Boston')

    return jsonify(geocode_result)

@app.route('/googletesting1')
def index4():
    geocode_result = gmaps.geocode('Boston')
    latitude = geocode_result[0]["geometry"]["location"]["lat"]
    longitude = geocode_result[0]["geometry"]["location"]["lng"]
    print(latitude)
    print(longitude)
    return jsonify(geocode_result[0]["geometry"]["location"])

if __name__ == '__main__':
    app.run()
