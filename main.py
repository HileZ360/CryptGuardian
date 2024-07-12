# main.py
import flet as ft
from presentation.gui import CryptGuardian
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(page: ft.Page):
    page.title = "CryptGuardian"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.full_screen = True
    try:
        CryptGuardian(page)
    except Exception as e:
        logging.error(f"Error creating GUI: {e}")

if __name__ == "__main__":
    ft.app(target=main)
