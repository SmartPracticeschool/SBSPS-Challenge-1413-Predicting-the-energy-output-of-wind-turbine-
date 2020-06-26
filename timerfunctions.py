import requests

def update_iamkey():

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic Yng6Yng=',
    }

    data = {
    'apikey': 'dwbBWzM45uTSa9IyuVnsF0ppPL2Lunwc5qODOhfc_K-h',
    'grant_type': 'urn:ibm:params:oauth:grant-type:apikey'
    }

    response = requests.post('https://iam.bluemix.net/identity/token', headers=headers, data=data).json()
    f = open('iamtoken.txt', 'w')
    f.write(response['access_token'])
    print("Updated the token")
    f.close()