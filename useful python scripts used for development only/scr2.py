import json
import pickle
countries = []
names = json.load(open("names.json", "r"))
for f in names.values():
    countries.append(f)

f = open('countries.pkl', 'ab')
pickle.dump( countries , f )
f.close()
