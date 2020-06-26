import requests
from mlPredictorWatson import predictPower 
# NUM_PREDICTIONS = 10
def getPredictions(city):
    weather_api = "54e3f61b512d6ae30ebd81acd43d155c"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api}"

    print(url)
    resp = requests.post(url).json()
    
    predictions = []
    wind_speed = []
    wind_directions = []
    initial_time = None
    for entry in resp['list'] :
        # cur = {
        #     'date' : entry['dt_txt'],
        #     'wind_speed' : entry['wind']['speed'],
        #     'wind_direction' : entry['wind']['deg'],
        #     'power' : predictPower(float(entry['wind']['speed']), float(entry['wind']['deg']))
        # }
        if initial_time == None:
            initial_time =  entry['dt_txt']
        wind_speed.append(float(entry['wind']['speed']))
        wind_directions.append(float(entry['wind']['deg']))
    # print(wind_directions)
    # print(wind_speed)
    predictions = predictPower(wind_speed, wind_directions)
        
    return (predictions, initial_time)


# print(getPredictions(""))