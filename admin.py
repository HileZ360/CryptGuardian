import json
import flet as ft
from utils import validate_date, load_json_file, save_json_file
from security import hash_password

KEYS_FILE = "keys.json"

class AdminPanel:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Admin Panel"
        self.page.full_screen = True  # Set full screen mode
        self.status_text = ft.Text(value="")
        self.init_ui()

    def load_keys(self) -> dict:
        try:
            return load_json_file(KEYS_FILE, {"keys": []})
        except Exception as e:
            self.status_text.value = f"Error loading keys: {str(e)}"
            return {"keys": []}

    def save_keys(self, data: dict):
        try:
            save_json_file(KEYS_FILE, data)
        except Exception as e:
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

    def init_ui(self):
        self.key_field = ft.TextField(label="Key")
        self.start_date_field = ft.TextField(label="Start Date (YYYY-MM-DD)")
        self.end_date_field = ft.TextField(label="End Date (YYYY-MM-DD)")
        self.access_info_field = ft.TextField(label="Access Information")

        add_key_button = ft.ElevatedButton(text="Add Key", on_click=self.add_key)

        self.page.add(
            ft.Column(
                [
                    ft.Text("Admin Panel", size=40, weight=ft.FontWeight.BOLD),
                    self.key_field,
                    self.start_date_field,
                    self.end_date_field,
                    self.access_info_field,
                    add_key_button,
                    self.status_text
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

def main(page: ft.Page):
    AdminPanel(page)

if __name__ == "__main__":
    ft.app(target=main)
