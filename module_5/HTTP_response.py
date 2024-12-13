# Напишите сырой HTTP запрос к гуглу
import requests

# сырой запрос
# GET / HTTP/1.1
# Host: www.google.com

# через requests
response = requests.get("www.google.com")

# через curl
# curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://www.google.com