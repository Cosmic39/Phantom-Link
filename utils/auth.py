import json

with open("config/secrets.json") as f:
    data = json.load(f)

AUTHORIZED_USER_ID = data["authorized_user_id"]
SECRET_CODE = data["secret_code"]

def is_authorized(user_id):
    return user_id == AUTHORIZED_USER_ID