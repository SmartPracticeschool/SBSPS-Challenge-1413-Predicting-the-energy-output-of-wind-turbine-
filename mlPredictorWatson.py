import requests
from mlHelperFuncts import transform, inverse

import urllib3, requests, json


def predictPower(windspeed, winddirection):
    [windspeed_scaled, winddirection_scaled] = transform(windspeed, winddirection)
    power_scaled = predictorAPIWrapper(windspeed_scaled, winddirection_scaled)
    return inverse(power_scaled)


def predictorAPIWrapper(windspeed_scaled, winddirection_scaled):
    

    # NOTE: generate iam_token and retrieve ml_instance_id based on provided documentation	
    iam_token = "eyJraWQiOiIyMDIwMDUyNTE4MzAiLCJhbGciOiJSUzI1NiJ9.eyJpYW1faWQiOiJpYW0tU2VydmljZUlkLTVkMGViNTM1LWY3MzgtNDQwYi04ODA4LTlmNzMzZWMxZGJjNCIsImlkIjoiaWFtLVNlcnZpY2VJZC01ZDBlYjUzNS1mNzM4LTQ0MGItODgwOC05ZjczM2VjMWRiYzQiLCJyZWFsbWlkIjoiaWFtIiwiaWRlbnRpZmllciI6IlNlcnZpY2VJZC01ZDBlYjUzNS1mNzM4LTQ0MGItODgwOC05ZjczM2VjMWRiYzQiLCJuYW1lIjoid2RwLXdyaXRlciIsInN1YiI6IlNlcnZpY2VJZC01ZDBlYjUzNS1mNzM4LTQ0MGItODgwOC05ZjczM2VjMWRiYzQiLCJzdWJfdHlwZSI6IlNlcnZpY2VJZCIsImFjY291bnQiOnsidmFsaWQiOnRydWUsImJzcyI6IjQ3NmFhMGQ2NDc4NjQ1NDU5ODA0NTI1ZmJjY2YwNmQ0In0sImlhdCI6MTU5MjgyMjU5OSwiZXhwIjoxNTkyODI2MTk5LCJpc3MiOiJodHRwczovL2lhbS5ibHVlbWl4Lm5ldC9pZGVudGl0eSIsImdyYW50X3R5cGUiOiJ1cm46aWJtOnBhcmFtczpvYXV0aDpncmFudC10eXBlOmFwaWtleSIsInNjb3BlIjoiaWJtIG9wZW5pZCIsImNsaWVudF9pZCI6ImJ4IiwiYWNyIjoxLCJhbXIiOlsicHdkIl19.i363oCmOXtITs6o2GJfb3HGnDvvYlwwodCH41BR6rm-arBhu4V1xwclg_bHBToPHT0dVkmYaialwPoas6xr0TqzDBCejUVXI_H1vKmuSd8iLoM8wW-aOC_QF-txoTxjHZ5bw4nEyqfvczq45Udv7eb3yReUxMhFpMY4NpcH0c7rgnSVjCrxagYuuj_78w9PeEqFkjFFFz4wFAT38GfmxfDhUgDz6Ag0hIm5QOfwBHIjyCaaztTjJ_WXTzKpk50wzxjZ-mnxO2ZbOJ-gFKJcheJ-UM1IDYkS4jS27wU79gHyw_oVDeofKRwZV3WrzBs9BchA_3dZPO2QHuXimUUyCsw"
    ml_instance_id = "6e725e72-d102-42dd-8647-3357992c6fda"

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token, 'ML-Instance-ID': ml_instance_id}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["speed ", "direction"], "values": [[ windspeed_scaled, winddirection_scaled  ]]}]}
    # try:
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/v4/deployments/44802140-211f-4386-9207-799f5ceddc7c/predictions', json=payload_scoring, headers=header)
    # return (response_scoring.text)
    power_pred = response_scoring.json()['predictions'][0]['values'][0][0]
    # print(power_pred)
    return (power_pred)
    # except :
    #     raise Exception("Can not access ML Service")

    
    # print("Scoring response")
    # print(json.loads(response_scoring.text))