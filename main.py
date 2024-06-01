import flet as ft
from gui import create_gui

def main(page: ft.Page):
    page.title = "CryptGuardian"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.full_screen = True  # Set full screen mode
    try:
        create_gui(page)
    except Exception as e:
        print(f"Error creating GUI: {e}")

if __name__ == "__main__":
    ft.app(target=main)
