import flet as ft
import hashlib
import json
from datetime import datetime

USER_CREDENTIALS_FILE = "user_credentials.json"
LOGIN_HISTORY_FILE = "login_history.json"
KEYS_FILE = "keys.json"

def load_json_file(file_path, default_data):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return default_data

def save_json_file(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def load_user_credentials():
    return load_json_file(USER_CREDENTIALS_FILE, {"users": []})

def save_user_credentials(data):
    save_json_file(USER_CREDENTIALS_FILE, data)

def load_login_history():
    return load_json_file(LOGIN_HISTORY_FILE, {"logins": []})

def save_login_history(data):
    save_json_file(LOGIN_HISTORY_FILE, data)

def load_keys():
    return load_json_file(KEYS_FILE, {"keys": []})

def save_keys(data):
    save_json_file(KEYS_FILE, data)

def create_gui(page):
    page.title = "CryptGuardian"
    page.add(ft.Image(src="background_image.jpg", width=800, height=600))

    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(username, password):
        users = load_user_credentials()["users"]
        for user in users:
            if user["username"] == username and user["password"] == hash_password(password):
                login_history = load_login_history()
                if "logins" not in login_history:
                    login_history["logins"] = []
                login_history["logins"].append({"username": username, "time": datetime.now().isoformat()})
                save_login_history(login_history)
                return True
        return False

    def register(username, password):
        users = load_user_credentials()
        for user in users["users"]:
            if user["username"] == username:
                return False, "Username already exists."
        if len(password) < 8:
            return False, "Password too short."
        users["users"].append({"username": username, "password": hash_password(password)})
        save_user_credentials(users)
        return True, "Registration successful."

    def on_login_click(e):
        username = username_field.value
        password = password_field.value
        if login(username, password):
            status_text.value = "Login successful!"
            page.update()
            show_main_interface(username)
        else:
            status_text.value = "Login failed. Please check your username and password."
            page.update()

    def on_register_click(e):
        username = username_field.value
        password = password_field.value
        success, message = register(username, password)
        status_text.value = message
        page.update()

    def show_main_interface(username):
        page.clean()

        def check_key(e):
            key_value = key_field.value
            keys = load_keys()["keys"]
            for key in keys:
                if key["key"] == key_value:
                    if key["start_date"] <= datetime.now().isoformat() <= key["end_date"]:
                        key_status_text.value = "Key accepted! Access granted."
                        key_info_text.value = key["access_info"]
                    else:
                        key_status_text.value = "Key expired or not active yet."
                    break
            else:
                key_status_text.value = "Invalid key."
            page.update()

        key_field = ft.TextField(label="Enter Key")
        check_key_button = ft.ElevatedButton(text="Submit Key", on_click=check_key)
        key_status_text = ft.Text(value="")
        key_info_text = ft.Text(value="")

        github_button = ft.ElevatedButton(
            text="GitHub",
            on_click=lambda _: page.launch_url("https://github.com/HileZ360/CryptGuardian")
        )

        page.add(
            ft.Column(
                [
                    ft.Text("CryptGuardian", size=40, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Welcome, {username}", size=30, weight=ft.FontWeight.BOLD),
                    key_field,
                    check_key_button,
                    key_status_text,
                    key_info_text,
                    github_button
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    username_field = ft.TextField(label="Username")
    password_field = ft.TextField(label="Password", password=True)
    status_text = ft.Text(value="")

    login_button = ft.ElevatedButton(text="Login", on_click=on_login_click)
    register_button = ft.ElevatedButton(text="Register", on_click=on_register_click)

    page.add(
        ft.Column(
            [
                ft.Text("CryptGuardian", size=40, weight=ft.FontWeight.BOLD),
                username_field,
                password_field,
                login_button,
                register_button,
                status_text
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

ft.app(target=create_gui)
