import requests

try:
    room_id = input('Enter service id: ')

    access_token = input('Enter your access token: ')

    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {access_token}'}

    endpoint = f'http://127.0.0.1:8000/rooms/{room_id}'
    response = requests.delete(endpoint, headers=headers)
    print(response.status_code)
except:
    print('Invalid')
