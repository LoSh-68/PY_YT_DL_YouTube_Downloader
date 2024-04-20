from class_PY_YT_DL import PY_YT_DL
import os
import json
from variables import SETTINGS_FILE, JSON_DATA

if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(JSON_DATA, file, indent=4)

if __name__ == "__main__":
    PY_YT_DL = PY_YT_DL()
    PY_YT_DL.mainloop()
