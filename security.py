import bcrypt
import re

def hash_password(password: str) -> str:
    try:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    except Exception as e:
        print(f"Error hashing password: {e}")
        return None

def check_password(hashed_password: str, password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    except Exception as e:
        print(f"Error checking password: {e}")
        return False

def authenticate_user(users: list, username: str, password: str) -> bool:
    for user in users:
        if user["username"] == username and check_password(user["password"], password):
            return True
    return False

def validate_user_credentials(username: str, password: str, user_data: dict, save_function) -> tuple[bool, str]:
    if not re.match(r'^[\w.@+-]+$', username):
        return False, "Invalid username."
    if len(password) < 8:
        return False, "Password too short."
    if any(user["username"] == username for user in user_data["users"]):
        return False, "Username already exists."

    hashed_password = hash_password(password)
    if hashed_password is None:
        return False, "Error hashing password."

    user_data["users"].append({
        "username": username,
        "password": hashed_password
    })
    save_function(user_data)
    return True, "Registration successful."
