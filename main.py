import flet as ft
from presentation.gui import CryptGuardian
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(page: ft.Page):
    page.title = "CryptGuardian"
    page.window.width = 1280
    page.window.height = 850
    page.window.resizable = False
    page.window.center()
    page.theme_mode = ft.ThemeMode.SYSTEM

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

    page.theme = ft.Theme(
        color_scheme=light_colors,
        visual_density=ft.VisualDensity.COMFORTABLE,
        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(size=28),
            title_medium=ft.TextStyle(size=22),
            body_medium=ft.TextStyle(size=16),
            body_small=ft.TextStyle(size=14),
        ),
    )
    page.dark_theme = ft.Theme(
        color_scheme=dark_colors,
        visual_density=ft.VisualDensity.COMFORTABLE,
        text_theme=ft.TextTheme(
            title_large=ft.TextStyle(size=28),
            title_medium=ft.TextStyle(size=22),
            body_medium=ft.TextStyle(size=16),
            body_small=ft.TextStyle(size=14),
        ),
    )

    CryptGuardian(page)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
