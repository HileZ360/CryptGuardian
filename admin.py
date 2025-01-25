import html
import flet as ft
from datetime import datetime
from infrastructure.utils import validate_date, load_json_file, save_json_file
import logging
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

KEYS_FILE = "data/keys.json"
file_lock = threading.Lock()

class AdminPanel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.status_text = ft.Text("", color=ft.Colors.ON_SURFACE_VARIANT, size=14)
        self.setup_page()
        self.init_ui()

    def setup_page(self):
        self.page.title = "CryptGuardian Admin"
        self.page.padding = 30
        self.page.window.width = 1280
        self.page.window.height = 720
        self.page.window.resizable = False
        self.page.window.center()
        self.page.theme_mode = ft.ThemeMode.SYSTEM

        light_colors = ft.ColorScheme(
            primary=ft.Colors.BLUE_GREY_100,
            on_primary=ft.Colors.BLACK,
            secondary=ft.Colors.BLUE_GREY_200,
            on_secondary=ft.Colors.BLACK,
            background=ft.Colors.WHITE,
            on_background=ft.Colors.BLACK,
            surface=ft.Colors.WHITE,
            on_surface=ft.Colors.BLACK,
            error=ft.Colors.RED_400,
            on_error=ft.Colors.WHITE,
        )
        dark_colors = ft.ColorScheme(
            primary=ft.Colors.BLUE_GREY_900,
            on_primary=ft.Colors.WHITE,
            secondary=ft.Colors.BLUE_GREY_700,
            on_secondary=ft.Colors.WHITE,
            background=ft.Colors.BLACK,
            on_background=ft.Colors.WHITE,
            surface=ft.Colors.BLACK,
            on_surface=ft.Colors.WHITE,
            error=ft.Colors.RED_400,
            on_error=ft.Colors.WHITE,
        )

        self.page.theme = ft.Theme(
            color_scheme=light_colors,
            visual_density=ft.VisualDensity.COMFORTABLE,
            text_theme=ft.TextTheme(
                title_large=ft.TextStyle(size=28),
                title_medium=ft.TextStyle(size=22),
                body_medium=ft.TextStyle(size=16),
                body_small=ft.TextStyle(size=14),
            ),
        )

        self.page.dark_theme = ft.Theme(
            color_scheme=dark_colors,
            visual_density=ft.VisualDensity.COMFORTABLE,
            text_theme=ft.TextTheme(
                title_large=ft.TextStyle(size=28),
                title_medium=ft.TextStyle(size=22),
                body_medium=ft.TextStyle(size=16),
                body_small=ft.TextStyle(size=14),
            ),
        )

    def create_text_field(self, label: str, hint_text: str = "") -> ft.TextField:
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            border_radius=12,
            filled=True,
            bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.ON_BACKGROUND),
            border_color=ft.Colors.with_opacity(0.15, ft.Colors.ON_BACKGROUND),
            color=ft.Colors.ON_BACKGROUND,
            text_size=16,
            height=65,
            content_padding=ft.padding.only(left=20, right=20, top=8, bottom=8),
            focused_border_color=ft.Colors.BLUE_400,
            focused_bgcolor=ft.Colors.with_opacity(0.12, ft.Colors.ON_BACKGROUND),
        )

    def init_ui(self):
        self.key_field = self.create_text_field("Ключ доступа", "Введите ключ доступа")
        self.start_date_field = self.create_text_field("Дата начала", "ГГГГ-ММ-ДД")
        self.end_date_field = self.create_text_field("Дата окончания", "ГГГГ-ММ-ДД")
        self.access_info_field = self.create_text_field("Информация о доступе", "Введите информацию о доступе")

        add_key_button = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ADD_ROUNDED, color=ft.Colors.ON_PRIMARY),
                    ft.Text("Добавить ключ", size=16, weight=ft.FontWeight.W_500),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                color=ft.Colors.ON_PRIMARY,
                bgcolor=ft.Colors.BLUE_400,
                surface_tint_color=ft.Colors.BLUE_200,
                elevation=1,
                padding=ft.padding.only(top=20, bottom=20, left=30, right=30),
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            on_click=self.add_key,
        )

        main_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED, size=40, color=ft.Colors.BLUE_400),
                                        ft.Text("Панель администратора", size=32, weight=ft.FontWeight.BOLD),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Text(
                                    "Управление ключами доступа",
                                    size=16,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        margin=ft.margin.only(bottom=30),
                    ),
                    self.key_field,
                    self.start_date_field,
                    self.end_date_field,
                    self.access_info_field,
                    ft.Container(content=add_key_button, margin=ft.margin.only(top=10)),
                    self.status_text,
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=40,
            border_radius=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1A1A1A", "#141414"],
            ),
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
        )

        self.page.add(
            ft.Container(
                content=main_container,
                margin=ft.margin.only(top=20, bottom=20),
                shadow=ft.BoxShadow(
                    spread_radius=8,
                    blur_radius=20,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                ),
            )
        )

    def load_keys(self) -> dict:
        with file_lock:
            try:
                return load_json_file(KEYS_FILE, {"keys": []})
            except Exception as e:
                logging.error(f"Error loading keys: {str(e)}")
                self.status_text.value = "Error loading keys."
                self.page.update()
                return {"keys": []}

    def save_keys(self, data: dict):
        with file_lock:
            try:
                save_json_file(KEYS_FILE, data)
            except Exception as e:
                logging.error(f"Error saving keys: {str(e)}")
                self.status_text.value = "Error saving keys."
                self.page.update()

    def add_key(self, e: ft.ControlEvent):
        key = html.escape(self.key_field.value.strip())
        start_date = self.start_date_field.value.strip()
        end_date = self.end_date_field.value.strip()
        access_info = html.escape(self.access_info_field.value.strip())
        if not key or not start_date or not end_date or not access_info:
            self.status_text.value = "All fields are required."
            self.page.update()
            return
        if len(key) > 100 or len(access_info) > 255:
            self.status_text.value = "Input is too long."
            self.page.update()
            return
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if start > end:
                self.status_text.value = "Start date must be before end date."
                self.page.update()
                return
        except ValueError:
            self.status_text.value = "Invalid date format. Use YYYY-MM-DD."
            self.page.update()
            return
        keys = self.load_keys()
        if any(k["key"] == key for k in keys["keys"]):
            self.status_text.value = "Key already exists."
            self.page.update()
            return
        keys["keys"].append({
            "key": key,
            "start_date": start_date,
            "end_date": end_date,
            "access_info": access_info,
        })
        self.save_keys(keys)
        self.status_text.value = "Key added successfully."
        self.key_field.value = ""
        self.start_date_field.value = ""
        self.end_date_field.value = ""
        self.access_info_field.value = ""
        self.page.update()

def main(page: ft.Page):
    AdminPanel(page)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
