import flet as ft
import logging
from datetime import datetime
from domain.security import authenticate_user, validate_user_credentials
from infrastructure.utils import load_json_file, save_json_file
from domain.models import User, SystemInfo
from domain.services import SystemInfoService, UserService
import html

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

USER_CREDENTIALS_FILE = "user_credentials.json"
LOGIN_HISTORY_FILE = "login_history.json"
KEYS_FILE = "data/keys.json"

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
        self.page.add(ft.Image(src="background_image.jpg", width=1920, height=396))

        # Поля ввода с слегка прозрачным фоном, подстраиваются под тему
        self.username_field = ft.TextField(
            label="Username",
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.ON_SURFACE),
            color=ft.Colors.ON_SURFACE
        )
        self.password_field = ft.TextField(
            label="Password",
            password=True,
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.ON_SURFACE),
            color=ft.Colors.ON_SURFACE
        )

        self.status_text = ft.Text(value="", color=ft.Colors.ON_SURFACE_VARIANT)

        login_button = ft.ElevatedButton(
            text="Login",
            on_click=self.on_login_click,
            style=ft.ButtonStyle(
                color=ft.Colors.ON_PRIMARY,
                bgcolor=ft.Colors.PRIMARY,
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
        register_button = ft.ElevatedButton(
            text="Register",
            on_click=self.on_register_click,
            style=ft.ButtonStyle(
                color=ft.Colors.ON_PRIMARY,
                bgcolor=ft.Colors.SECONDARY,
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )

        # Основной контейнер с нейтральным цветом, адаптирующимся к теме
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "CryptGuardian",
                            size=50,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.ON_SURFACE
                        ),
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
                border_radius=15,
                bgcolor=ft.Colors.SURFACE,
                expand=True,
                shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)),
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
            ft.Text(f"CPU: {system_info.cpu.model}", color=ft.Colors.ON_SURFACE),
            ft.Text(f"Cores: {system_info.cpu.cores}", color=ft.Colors.ON_SURFACE),
            ft.Text(f"Threads: {system_info.cpu.threads}", color=ft.Colors.ON_SURFACE),
            ft.Text(f"CPU Frequency: {system_info.cpu.frequency} MHz", color=ft.Colors.ON_SURFACE),
            ft.Text(f"Memory: {system_info.memory.total // (1024 ** 3)} GB", color=ft.Colors.ON_SURFACE),
            ft.Text(f"Available: {system_info.memory.available // (1024 ** 3)} GB", color=ft.Colors.ON_SURFACE),
            ft.Text(f"Disk Total: {system_info.disk.total // (1024 ** 3)} GB", color=ft.Colors.ON_SURFACE),
            ft.Text(f"Disk Free: {system_info.disk.free // (1024 ** 3)} GB", color=ft.Colors.ON_SURFACE),
            *[
                ft.Text(
                    f"GPU: {gpu.name}, Memory: {gpu.memory_total} MB, Free: {gpu.memory_free} MB",
                    color=ft.Colors.ON_SURFACE
                )
                for gpu in system_info.gpu
            ]
        ])

        self.key_field = ft.TextField(
            label="Enter Key",
            bgcolor=ft.Colors.with_opacity(0.06, ft.Colors.ON_SURFACE),
            color=ft.Colors.ON_SURFACE
        )
        self.key_status_text = ft.Text(value="", color=ft.Colors.ON_SURFACE_VARIANT)
        key_submit_button = ft.ElevatedButton(
            text="Submit Key",
            on_click=self.on_key_submit,
            style=ft.ButtonStyle(
                color=ft.Colors.ON_PRIMARY,
                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )

        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "CryptGuardian",
                            size=50,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.ON_SURFACE
                        ),
                        ft.Text(
                            f"Welcome, {username}",
                            size=30,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.ON_SURFACE
                        ),
                        ft.ElevatedButton(
                            text="Toggle System Info",
                            on_click=self.toggle_system_info,
                            style=ft.ButtonStyle(
                                color=ft.Colors.ON_PRIMARY,
                                bgcolor=ft.Colors.PRIMARY,
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                        ),
                        system_info_display if self.system_info_visible else ft.Container(),
                        ft.Container(
                            padding=10,
                            content=self.create_cpu_usage_graph(),
                            border=ft.BorderSide(1, ft.Colors.with_opacity(0.2, ft.Colors.BLACK))
                        ),
                        self.key_field,
                        key_submit_button,
                        self.key_status_text
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
                ),
                padding=20,
                border_radius=15,
                bgcolor=ft.Colors.SURFACE,
                shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK)),
                expand=True
            )
        )

    def create_cpu_usage_graph(self):
        cpu_percentages = self.system_info_service.get_cpu_usage()
        return ft.Text(f"CPU Usage: {cpu_percentages}%", color=ft.Colors.ON_SURFACE)

    def on_key_submit(self, e: ft.ControlEvent):
        key = self.key_field.value.strip()
        keys_data = self.load_keys()
        for key_data in keys_data["keys"]:
            if key_data["key"] == key:
                self.key_status_text.value = (
                    f"Key: {key}\n"
                    f"Start Date: {key_data['start_date']}\n"
                    f"End Date: {key_data['end_date']}\n"
                    f"Access Info: {key_data['access_info']}"
                )
                self.page.update()
                return
        self.key_status_text.value = "Invalid key."
        self.page.update()
