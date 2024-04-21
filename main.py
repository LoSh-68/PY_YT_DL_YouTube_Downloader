from class_PY_YT_DL import PY_YT_DL
import os
import json
from vars_defs import SETTINGS_FILE, JSON_DATA
import pywinstyles

if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(JSON_DATA, file, indent=4)


if __name__ == "__main__":
    PY_YT_DL = PY_YT_DL()
    pywinstyles.apply_style(PY_YT_DL, style="acrylic")
    PY_YT_DL.mainloop()
