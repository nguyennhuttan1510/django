import requests

endpoint = 'http://127.0.0.1:8000/account/password_change/'
# endpoint_get = 'http://127.0.0.1:8000/users/'

# get_response = requests.get(endpoint_get)
post_response = requests.post(endpoint, json={"old_password": "o0i9u8y7",
                                              "new_password1": "o0i9u8y7t6",
                                              "new_password2": "o0i9u8y7t6"})

# print(get_response.json())
print(post_response.status_code)
