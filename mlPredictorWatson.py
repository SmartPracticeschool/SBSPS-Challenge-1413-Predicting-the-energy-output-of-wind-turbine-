import requests
from mlHelperFuncts import transform, inverse #For normalization
import urllib3, requests, json

#More on Normalization : https://www.analyticsvidhya.com/blog/2020/04/feature-scaling-machine-learning-normalization-standardization/
#Normalization of data is done as ML Models perform better on Normalizaed data
def predictPower(windspeed, winddirection):
    """ 
    Parameters:
        windspeed -> list of windspeeds m/s
        winddirection ->list of wind directions degree
    Return power in KW
    This funtion first normalizes the values of windspeed and winddirections then passes it to APIWrapper and then 
    denormalizes the result back and returns it
    """
    api_input = []
    for i in range(len(windspeed)):
        api_input.append(transform(windspeed[i], winddirection[i]))
    power_scaled_list = predictorAPIWrapper(api_input)
    power_output = []
    for i in range(len(power_scaled_list)):
        power_output.append(inverse(float(power_scaled_list[i][0])))
    return power_output


def predictorAPIWrapper(api_input):
    
    """
    Parameters:
        api_input = list of list of windspeed(normalized) and winddirection(normalized)
        Return a list of normalized power outputs 

    """

    # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation	
    iam_token = ''
    with open('iamtoken.txt', 'r') as f:
        iam_token = f.read()
    ml_instance_id = "aa9af3a6-d746-4bc7-8a1b-baac0e78743d"

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token, 'ML-Instance-ID': ml_instance_id}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["speed ", "direction"], "values": api_input}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v4/deployments/7c9a5fb9-28d2-4796-bf11-ef0a7c7ee2f1/predictions', json=payload_scoring, headers=header)

    power_pred = None
    try:
        power_pred = response_scoring.json()['predictions'][0]['values']
    except :
        raise Exception(f"Error in the IBM AI service RESPONCE ---> : {response_scoring.json()}")

    return power_pred
   