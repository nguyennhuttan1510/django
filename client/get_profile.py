import requests

endpoint = 'http://127.0.0.1:8000/accounts/'


try:
    access_token = input('Enter your access token: ')

    user_id = input("Enter user_id:\n")

    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    if user_id:
        endpoint = f'http://127.0.0.1:8000/accounts/{user_id}'

    response = requests.get(endpoint, headers=headers)
    print(response)
    print(response.json())
except:
    print('Invalid for get users')
