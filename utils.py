import json
import re

def load_json_file(filename: str, default: dict) -> dict:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filename}. Using default data.")
        return default
    except json.JSONDecodeError:
        print(f"Error decoding JSON file: {filename}. Using default data.")
        return default
    except Exception as e:
        print(f"Error loading JSON file: {str(e)}")
        return default

def save_json_file(filename: str, data: dict):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")

def validate_date(date_string: str) -> bool:
    return re.match(r"^\d{4}-\d{2}-\d{2}$", date_string) is not None
