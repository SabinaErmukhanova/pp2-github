import json  # used to read and write JSON files
import os    # used to check if file exists


SETTINGS_FILE = "settings.json"  # name of settings file


#  LOAD SETTINGS
def load_settings():

    # default settings if file doesn't exist or is broken
    default_settings = {
        "sound": True,                 # sound on/off
        "grid": False,                # grid display on/off
        "snake_color": [170, 200, 50]  # default snake color (RGB)
    }

    # if settings file does not exist
    if not os.path.exists(SETTINGS_FILE):
        save_settings(default_settings)  # create file with defaults
        return default_settings

    try:
        # try to open and read JSON file
        with open(SETTINGS_FILE, "r") as file:
            data = json.load(file)

        # make sure all keys exist (important for safety)
        for key in default_settings:
            if key not in data:
                data[key] = default_settings[key]

        return data

    except:
        # if file is corrupted → return default
        return default_settings


#  SAVE SETTINGS 
def save_settings(settings):

    # save dictionary to JSON file
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)