import requests

user_id = input("Enter user_id:\n")
access_token = input('Enter your access token: ')
try:
    user_id = int(user_id)
except:
    user_id = None
    print("Please enter user_id")

if user_id:
    headers = {'content-type': 'application/json', 'Authorization': f'Bearer {access_token}'}
    url = f"http://127.0.0.1:8000/accounts/{user_id}"
    update_response = requests.delete(url, headers=headers)
    print(update_response.status_code)
