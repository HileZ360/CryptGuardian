import flet as ft
from gui import create_gui

def main(page: ft.Page):
    page.title = "CryptGuardian"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    create_gui(page)

ft.app(target=main)
