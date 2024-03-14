import requests

endpoint = 'http://127.0.0.1:8000/rooms/'

try:
    access_token = input('Enter your access token: ')

    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {access_token}'}

    response = requests.get(endpoint, headers=headers)

    print(response)
    print(response.json())
except:
    print('Invalid for get room')
