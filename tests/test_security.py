import pytest
from domain.security import hash_password, check_password, authenticate_user, validate_user_credentials

def test_hash_password():
    password = "securepassword"
    hashed_password = hash_password(password)
    assert hashed_password is not None
    assert check_password(hashed_password, password)

def test_authenticate_user():
    users = [
        {"username": "testuser", "password": hash_password("securepassword")}
    ]
    assert authenticate_user(users, "testuser", "securepassword")
    assert not authenticate_user(users, "testuser", "wrongpassword")

def test_validate_user_credentials():
    user_data = {"users": []}
    save_function = lambda x: None
    assert validate_user_credentials("newuser", "securepassword", user_data, save_function) == (True, "Registration successful.")
    assert validate_user_credentials("newuser", "short", user_data, save_function) == (False, "Password too short.")
    user_data["users"].append({"username": "newuser", "password": hash_password("securepassword")})
    assert validate_user_credentials("newuser", "securepassword", user_data, save_function) == (False, "Username already exists.")
