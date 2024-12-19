from flet import Page, app, Column, Row
from src.UI.components.Button import Button
from src.UI.components.ButtonGroup import ButtonGroup
from src.UI.components.Text import Text
from src.UI.components.toggleThemeButton import ToggleThemeButton
# PRUEBAS
def main(page: Page):

    page.theme_mode = "dark"
    
    page.fonts = {
        "firasansBold": "fonts/FiraSans-Bold.ttf",
        "firasansSemiBold": "fonts/FiraSans-SemiBold.ttf",
        "firasansMedium": "fonts/FiraSans-Medium.ttf",
        "firasansRegular": "fonts/FiraSans-Regular.ttf",
        "firasansLight": "fonts/FiraSans-Light.ttf",
    }

    # Crear un grupo de botones
    button_group = ButtonGroup()

    def on_click(e):
        print("Clicked")
        
    # Layout de la página
    page.add(
        Column([
            ToggleThemeButton(page),
            Text("Hello, Themed World!", page, 20, "firasansBold"),
            Row([
                Button("ADD_ROUNDED", page, on_click, button_group),
                Button("DASHBOARD_ROUNDED", page,  on_click, button_group),
                Button("LAYERS_ROUNDED", page,  on_click, button_group),
                Button("isotipe_transparent.svg", page,  on_click, button_group)
            ]),
        ])
    )




app(target=main)
