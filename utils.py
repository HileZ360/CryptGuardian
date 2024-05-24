import json
import re

def load_json_file(filename, default):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return default

def save_json_file(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def validate_date(date_string):
    return re.match(r"^\d{4}-\d{2}-\d{2}$", date_string) is not None
