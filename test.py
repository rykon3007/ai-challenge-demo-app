
import requests
r = requests.get("https://umayadia-apisample.azurewebsites.net/api/persons/Shakespeare")
print(r.text)
