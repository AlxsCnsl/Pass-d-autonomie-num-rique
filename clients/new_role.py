import requests

port = 8000
endpoint =f"http://127.0.0.1:{port}/api/test"


data = {
  'name' : 'user'
}

response = requests.post(endpoint, json=data)
print(response.json())
print(response.status_code)