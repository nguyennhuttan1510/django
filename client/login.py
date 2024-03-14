from getpass import getpass

import requests

endpoint = 'http://127.0.0.1:8000/token/'

# headers = {'Content-Type': 'application/json', 'Authentication': 'Bearer '}

username = input('Enter your username: ')
password = getpass('Enter your password: ')

try:
    username = str(username)
    password = str(password)
except:
    username = None
    password = None
    print('Invalid')

if username and password:
    response = requests.post(endpoint, json={'username': username, 'password': password})
    print(response.json())
