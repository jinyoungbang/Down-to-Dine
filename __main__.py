from flask import Flask, request, jsonify, render_template
import requests
import pprint
import json
import googlemaps
from datetime import datetime
from pyzomato import Pyzomato

p = Pyzomato('e2d11e64cba0ac13166aefdeb59df363')

app = Flask(__name__)

@app.route('/')
def index():
    return "testing"

@app.route('/location')
def index1():
    restaurants = p.search(lat="42.350301", lon="-71.102678", radius="", sort=)
    return jsonify(restaurants)

@app.route('/averageprice')
def index2():
    restaurants = p.search(q="Boston")
    return restaurants["restaurants"][0]["restaurant"]["average_cost_for_two"]

if __name__ == '__main__':
    app.run()
