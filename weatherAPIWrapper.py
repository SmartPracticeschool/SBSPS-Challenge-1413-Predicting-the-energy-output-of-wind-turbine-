import requests
from mlPredictorWatson import predictPower 
def getPredictions(city):
    weather_api = "54e3f61b512d6ae30ebd81acd43d155c"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={weather_api}"
    print(f'[DEBUG] Gone for {url}')
    
    resp = requests.post(url).json()
    if 'list' not in resp:
        raise Exception(f'Weather API Error for {url} responce got => {resp} ')
    predictions = []
    wind_speed = []
    wind_directions = []
    initial_time = None
    for entry in resp['list'] :
        
        if initial_time == None:
            initial_time =  entry['dt_txt']
        wind_speed.append(float(entry['wind']['speed']))
        wind_directions.append(float(entry['wind']['deg']))
    predictions = predictPower(wind_speed, wind_directions)
        
    return (predictions, initial_time)


