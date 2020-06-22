import os
import json
import shutil 

if os.path.exists("./country_data"):
    shutil.rmtree("./country_data")


try:
    os.mkdir("country_data")
    names = json.load(open("names.json", "r"))
    for country_name in names.keys():
        os.mkdir(f"./country_data/{country_name}")

except:
    print("Error!")

