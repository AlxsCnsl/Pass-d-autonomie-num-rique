import requests

port = 8000
endpoint = 'roles/'
url =f"http://127.0.0.1:{port}/api/{endpoint}"


data = {
  'name' : ''
}

response = requests.post(url, data=data)