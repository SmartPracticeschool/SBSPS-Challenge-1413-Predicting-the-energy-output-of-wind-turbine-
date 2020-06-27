import json
city_in_country = {}

names = json.load(open("names.json", "r"))
temp = {} # ISO Codes - name

city_names = json.load(open("city.list.min.json", "r", encoding="utf8"))
num = 0
for city in city_names:
        num += 1
        # if num == 1000:
        #     break
        if num % 100 == 0:
            # fle = 
                print(f"Performing {num} out of {len(city_names)}", end = "\r")
        try:
            if names[city['country']] in city_in_country:
                city_in_country[names[city['country']]].append((city['name'], city['id']))
            else :
                city_in_country[names[city['country']]] = [(city['name'], city['id'])]
        except :
            print(f"Error for {city}")

import pickle
f = open('city_in_country.pkl', 'ab')
pickle.dump( city_in_country , f )
f.close()
        