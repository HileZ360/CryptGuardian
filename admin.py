import html
import flet as ft
import logging
import threading
from datetime import datetime
from infrastructure.utils import validate_date, load_json_file, save_json_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

KEYS_FILE = "data/keys.json"
file_lock = threading.Lock()

class AdminPanel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.status_text = ft.Text("", color=ft.colors.GREY, size=18)
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
            primary=ft.colors.BLUE_GREY_100,
            on_primary=ft.colors.BLACK,
            secondary=ft.colors.BLUE_GREY_200,
            on_secondary=ft.colors.BLACK,
            background=ft.colors.WHITE,
            on_background=ft.colors.BLACK,
            surface=ft.colors.WHITE,
            on_surface=ft.colors.BLACK,
            error=ft.colors.RED_400,
            on_error=ft.colors.WHITE,
        )
        dark_colors = ft.ColorScheme(
            primary=ft.colors.BLUE_GREY_900,
            on_primary=ft.colors.WHITE,
            secondary=ft.colors.BLUE_GREY_700,
            on_secondary=ft.colors.WHITE,
            background=ft.colors.BLACK,
            on_background=ft.colors.WHITE,
            surface=ft.colors.BLACK,
            on_surface=ft.colors.WHITE,
            error=ft.colors.RED_400,
            on_error=ft.colors.WHITE,
        )

        text_theme = ft.TextTheme(
            title_large=ft.TextStyle(size=32),
            title_medium=ft.TextStyle(size=24),
            body_medium=ft.TextStyle(size=18),
            body_small=ft.TextStyle(size=16),
        )

        self.page.theme = ft.Theme(
            color_scheme=light_colors,
            visual_density=ft.VisualDensity.COMFORTABLE,
            text_theme=text_theme,
        )
        self.page.dark_theme = ft.Theme(
            color_scheme=dark_colors,
            visual_density=ft.VisualDensity.COMFORTABLE,
            text_theme=text_theme,
        )

    def create_text_field(self, label: str, hint_text: str = "") -> ft.TextField:
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            border_radius=12,
            filled=True,
            bgcolor=ft.colors.with_opacity(0.06, ft.colors.ON_SURFACE),
            border_color=ft.colors.with_opacity(0.15, ft.colors.ON_SURFACE),
            color=ft.colors.ON_SURFACE,
            text_size=16,
            height=65,
            content_padding=ft.padding.only(left=20, right=20, top=8, bottom=8),
            focused_border_color=ft.colors.BLUE_400,
            focused_bgcolor=ft.colors.with_opacity(0.12, ft.colors.ON_SURFACE),
        )

    def init_ui(self):
        self.key_field = self.create_text_field("Ключ доступа", "Введите ключ доступа")
        self.start_date_field = self.create_text_field("Дата начала", "ГГГГ-ММ-ДД")
        self.end_date_field = self.create_text_field("Дата окончания", "ГГГГ-ММ-ДД")
        self.access_info_field = self.create_text_field("Информация о доступе", "Введите информацию о доступе")

        add_key_button = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ADD_ROUNDED, color=ft.colors.WHITE),
                    ft.Text("Добавить ключ", size=18, weight=ft.FontWeight.W_600),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_400,
                surface_tint_color=ft.colors.BLUE_200,
                elevation=2,
                padding=ft.padding.only(top=20, bottom=20, left=30, right=30),
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            on_click=self.add_key,
        )

        admin_title = ft.Row(
            [
                ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED, size=48, color=ft.colors.BLUE_400),
                ft.Text("Панель администратора", size=28, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        intro_text = ft.Text("Управление ключами доступа", size=18, text_align=ft.TextAlign.CENTER)

        inner_col = ft.Column(
            [
                ft.Container(
                    content=ft.Column([admin_title, intro_text], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    margin=ft.margin.only(bottom=20),
                ),
                self.key_field,
                self.start_date_field,
                self.end_date_field,
                self.access_info_field,
                ft.Container(content=add_key_button, margin=ft.margin.only(top=15)),
                self.status_text,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        main_container = ft.Container(
            content=inner_col,
            padding=40,
            border_radius=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1A1A1A", "#141414"],
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.ON_SURFACE)),
        )

        self.page.add(
            ft.Container(
                content=main_container,
                margin=ft.margin.only(top=20, bottom=20),
                shadow=ft.BoxShadow(
                    spread_radius=8,
                    blur_radius=20,
                    color=ft.colors.with_opacity(0.1, ft.colors.ON_SURFACE),
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
        from html import escape
        key = escape(self.key_field.value.strip())
        start_date = self.start_date_field.value.strip()
        end_date = self.end_date_field.value.strip()
        access_info = escape(self.access_info_field.value.strip())

        if not key or not start_date or not end_date or not access_info:
            self.status_text.value = "All fields are required."
            self.page.update()
            return
        if len(key) > 100 or len(access_info) > 255:
            self.status_text.value = "Input is too long."
            self.page.update()
            return

        try:
            sd = datetime.strptime(start_date, "%Y-%m-%d")
            ed = datetime.strptime(end_date, "%Y-%m-%d")
            if sd > ed:
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
