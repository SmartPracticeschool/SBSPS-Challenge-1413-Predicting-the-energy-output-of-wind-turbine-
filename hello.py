from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
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
from script import update
import pickle
app = Flask(__name__, static_url_path='')

CITIES_IN_COUNTRY = {}
db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

threading.Timer(60*15, update_iamkey).start()


@app.route('/')
def root():
    return render_template('index.html')

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])


@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)


# @app.route('/get_started')
# def get_started():

@app.route('/predict')
def predict():
    return render_template('predict.html')
    
@app.route('/predict/all_countries')
def all_countries():
    countries = []
    # file = json.load(open('names.json', 'r'))
    # for country_name in file.values():
    #     countries.append(country_name)
    
    f = open('countries.pkl', 'rb')
    countries = pickle.load(f)

    d = {"countries" : countries}

    return jsonify(d)

@app.route('/predict/cities/<country>')
def cities(country):
    all_cities = []
    # for city in os.listdir("./country_data/" + country):
    #     with open("./country_data/" + country + "/" + city) as f:
    #         all_cities.append(json.load(f))
    # cur = {"cities" : all_cities}

    f = open('data', 'rb')
    city_in_country = pickle.load(f)
    # print(city_in_country[country])
    for entry in city_in_country[country]:
        all_cities.append(entry[0]) 

    cur = {"cities" : all_cities}
    return jsonify(cur)

@app.route('/predict/submit', methods = ['POST'])
def submit():
    print(request.form)
    city = request.form['city'] 
    resp, initial_time = getPredictions(city)
    
    return jsonify({
        'powers' : resp,
        'time' : initial_time
    })
    

@app.route('/result/<city>')
def result(city):
    predictions = getPredictions(city)[0]
    return jsonify(predictions)


@app.route('/get_windspeeds', methods = ['POST'])
def get_windspeeds():
    city = request.form['city']
    weather_api = "54e3f61b512d6ae30ebd81acd43d155c"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api}"
    resp = requests.post(url).json()
    
    windspeeds  = []
    for entry in resp['list'] :
        windspeeds.append(float(entry['wind']['speed']))
    return jsonify({
        'windspeeds' : windspeeds
    })


@app.route('/compare')
def compare():
    return render_template('compare.html')

@app.route('/test/<ws>/<wd>')
def test(ws, wd):
    return str(power_pred(int(ws), int(wd)))
@app.route('/down')
def down():
    from google_drive_downloader import GoogleDriveDownloader as gdd
    gdd.download_file_from_google_drive(file_id='1K2obxXAwzg63KlRAlBkuIxB79YCYq9lP',dest_path='./data')
    f = open('data', 'rb')
    city_in_country = pickle.load(f)
    f.close()
    return jsonify({"Success":10, "vsl" : city_in_country})
    

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    update_iamkey()
    
    threading.Timer(1200, update_iamkey).start()
    app.run(host='0.0.0.0', port=port, debug=True)
    
