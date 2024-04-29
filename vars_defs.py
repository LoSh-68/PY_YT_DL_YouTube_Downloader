import json
import os
from colorama import Back, Fore, Style

APPNAME = "PY_YT_DL"
DOWNLOAD_FOLDER = "PY_YT_DL_DOWNLOADS"
SETTINGS_FILE = "settings.json"

ASCII_ART = (
    r"""
/$$$$$$$  /$$     /$$ /$$     /$$ /$$$$$$$$     /$$$$$$$  /$$      
| $$__  $$|  $$   /$$/|  $$   /$$/|__  $$__/    | $$__  $$| $$      
| $$  \ $$ \  $$ /$$/  \  $$ /$$/    | $$       | $$  \ $$| $$      
| $$$$$$$/  \  $$$$/    \  $$$$/     | $$       | $$  | $$| $$      
| $$____/    \  $$/      \  $$/      | $$       | $$  | $$| $$      
| $$          | $$        | $$       | $$       | $$  | $$| $$      
| $$          | $$        | $$       | $$       | $$$$$$$/| $$$$$$$$
|__/          |__//$$$$$$ |__/       |__//$$$$$$|_______/ |________/
                 |______/               |______/ 
    """
)

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
    return json_data


def welcome_messsage():
    print(Fore.BLUE + Back.BLACK + ASCII_ART)
    print(Fore.BLUE + Back.BLACK + f"Welcome to {APPNAME}\n"
                                   f"this is the console here you see whats going on.\n")
    print(Fore.BLUE + Back.BLACK + "you will need the console to use the OAUTH feature\n"
                                   f"Only with OAUTH you are able to download AGE RESTRICTED content\n"
                                   f"Simply set it to true in the settings (restart the app) and follow the instruction when downloading AGE RESTRICTED content.\n"
                                   f"Made by LoSh / https://github.com/LoSh-68/PY_YT_DL_YouTube_Downloader\n")
    print(Fore.BLACK + Back.LIGHTGREEN_EX + "Green = Good")
    print(Fore.BLACK + Back.LIGHTRED_EX + "Red = Error")
    print(Fore.BLACK + Back.LIGHTBLUE_EX + "Blue = Info")
    print(Style.RESET_ALL)



def clear_console():
    if os.name == 'nt':
        os.system('cls')
        welcome_messsage()
    else:
        os.system('clear')
        welcome_messsage()
