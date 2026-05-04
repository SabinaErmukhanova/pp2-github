import json  # used to read and write JSON files (leaderboard and settings)
import os  # used to check if files exist

LEADERBOARD_FILE = "leaderboard.json"  # file where scores are stored
SETTINGS_FILE = "settings.json"  # file where user settings are stored


def load_leaderboard():
    # function to load leaderboard data from file

    if not os.path.exists(LEADERBOARD_FILE):
        # if file does not exist, return empty list (no scores yet)
        return []

    try:
        # try to open and read the file
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)  # convert JSON into Python list
    except:
        # if file is corrupted or cannot be read, return empty list
        return []


def save_score(result):
    # function to save a new score into leaderboard

    data = load_leaderboard()  # load existing scores

    # add new score entry
    data.append({
        "name": result.get("name", "Unknown"),  # player name
        "score": result.get("score", 0),  # score value
        "distance": result.get("distance", 0),  # distance traveled
        "coins": result.get("coins", 0)  # coins collected
    })

    # sort scores from highest to lowest and keep only top 10
    data = sorted(data, key=lambda x: x.get("score", 0), reverse=True)[:10]

    # save updated leaderboard back to file
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(data, file, indent=4)  # indent=4 makes it readable


def load_settings():
    # function to load game settings

    default_settings = {
        "sound": True,  # sound is enabled by default
        "difficulty": "medium",  # default difficulty
        "car_color": "default"  # default car color
    }

    if not os.path.exists(SETTINGS_FILE):
        # if settings file does not exist, create it with default values
        save_settings(default_settings)
        return default_settings

    try:
        # try to read settings from file
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)  # convert JSON to Python dictionary
    except:
        # if file is broken or unreadable, return default settings
        return default_settings


def save_settings(settings):
    # function to save settings to file

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)  # save dictionary as JSON