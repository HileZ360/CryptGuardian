# admin.py
import json
import flet as ft
from infrastructure.utils import validate_date, load_json_file, save_json_file
from domain.security import hash_password
import logging

KEYS_FILE = "keys.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AdminPanel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.status_text = ft.Text("", color=ft.colors.WHITE60, size=14)
        self.setup_page()
        self.init_ui()

    def setup_page(self):
        self.page.title = "CryptGuardian Admin"
        self.page.padding = 30
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.colors.BLUE_GREY_100,
            visual_density=ft.ThemeVisualDensity.COMFORTABLE,
        )
        self.page.window_bgcolor = "#0A0A0A"
        self.page.fonts = {
            "SpaceGrotesk": "fonts/SpaceGrotesk-Medium.ttf"
        }

    def create_text_field(self, label: str, hint_text: str = "") -> ft.TextField:
        return ft.TextField(
            label=label,
            hint_text=hint_text,
            border_radius=12,
            filled=True,
            bgcolor=ft.colors.with_opacity(0.08, ft.colors.WHITE),
            border_color=ft.colors.with_opacity(0.15, ft.colors.WHITE),
            color=ft.colors.WHITE,
            text_size=16,
            height=65,
            content_padding=ft.padding.only(left=20, right=20, top=8, bottom=8),
            focused_border_color=ft.colors.BLUE_400,
            focused_bgcolor=ft.colors.with_opacity(0.12, ft.colors.WHITE),
        )

    def init_ui(self):
        self.key_field = self.create_text_field("Ключ доступа", "Введите ключ доступа")
        self.start_date_field = self.create_text_field("Дата начала", "ГГГГ-ММ-ДД")
        self.end_date_field = self.create_text_field("Дата окончания", "ГГГГ-ММ-ДД")
        self.access_info_field = self.create_text_field("Информация о доступе", "Введите информацию о доступе")

        add_key_button = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.ADD_ROUNDED, color=ft.colors.WHITE),
                    ft.Text("Добавить ключ", size=16, weight=ft.FontWeight.W_500)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_400,
                surface_tint_color=ft.colors.BLUE_200,
                elevation=0,
                padding=ft.padding.only(top=20, bottom=20, left=30, right=30),
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            on_click=self.add_key
        )

        main_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.icons.ADMIN_PANEL_SETTINGS_ROUNDED, 
                                               size=40, 
                                               color=ft.colors.BLUE_400),
                                        ft.Text(
                                            "Панель администратора",
                                            size=32,
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.colors.WHITE,
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Text(
                                    "Управление ключами доступа",
                                    size=16,
                                    color=ft.colors.WHITE60,
                                    text_align=ft.TextAlign.CENTER,
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5
                        ),
                        margin=ft.margin.only(bottom=30)
                    ),
                    self.key_field,
                    self.start_date_field,
                    self.end_date_field,
                    self.access_info_field,
                    ft.Container(
                        content=add_key_button,
                        margin=ft.margin.only(top=10)
                    ),
                    self.status_text
                ],
                spacing=15,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=40,
            border_radius=20,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=["#1A1A1A", "#141414"]
            ),
            border=ft.border.all(1, ft.colors.with_opacity(0.1, ft.colors.WHITE)),
        )

        self.page.add(
            ft.Container(
                content=main_container,
                margin=ft.margin.only(top=20, bottom=20),
                shadow=ft.BoxShadow(
                    spread_radius=8,
                    blur_radius=20,
                    color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                )
            )
        )

    def load_keys(self) -> dict:
        try:
            return load_json_file(KEYS_FILE, {"keys": []})
        except Exception as e:
            logging.error(f"Error loading keys: {str(e)}")
            self.status_text.value = f"Error loading keys: {str(e)}"
            return {"keys": []}

    def save_keys(self, data: dict):
        try:
            save_json_file(KEYS_FILE, data)
        except Exception as e:
            logging.error(f"Error saving keys: {str(e)}")
            self.status_text.value = f"Error saving keys: {str(e)}"

    def add_key(self, e: ft.ControlEvent):
        key = self.key_field.value.strip()
        start_date = self.start_date_field.value.strip()
        end_date = self.end_date_field.value.strip()
        access_info = self.access_info_field.value.strip()

        if not key or not start_date or not end_date or not access_info:
            self.status_text.value = "All fields are required."
        elif not validate_date(start_date) or not validate_date(end_date):
            self.status_text.value = "Invalid date format. Use YYYY-MM-DD."
        elif start_date > end_date:
            self.status_text.value = "Start date must be before end date."
        else:
            keys = self.load_keys()
            if any(k["key"] == key for k in keys["keys"]):
                self.status_text.value = "Key already exists."
            else:
                keys["keys"].append({
                    "key": key,
                    "start_date": start_date,
                    "end_date": end_date,
                    "access_info": access_info
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

if __name__ == "__main__":
    ft.app(target=main)
