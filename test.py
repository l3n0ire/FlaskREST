import requests

BASE="http://127.0.0.1:5000/"
response = requests.put(BASE+"api/users",{"name":"colin","gender":"female","age":10})
response = requests.get(BASE+"api/users/colin")
delResponse = requests.delete(BASE+"api/users/colin")
print(response.json())
print(delResponse)
