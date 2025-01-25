import bcrypt
import re
import logging
from time import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

failed_attempts = {}
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 300

def is_locked(username: str) -> bool:
    if username in failed_attempts:
        attempts, last_failed = failed_attempts[username]
        if attempts >= MAX_ATTEMPTS and time() - last_failed < LOCKOUT_TIME:
            return True
    return False

def hash_password(password: str) -> str:
    try:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()
    except Exception as e:
        logging.error(f"Error hashing password: {e}")
        return None

def check_password(hashed_password: str, password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    except Exception as e:
        logging.error(f"Error checking password: {e}")
        return False

def authenticate_user(users: list, username: str, password: str) -> bool:
    if is_locked(username):
        logging.warning(f"Account locked for user: {username}")
        return False
    for user in users:
        if user["username"] == username and check_password(user["password"], password):
            failed_attempts.pop(username, None)
            logging.info(f"User {username} authenticated successfully.")
            return True
    attempts, _ = failed_attempts.get(username, (0, 0))
    failed_attempts[username] = (attempts + 1, time())
    if failed_attempts[username][0] >= MAX_ATTEMPTS:
        logging.warning(f"User {username} is locked due to too many failed attempts.")
    return False

def validate_user_credentials(username: str, password: str, user_data: dict, save_function) -> tuple[bool, str]:
    if not re.match(r'^[\w.@+-]+$', username):
        return False, "Invalid username. Use only letters, numbers, and @/./+/-/_ characters."
    if len(password) < 8:
        return False, "Password too short."
    if any(user["username"] == username for user in user_data["users"]):
        return False, "Username already exists."
    hashed_password = hash_password(password)
    if hashed_password is None:
        return False, "Error hashing password."
    user_data["users"].append({"username": username, "password": hashed_password})
    try:
        save_function(user_data)
        logging.info(f"User {username} registered successfully.")
        return True, "Registration successful."
    except Exception as e:
        logging.error(f"Error saving user data: {e}")
        return False, "Error saving user data."
