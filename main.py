from flet import Page, app, Column, Row, ElevatedButton, ButtonStyle
from src.UI.components.Button import Button
from src.UI.components.ButtonGroup import ButtonGroup
from src.UI.components.Text import Text
from src.UI.components.toggleThemeButton import ToggleThemeButton
from assets.colors import COLORS as c

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
            #ToggleThemeButton(page),
            #Text("Hello, Themed World!", page, 20, "firasansBold"),
            Row([
                Row([
                    Button("isotipe_transparent.svg", page, group=button_group),
                    Button("ADD_CIRCLE_ROUNDED", page, group=button_group),
                    Button("LAYERS_ROUNDED", page, group=button_group),
                    Button("ALT_ROUTE_ROUNDED", page, group=button_group),
                    Button("STORAGE_ROUNDED", page, group=button_group),
                    Button("EXTENSION_ROUNDED", page, group=button_group),
                ],spacing=20),
                Row([
                    Text("untitled", page),
                    Text("bassalt.app.untitled", page,color=c[page.theme_mode]["default"]),
                ],spacing=10),
                Row([
                    ElevatedButton(content=Text("Publish", page,color=c[page.theme_mode]["text"]),bgcolor="#5D64AC",style=ButtonStyle(padding=15)),
                    Button("SHARE_ROUNDED", page),
                    Button("PLAY_ARROW_ROUNDED", page),
                    Button("SETTINGS_ROUNDED", page),
                    Button("PERSON_ROUNDED", page),
                    ToggleThemeButton(page),
                ],spacing=20),
                

            ],alignment="center",spacing=60),



        ])
    ) 



app(target=main)
