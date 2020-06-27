import os
import json
import shutil 
def update():
    if os.path.exists("./country_data"):
        shutil.rmtree("./country_data")
        print("Removed data!")

    
    # try:
    os.mkdir("country_data")
    names = json.load(open("names.json", "r"))
    en2word = {}
    for country_name in names.values():
        os.mkdir(f"./country_data/{country_name}")
    print("Created directories")
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
            out_file = open(f"./country_data/{names[city['country']]}/{city['name']}", 'w')
            json.dump(city, out_file)
        except :
            print(f"Error for {city}")
        out_file.close()


if __name__ == '__main__':
    update()

