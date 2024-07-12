# presentation/gui.py
import flet as ft
import logging
from datetime import datetime
from domain.security import authenticate_user, validate_user_credentials
from infrastructure.utils import load_json_file, save_json_file
from domain.models import User, SystemInfo
from domain.services import SystemInfoService, UserService

USER_CREDENTIALS_FILE = "user_credentials.json"
LOGIN_HISTORY_FILE = "login_history.json"
KEYS_FILE = "keys.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(asctime)s - %(message)s')

class CryptGuardian:
    def __init__(self, page: ft.Page):
        self.page = page
        self.user_service = UserService()
        self.system_info_service = SystemInfoService()
        self.page.title = "CryptGuardian"
        self.username = ""
        self.system_info_visible = False
        self.init_ui()

    def load_user_credentials(self) -> dict:
        return self.user_service.load_user_credentials()

    def save_user_credentials(self, data: dict):
        self.user_service.save_user_credentials(data)

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
        return self.user_service.change_password(users, username, old_password, new_password)

    def init_ui(self):
        self.page.add(ft.Image(src="background_image.jpg", width=800, height=600))

        self.username_field = ft.TextField(label="Username", bgcolor=ft.colors.BLACK87)
        self.password_field = ft.TextField(label="Password", password=True, bgcolor=ft.colors.BLACK87)
        self.status_text = ft.Text(value="")

        login_button = ft.ElevatedButton(
            text="Login",
            on_click=self.on_login_click,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE,
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
        register_button = ft.ElevatedButton(
            text="Register",
            on_click=self.on_register_click,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.GREEN,
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("CryptGuardian", size=50, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE),
                        self.username_field,
                        self.password_field,
                        login_button,
                        register_button,
                        self.status_text
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                padding=20,
                bgcolor=ft.colors.BLACK87,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.colors.GREY),
                expand=True
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

    def toggle_system_info(self, e: ft.ControlEvent):
        self.system_info_visible = not self.system_info_visible
        self.show_main_interface(self.username)

    def show_main_interface(self, username: str):
        self.page.clean()
        self.username = username

        system_info = self.system_info_service.get_system_info()

        system_info_display = ft.Column([
            ft.Text(f"CPU: {system_info.cpu.model}"),
            ft.Text(f"Cores: {system_info.cpu.cores}"),
            ft.Text(f"Threads: {system_info.cpu.threads}"),
            ft.Text(f"CPU Frequency: {system_info.cpu.frequency} MHz"),
            ft.Text(f"Memory: {system_info.memory.total // (1024 ** 3)} GB"),
            ft.Text(f"Available: {system_info.memory.available // (1024 ** 3)} GB"),
            ft.Text(f"Disk Total: {system_info.disk.total // (1024 ** 3)} GB"),
            ft.Text(f"Disk Free: {system_info.disk.free // (1024 ** 3)} GB"),
            *[
                ft.Text(f"GPU: {gpu.name}, Memory: {gpu.memory_total} MB, Free: {gpu.memory_free} MB")
                for gpu in system_info.gpu
            ]
        ])

        self.key_field = ft.TextField(label="Enter Key")
        self.key_status_text = ft.Text(value="")
        key_submit_button = ft.ElevatedButton(text="Submit Key", on_click=self.on_key_submit)

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("CryptGuardian", size=50, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                        ft.Text(f"Welcome, {username}", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN),
                        ft.ElevatedButton(
                            text="Toggle System Info",
                            on_click=self.toggle_system_info,
                            style=ft.ButtonStyle(
                                color=ft.colors.WHITE,
                                bgcolor=ft.colors.PURPLE,
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                        ),
                        system_info_display if self.system_info_visible else ft.Container(),
                        ft.Container(padding=10, content=self.create_cpu_usage_graph(), border=ft.BorderSide(1, ft.colors.GREY)),
                        self.key_field,
                        key_submit_button,
                        self.key_status_text
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
                ),
                padding=20,
                bgcolor=ft.colors.BLACK87,
                border_radius=15,
                shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.colors.GREY),
                expand=True
            )
        )

    def create_cpu_usage_graph(self):
        cpu_percentages = self.system_info_service.get_cpu_usage()
        return ft.Text(f"CPU Usage: {cpu_percentages}%")

    def on_key_submit(self, e: ft.ControlEvent):
        key = self.key_field.value.strip()
        keys_data = self.load_keys()
        for key_data in keys_data["keys"]:
            if key_data["key"] == key:
                self.key_status_text.value = f"Key: {key}\nStart Date: {key_data['start_date']}\nEnd Date: {key_data['end_date']}\nAccess Info: {key_data['access_info']}"
                self.page.update()
                return
        self.key_status_text.value = "Invalid key."
        self.page.update()
