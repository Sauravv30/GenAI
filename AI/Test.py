import requests

UPLOAD_URL = "http://localhost:8000/upload"
QUESTION_URL = "http://localhost:8000/ask"
WEB_URL = "http://localhost:8000/url"

response = requests.post(WEB_URL,
                         json={"url": "https://www.simplilearn.com/tutorials/python-tutorial/python-threading"},
                         headers={'accept': 'application/json', "Content-Type": 'application/json'})
print(response.status_code)
print(response.text)
