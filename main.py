from flet import Page, app, Column, Row
from src.UI.components.Button import Button
from src.UI.components.ButtonGroup import ButtonGroup
from src.UI.components.Text import Text
from src.UI.components.toggleThemeButton import ToggleThemeButton

# PRUEBAS
def main(page: Page):

    page.theme_mode = "dark"
    page.fonts = {
        "firacodeBold": "fonts/FiraCode-Bold.ttf",
        "firacodeSemiBold": "fonts/FiraCode-SemiBold.ttf",
        "firacodeMedium": "fonts/FiraCode-Medium.ttf",
    }

    # Crear un grupo de botones
    button_group = ButtonGroup()

    # Widgets adicionales
    text = Text("Hello, Themed World!", page)

    # Layout de la página
    page.add(
        Column([
            ToggleThemeButton(page),
            text,
            Row([
                Button("ADD_ROUNDED", page, lambda e: print("Clicked"),button_group),
                Button("DASHBOARD_ROUNDED", page,  lambda e: print("Clicked"), button_group),
                Button("LAYERS_ROUNDED", page,  lambda e: print("Clicked"), button_group),
                Button("isotipe_transparent.svg", page,  lambda e: print("Clicked"), button_group)
            ]),
        ])
    )

    
app(target=main)
