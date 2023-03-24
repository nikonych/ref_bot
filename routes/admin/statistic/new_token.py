import requests

data = {
    "response_type": "code",
    "client_id": "api_wallet_private",
    "client_software": "api",
    "token": "8287f92e82ba8be26cbc5aab0f4b7ebb",
}

req = requests.post("http://qiwi.com/oauth/authorize", data=data)
print(req.json())
