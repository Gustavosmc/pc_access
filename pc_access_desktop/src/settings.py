import json
from collections import OrderedDict
from src.basedir import PATH_FILES_DATA


def search_setting(setting_searched, settings_file="settings"):
    try:
        with open(PATH_FILES_DATA + '{}.json'.format(settings_file), encoding="utf-8") as json_file:
            json_data = json.load(json_file, object_pairs_hook=OrderedDict)
            return json_data[setting_searched]
    except Exception as ex:
        print(str(ex))
        return None


def update_setting(setting, setting_data, settings_file="settings"):
    with open(PATH_FILES_DATA + '{}.json'.format(settings_file), 'r+', encoding="utf-8") as file:
        text = json.load(file)
        text[setting] = setting_data
        file.seek(0)
        json.dump(text, file, indent=2)
        file.truncate()
