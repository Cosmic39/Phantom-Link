import os
import sys
import json


# ---------------- 📁 PATH HANDLING ---------------- #

def get_base_path():
    # Running as EXE
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)

    # Running as script
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = get_base_path()
SECRETS_PATH = os.path.join(BASE_DIR, "config", "secrets.json")


# ---------------- 🔐 LOAD CONFIG ---------------- #

if not os.path.exists(SECRETS_PATH):
    raise FileNotFoundError(
        "❌ secrets.json not found!\n"
        "👉 Create: config/secrets.json in the same folder as the EXE"
    )

try:
    with open(SECRETS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError:
    raise ValueError("❌ secrets.json is not a valid JSON file")


# ---------------- 🔑 VALIDATION ---------------- #

required_keys = ["authorized_user_id", "secret_code", "bot_token"]

for key in required_keys:
    if key not in data:
        raise KeyError(f"❌ Missing '{key}' in secrets.json")


# ---------------- 🔑 VARIABLES ---------------- #

AUTHORIZED_USER_ID = int(data["authorized_user_id"])
SECRET_CODE = str(data["secret_code"])  # force string safety
BOT_TOKEN = data["bot_token"]


# ---------------- 🧠 AUTH CHECK ---------------- #

def is_authorized(user_id):
    return user_id == AUTHORIZED_USER_ID