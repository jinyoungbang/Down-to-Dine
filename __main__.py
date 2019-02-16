from flask import Flask, request, jsonify
import requests
import pprint
import json
import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBx9Cwhpeg0Kg3GMlYQLHkiXnvozWfDD1E')

app = Flask(__name__)

@app.route('/')
def index():
    return "testing"

if __name__ == '__main__':
    app.run()
