import json
import os

APPNAME = "PY_YT_DL"

SETTINGS_FILE = "settings.json"

JSON_DATA = [
    {"id": 1, "name": "video_resolution", "content": ""},
    {"id": 2, "name": "video_filetype", "content": ""},
    {"id": 3, "name": "video_fps", "content": ""},
    {"id": 4, "name": "video_codec", "content": ""},
    {"id": 5, "name": "video_bitrate", "content": ""},
    {"id": 6, "name": "audio_filetype", "content": ""},
    {"id": 7, "name": "audio_codec", "content": ""},
    {"id": 8, "name": "audio_bitrate", "content": ""},
    {"id": 9, "name": "_use_oauth", "content": ""},
    {"id": 10, "name": "allow_oauth_cache", "content": ""},
    {"id": 11, "name": "win_sound", "content": ""},
    {"id": 12, "name": "theme", "content": ""}
]


def get_json_data():
    if not os.path.exists(SETTINGS_FILE):
        return None  # Return None or raise an exception if the file doesn't exist
    else:
        with open(SETTINGS_FILE, "r") as file:
            json_data = json.load(file)  # Load JSON data from the file
            return json_data
