import json
import os

APPNAME = "PY_YT_DL"
DOWNLOAD_FOLDER = "PY_YT_DL_DOWNLOADS"
SETTINGS_FILE = "settings.json"

JSON_DATA = [
    {"id": 1, "name": "use_oauth", "content": "False"},
    {"id": 2, "name": "allow_oauth_cache", "content": "False"},
    {"id": 3, "name": "win_sound", "content": "True"},
    {"id": 4, "name": "theme", "content": "dark"}
]


def get_json_data():
    if not os.path.exists(SETTINGS_FILE):
        raise FileNotFoundError(f"Settings file '{SETTINGS_FILE}' not found.")
    with open(SETTINGS_FILE, "r") as file:
        json_data = json.load(file)
    return json_data  #


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
