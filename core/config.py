import os
import json

# Config File
CONFIG_JSON = "config.json"

def create_config_json():
    
    if not os.path.exists(CONFIG_JSON):
        try:
            with open(CONFIG_JSON, "w", encoding="utf-8") as file:
                dict_config = {
                    "Security": [],
                    "Allowed Types": []
                }
                json.dump(dict_config, file, indent=4)
                print(f"[ FILE CONFIG CREATE ] : {file.name}")

                return True
            
        except json.JSONEncoder as error:
            print(error)
            return False
    else:
        print(f"[ FILE CONFIG EXISTS ] : {CONFIG_JSON}")
        return True

def read_config_json():
    try:
        def read_file():
            with open(CONFIG_JSON, "r", encoding="utf-8") as file:
                dict_config_json = json.load(file)
                return dict_config_json

        return read_file()
    except FileNotFoundError:
        create_config_json()
    finally:
        dict_config_json = read_file()
    return dict_config_json
        

def write_data_to_config_json(dict_config):
    with open(CONFIG_JSON, "w", encoding="utf-8") as file:
        json.dump(dict_config, file, indent=4)
        return True