from flet import Page, app, Column, Row, ElevatedButton, ButtonStyle
from src.UI.components.button.Button import Button
from src.UI.components.button.ButtonGroup import ButtonGroup
from src.UI.components.text.Text import Text
from src.UI.components.theming.toggleThemeButton import ToggleThemeButton
from assets.colors import get_color 

def main(page: Page):
    
    #region Page config
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

    #region Top Menu
    top_menu = Row([
        Row([
            Button(page, "isotipe_transparent.svg", group=button_group),
            Button(page, "ADD_CIRCLE_ROUNDED", group=button_group),
            Button(page, "LAYERS_ROUNDED", group=button_group),
            Button(page, "ALT_ROUTE_ROUNDED", group=button_group),
            Button(page, "STORAGE_ROUNDED", group=button_group),
            Button(page, "EXTENSION_ROUNDED", group=button_group),
            ],spacing=25
        ),
        Row([
            Text(page, "untitled", color_key="text"),
            Text(page, "bassalt.app.untitled", color_key="default"),
            ],spacing=10
        ),
        Row([
            ElevatedButton(
                content=Text(page, "Publish", color_key="text"),
                bgcolor=get_color(page.theme_mode, "primary"),
                style=ButtonStyle(padding=15)
            ),
            Button(page, "SHARE_ROUNDED"),
            Button(page, "PLAY_ARROW_ROUNDED"),
            Button(page, "SETTINGS_ROUNDED"),   
            Button(page, "PERSON_ROUNDED"),
            ToggleThemeButton(page),
            ],spacing=25
        ),
    ],
    alignment="center",
    spacing=60,
    )


    # Layout de la página
    page.add(
        Column([
            top_menu
        ])
    ) 


app(target=main)
