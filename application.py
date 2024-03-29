from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, abort
import atexit
import os
import json
from mlHelperFuncts import transform, inverse
from mlPredictorWatson import predictPower as power_pred
import json
from weatherAPIWrapper import getPredictions
import requests
from timerfunctions import update_iamkey 
import threading
import pickle
import random
app = Flask(__name__, static_url_path='')




# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))



@app.route('/')
def root():
    #Home Page showing all options for the user
    return render_template('index.html')


@app.route('/predict')
def predict():
    #Returns the page for prediction as per city
    return render_template('predict.html')
    
@app.route('/predict/all_countries')
def all_countries():
    #API --> outputs all counties in a json format
    countries = []
    #countries.pkl is pickled version of a list of all countries
    f = open('countries.pkl', 'rb')
    countries = pickle.load(f)

    d = {"countries" : countries}

    return jsonify(d)

@app.route('/predict/cities/<country>')
def cities(country):
    
    #API for delivering a list of all cities in a country using GET
    all_cities = []
    #data is a pickled version of a dict of country name TO list of city names
    f = open('data', 'rb')
    city_in_country = pickle.load(f)
    for entry in city_in_country[country]:
        all_cities.append(entry[0]) 

    cur = {"cities" : all_cities}
    f.close()
    return jsonify(cur)

@app.route('/predict/submit', methods = ['POST'])
def submit():
    #API to return a predictions of expected powers 
    try:
        update_iamkey()
        city = request.form['city'] 
        #We need to replace UNICODE characters with their ASCII equivalents as UNICODEare not accepted by weather API
        forbidden = ['ā', 'ē', 'ī', "ō", 'ū', 'ȳ', 'á', 'é', 'í' , 'ó', 'ú', 'ý', 'ï']
        allowed = ['a', 'e', 'i', 'o', 'u','y', 'a', 'e', 'i', 'o', 'u','y' , 'i' ]
        for i in range(len(forbidden)):
            city = city.replace(forbidden[i], allowed[i])
        
            resp, initial_time = getPredictions(city)
            return jsonify({
                'powers' : resp,
                'time' : initial_time
            })
    except Exception as e:
        return str("[ERROR] " + e.message) 

        


@app.route('/get_windspeeds', methods = ['POST'])
def get_windspeeds():
    #API to return a json of expected windspeeds

    city = request.form['city']
    #We need to replace UNICODE characters with their ASCII equivalents as UNICODEare not accepted by weather API
    forbidden = ['ā', 'ē', 'ī', "ō", 'ū', 'ȳ', 'á', 'é', 'í' , 'ó', 'ú', 'ý', 'ï']
    allowed = ['a', 'e', 'i', 'o', 'u','y', 'a', 'e', 'i', 'o', 'u','y' , 'i' ]
    for i in range(len(forbidden)):
        city = city.replace(forbidden[i], allowed[i])
    weather_api = "54e3f61b512d6ae30ebd81acd43d155c"
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api}"
        resp = requests.post(url).json()
        
        windspeeds  = []
        for entry in resp['list'] :
            windspeeds.append(float(entry['wind']['speed']))
        return jsonify({
            'windspeeds' : windspeeds
        })
    except :
        return jsonify({
            'error' : 'Çan not access the openweather maps'
        })

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/windy_cities')
def windy_cities():
    cities = ['Wellington', 'Barrow Island', 'Cape Blanco', 'Rio Gallegos', 'Bridge Creek', 'Dodge City', 'Gruissan', 
                'Patagonia', 'Oklahoma', 'Punta Arenas', 'Baku', 'Punta Arenas']
    city = random.choice(cities)
    weather_api = "54e3f61b512d6ae30ebd81acd43d155c"
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}'
    
    resp = requests.get(url).json()
    try:
        lat = resp["coord"]["lat"]
    except:
        print(city)
        
        abort(404)
    lon = resp["coord"]["lon"]
    temp = resp["main"]["temp"]
    press = resp["main"]["pressure"]
    windspeed = resp["wind"]["speed"]
    winddir = resp["wind"]["deg"]

    return jsonify({
        'city' : city,
        'lat' : lat,
        'lon' : lon,
        'temp' : temp,
        'pressure' : press,
        'windspeed' : windspeed,
        'winddir' : winddir
    })



@app.route('/compare')
def compare():
    #Returns a webpage for compare route
    return render_template('compare.html')

##########DEBUG PURPOSES ONLY ###########
# @app.route('/test/<ws>/<wd>')
# def test(ws, wd):
#     return str(power_pred(int(ws), int(wd)))
#########################################
@app.route('/down')
def down():
    #this funtion will download pickled data requred by the web app from Google Drive 
    from google_drive_downloader import GoogleDriveDownloader as gdd
    gdd.download_file_from_google_drive(file_id='1K2obxXAwzg63KlRAlBkuIxB79YCYq9lP',dest_path='./data')
    f = open('data', 'rb')
    city_in_country = pickle.load(f)
    f.close()
    return jsonify({"Success":10, "vsl" : city_in_country})
    



if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=port, debug=True)
    
