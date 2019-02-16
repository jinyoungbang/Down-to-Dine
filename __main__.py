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

# class Restaurant:
#     def __init__(self, i):
#         self.i = i
#
#     def getName(self):
#         return self.restaurants
#

# sum of three


app = Flask(__name__)

# main homepage connected to index.html
@app.route('/')
def index():
    return render_template('index.html')


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

    # debugging
    # print(user_text)
    # print(user_price)
    # print(average_cost)
    dict = {}

    for i in range(len(restaurants["restaurants"])):
        average_cost = (restaurants["restaurants"][i]["restaurant"]["average_cost_for_two"])/2
        if average_cost < int(user_price):
            dict[i] = (restaurants["restaurants"][i]["restaurant"]["average_cost_for_two"])/2

    list_of_dict = []
    list_of_dict_price = []
    list_of_dict_sorting = []
    counter = 0

    for i in dict:
        list_of_dict += [counter, i, (restaurants["restaurants"][i]["restaurant"]["average_cost_for_two"]/2)]
        list_of_dict_price += [(restaurants["restaurants"][i]["restaurant"]["average_cost_for_two"]/2)]
        list_of_dict_sorting += [[(restaurants["restaurants"][i]["restaurant"]["average_cost_for_two"]/2), i]]
        counter += 1

    print(list_of_dict)
    print()
    print(list_of_dict_price)
    print()
    print(list_of_dict_sorting)
    print()
    print(len(list_of_dict_price))
    print((list_of_dict_sorting)[1][0])
    print(type(list_of_dict_sorting))
    print(type(list_of_dict_price))
    print(type((list_of_dict_sorting)[1][0]))

    numbers = list_of_dict_sorting
    result = [seq for i in range(len(numbers), 0, -1) for seq in itertools.combinations(numbers[0], i) if sum(seq) <= int(user_price)]

    updated_result = []
    for i in range(len(result)):
        if len(result[i]) == 3:
            updated_result += [result[i]]

    print(updated_result)



    return render_template('begin.html')

if __name__ == '__main__':
    app.run()
