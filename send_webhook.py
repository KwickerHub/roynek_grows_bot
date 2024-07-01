import requests
import json

# The URL of the locally running Flask server
url = 'http://localhost:8000/webhook'
# payload = {
#     "update_id":1111111111,"message":{"message_id":2222,"from":{"id":333333333333,"is_bot":false,"first_name":"Username","last_name":"Lastname","username":"username","language_code":"en},"chat":{"id":1111111111,"first_name":"Username","last_name":"Lastname","username":"username","type":"private"},"date":1518592199,"text":"xyz"}
#                                                                 }
#     }}

# Sample payload mimicking the webhook data
# Sample payload mimicking the webhook data

payload = {
    "update_id": 7289772,
    "message": {
        "date": 1441645532,
        "chat": {
            "last_name": "N",
            "id": 1091264015,
            "first_name": "Ken",
            "username": "NKenyor",
            "type": "private"  # Add this field
        },
        "message_id": 334,
        "from": {
            "last_name": "N",
            "id": 1091264015,
            "first_name": "Ken",
            "username": "NKenyor",
            "is_bot": False  # Add this field
        },
        "text": "/referral"
    }
}


# Headers
headers = {
    'Content-Type': 'application/json'
}

# Send the POST request
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print the response
print(response.status_code)
print(response.text)
