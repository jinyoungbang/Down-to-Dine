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
    return render_template('index.html')

@app.route('/begin', methods=['GET', 'POST'])
def testing():
    return render_template('begin.html')

@app.route('/location', methods=['POST'])
def index1():
    user_location = request.form['text']
    restaurants = p.search(q=user_location)
    return jsonify(restaurants)

@app.route('/averageprice')
def index2():
    restaurants = p.search(q="Boston")
    return restaurants["restaurants"][0]["restaurant"]["average_cost_for_two"]

@app.route('/test')
def index3():
    restaurants = p.search(lat="42.350301", lon="-71.102678", radius="500")
    return jsonify(restaurants)

if __name__ == '__main__':
    app.run()
