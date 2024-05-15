import json
import flet as ft

KEYS_FILE = "keys.json"

def load_keys():
    try:
        with open(KEYS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"keys": []}

def save_keys(data):
    with open(KEYS_FILE, "w") as file:
        json.dump(data, file, indent=4)

def create_admin_interface(page):
    page.title = "Admin Panel"

    def add_key(e):
        key = key_field.value
        start_date = start_date_field.value
        end_date = end_date_field.value
        access_info = access_info_field.value

        if not key or not start_date or not end_date or not access_info:
            status_text.value = "All fields are required."
        else:
            keys = load_keys()
            keys["keys"].append({
                "key": key,
                "start_date": start_date,
                "end_date": end_date,
                "access_info": access_info
            })
            save_keys(keys)
            status_text.value = "Key added successfully."
            key_field.value = ""
            start_date_field.value = ""
            end_date_field.value = ""
            access_info_field.value = ""
        page.update()

    key_field = ft.TextField(label="Key")
    start_date_field = ft.TextField(label="Start Date (YYYY-MM-DD)")
    end_date_field = ft.TextField(label="End Date (YYYY-MM-DD)")
    access_info_field = ft.TextField(label="Access Information")

    add_key_button = ft.ElevatedButton(text="Add Key", on_click=add_key)
    status_text = ft.Text(value="")

    page.add(
        ft.Column(
            [
                ft.Text("Admin Panel", size=40, weight=ft.FontWeight.BOLD),
                key_field,
                start_date_field,
                end_date_field,
                access_info_field,
                add_key_button,
                status_text
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

def main(page: ft.Page):
    create_admin_interface(page)

ft.app(target=main)
