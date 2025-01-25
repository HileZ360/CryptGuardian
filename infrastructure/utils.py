import os
import json
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_json_file(filename: str, default: dict) -> dict:
    if not isinstance(filename, str) or not filename.endswith(".json"):
        logging.error("Invalid filename. Must be a JSON file.")
        return default
    try:
        if not os.path.exists(filename):
            logging.warning(f"File not found: {filename}. Using default data.")
            return default
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise ValueError("JSON data is not a dictionary.")
            return data
    except FileNotFoundError:
        logging.warning(f"File not found: {filename}. Using default data.")
        return default
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON file: {filename}. Using default data.")
        return default
    except Exception as e:
        logging.error(f"Unexpected error while loading JSON file '{filename}': {str(e)}")
        return default

def save_json_file(filename: str, data: dict):
    if not isinstance(filename, str) or not filename.endswith(".json"):
        logging.error("Invalid filename. Must be a JSON file.")
        return
    if not isinstance(data, dict):
        logging.error("Invalid data. Must be a dictionary.")
        return
    try:
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            logging.info(f"Data successfully saved to {filename}.")
    except Exception as e:
        logging.error(f"Unexpected error while saving JSON file '{filename}': {str(e)}")

def validate_date(date_string: str) -> bool:
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date_string))
