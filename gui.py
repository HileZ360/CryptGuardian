import flet as ft
import json
from datetime import datetime
from security import hash_password, validate_user_credentials, authenticate_user
from utils import load_json_file, save_json_file

USER_CREDENTIALS_FILE = "user_credentials.json"
LOGIN_HISTORY_FILE = "login_history.json"
KEYS_FILE = "keys.json"

class CryptGuardian:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "CryptGuardian"
        self.username = ""
        self.init_ui()

    def load_user_credentials(self) -> dict:
        return load_json_file(USER_CREDENTIALS_FILE, {"users": []})

    def save_user_credentials(self, data: dict):
        save_json_file(USER_CREDENTIALS_FILE, data)

    def load_login_history(self) -> dict:
        return load_json_file(LOGIN_HISTORY_FILE, {"logins": []})

    def save_login_history(self, data: dict):
        save_json_file(LOGIN_HISTORY_FILE, data)

    def load_keys(self) -> dict:
        return load_json_file(KEYS_FILE, {"keys": []})

    def save_keys(self, data: dict):
        save_json_file(KEYS_FILE, data)

    def login(self, username: str, password: str) -> bool:
        users = self.load_user_credentials()["users"]
        return authenticate_user(users, username, password)

    def register(self, username: str, password: str) -> tuple[bool, str]:
        return validate_user_credentials(username, password, self.load_user_credentials(), self.save_user_credentials)

    def change_password(self, username: str, old_password: str, new_password: str) -> tuple[bool, str]:
        users = self.load_user_credentials()
        for user in users["users"]:
            if user["username"] == username and user["password"] == hash_password(old_password):
                if len(new_password) < 8:
                    return False, "New password too short."
                user["password"] = hash_password(new_password)
                self.save_user_credentials(users)
                return True, "Password changed successfully."
        return False, "Old password is incorrect."

    def init_ui(self):
        self.page.add(ft.Image(src="background_image.jpg", width=800, height=600))

        self.username_field = ft.TextField(label="Username")
        self.password_field = ft.TextField(label="Password", password=True)
        self.status_text = ft.Text(value="")

        login_button = ft.ElevatedButton(text="Login", on_click=self.on_login_click)
        register_button = ft.ElevatedButton(text="Register", on_click=self.on_register_click)

        self.page.add(
            ft.Column(
                [
                    ft.Text("CryptGuardian", size=40, weight=ft.FontWeight.BOLD),
                    self.username_field,
                    self.password_field,
                    login_button,
                    register_button,
                    self.status_text
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def on_login_click(self, e: ft.ControlEvent):
        username = self.username_field.value
        password = self.password_field.value
        if self.login(username, password):
            self.status_text.value = "Login successful!"
            self.page.update()
            self.show_main_interface(username)
        else:
            self.status_text.value = "Login failed. Please check your username and password."
            self.page.update()

    def on_register_click(self, e: ft.ControlEvent):
        username = self.username_field.value
        password = self.password_field.value
        success, message = self.register(username, password)
        self.status_text.value = message
        self.page.update()

    def on_change_password_click(self, e: ft.ControlEvent):
        old_password = self.old_password_field.value
        new_password = self.new_password_field.value
        success, message = self.change_password(self.username, old_password, new_password)
        self.password_status_text.value = message
        self.page.update()

    def show_main_interface(self, username: str):
        self.page.clean()
        self.username = username

        self.old_password_field = ft.TextField(label="Old Password", password=True)
        self.new_password_field = ft.TextField(label="New Password", password=True)
        self.password_status_text = ft.Text(value="")

        change_password_button = ft.ElevatedButton(text="Change Password", on_click=self.on_change_password_click)

        key_field = ft.TextField(label="Enter Key")
        key_status_text = ft.Text(value="")
        key_info_text = ft.Text(value="")

        def check_key(e: ft.ControlEvent):
            key_value = key_field.value.strip()
            keys = self.load_keys()["keys"]
            current_date = datetime.now().isoformat()[:10]
            for key in keys:
                if key["key"] == key_value:
                    if key["start_date"] <= current_date <= key["end_date"]:
                        key_status_text.value = "Key accepted! Access granted."
                        key_info_text.value = key["access_info"]
                    else:
                        key_status_text.value = "Key expired or not active yet."
                    break
            else:
                key_status_text.value = "Invalid key."
            self.page.update()

        check_key_button = ft.ElevatedButton(text="Submit Key", on_click=check_key)
        github_button = ft.ElevatedButton(text="GitHub", on_click=lambda _: self.page.launch_url("https://github.com/HileZ360/CryptGuardian"))

        self.page.add(
            ft.Column(
                [
                    ft.Text("CryptGuardian", size=40, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Welcome, {username}", size=30, weight=ft.FontWeight.BOLD),
                    self.old_password_field,
                    self.new_password_field,
                    change_password_button,
                    self.password_status_text,
                    key_field,
                    ft.Row([check_key_button, github_button]),
                    key_status_text,
                    key_info_text
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

def create_gui(page: ft.Page):
    CryptGuardian(page)

if __name__ == "__main__":
    ft.app(target=create_gui)
