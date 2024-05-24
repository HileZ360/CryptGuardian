import hashlib
import re

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(users, username, password):
    hashed_password = hash_password(password)
    for user in users:
        if user["username"] == username and user["password"] == hashed_password:
            return True
    return False

def validate_user_credentials(username, password, user_data, save_function):
    if not re.match(r'^[\w.@+-]+$', username):
        return False, "Invalid username."
    if len(password) < 8:
        return False, "Password too short."
    if any(user["username"] == username for user in user_data["users"]):
        return False, "Username already exists."

    user_data["users"].append({
        "username": username,
        "password": hash_password(password)
    })
    save_function(user_data)
    return True, "Registration successful."
