from flet import Page, app, Column, Row, ElevatedButton, ButtonStyle
from src.UI.components.Button import Button
from src.UI.components.ButtonGroup import ButtonGroup
from src.UI.components.Text import Text
from src.UI.components.toggleThemeButton import ToggleThemeButton

def main(page: Page):
    
    page.title = "Bassalt"
    page.window.icon = "isotipe.ico"
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
        
    # Layout de la página
    page.add(
        Column([ 
            Row([
                Row([
                    Button(page, "isotipe_transparent.svg", group=button_group, color_key="icon", bgcolor_key="default"),
                    Button(page, "ADD_CIRCLE_ROUNDED", group=button_group),
                    Button(page, "LAYERS_ROUNDED", group=button_group),
                    Button(page, "ALT_ROUTE_ROUNDED", group=button_group),
                    Button(page, "STORAGE_ROUNDED", group=button_group),
                    Button(page, "EXTENSION_ROUNDED", group=button_group),
                    ],spacing=20
                ),
                Row([
                    Text(page, "untitled", color_key="text"),
                    Text(page, "bassalt.app.untitled", color_key="default"),
                    ],spacing=10
                ),
                Row([
                    ElevatedButton(
                        content=Text(page, "Publish", color_key="text"),
                        bgcolor="#5D64AC",
                        style=ButtonStyle(padding=15)
                    ),
                    Button(page, "SHARE_ROUNDED"),
                    Button(page, "PLAY_ARROW_ROUNDED"),
                    Button(page, "SETTINGS_ROUNDED"),   
                    Button(page, "PERSON_ROUNDED"),
                    ToggleThemeButton(page),
                    ],spacing=20
                ),
                

            ],alignment="center",spacing=60),



        ])
    ) 



app(target=main)
