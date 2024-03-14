import requests

endpoint_update = 'http://127.0.0.1:8000/users/1/update/'

update_response = requests.put(endpoint_update,
                               data={'name': 'nguyen nhut tan', 'email': 'nguyentan@gmail.com', 'age': 15})

print(update_response.json())
