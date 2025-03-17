import requests
port = 8000


#test1
endpoint =f"http://127.0.0.1:{port}/api/test?kaka=gros"
respons = requests.get(endpoint)

print(respons.json())
print(respons.status_code)