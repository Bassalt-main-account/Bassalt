from flet import Page, app, Column, Row
from src.UI.components.Button import Button
from src.UI.components.ButtonGroup import ButtonGroup
from src.UI.components.Text import Text
from src.UI.components.toggleThemeButton import ToggleThemeButton


def main(page: Page):
    page.title = "Bassalt"
    page.window.icon = "icon.ico"
    page.window.width = 1000
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
                Button("ADD_ROUNDED", page, on_click, button_group,col={"sm": 4, "md": 4, "xl": 4},),
                Button("DASHBOARD_ROUNDED", page,  on_click, button_group,col={"sm": 4, "md": 4, "xl": 4},),
                Button("LAYERS_ROUNDED", page,  on_click, button_group,col={"sm": 4, "md": 4, "xl": 4},),
                Button("isotipe_transparent.svg", page,  on_click, button_group,col={"sm": 4, "md": 4, "xl": 4},)
            ])
        ])
    )



app(target=main)
