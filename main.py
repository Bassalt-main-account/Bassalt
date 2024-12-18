import flet as ft
from src.UI.components.ThemedButton import ThemedButton
from src.UI.components.ButtonGroup import ButtonGroup
from src.UI.components.ThemedText import ThemedText
from src.UI.components.ThemedWidget import ThemedWidget
from src.UI.components.toggleThemeButton import ToggleThemeButton

# PRUEBAS
def main(page: ft.Page):
    page.theme_mode = "dark"

    # Lista de botones e inicialización
    icons = ["add_rounded", "DASHBOARD_ROUNDED", "LAYERS_ROUNDED", "isotipe_transparent.svg"]
    button_group = ButtonGroup()
    buttons = [
        ThemedButton(icon, lambda e: print("Clicked"), page, button_group)
        for icon in icons
    ]

    # Widgets adicionales
    themed_text = ThemedText("Hello, Themed World!", page)

    # Layout de la página
    page.add(
        ft.Column([
            ToggleThemeButton(page),
            themed_text,
            ft.Row(buttons),
        ])
    )

ft.app(target=main)
