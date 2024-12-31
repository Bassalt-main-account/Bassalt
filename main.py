from flet import (
    Page, app, AppView,
    Stack, Container, Alignment, Row, Border, border
)
from src.UI.components.menu.TopMenu import TopMenu
from src.UI.components.menu.BelowBar import BelowBar
from src.UI.components.screen.Screen import Screen
from assets.colors import get_color

def main(page: Page):
    page.title = "Bassalt"
    page.window.icon = "isotipe.ico"
    page.theme_mode = "dark"
    page.bgcolor = get_color(page.theme_mode, "background2")
    page.padding = 0
    page.horizontal_alignment = "center"
    page.fonts = {
        "firasansBold": "fonts/FiraSans-Bold.ttf",
        "firasansSemiBold": "fonts/FiraSans-SemiBold.ttf",
        "firasansMedium": "fonts/FiraSans-Medium.ttf",
        "firasansRegular": "fonts/FiraSans-Regular.ttf",
        "firasansLight": "fonts/FiraSans-Light.ttf",
    }

    top_menu = TopMenu(page)
    top_menu_container = Container(top_menu,top=0)

    screen = Screen(page)
    screen_container = Container(screen,top=100)

    below_bar = BelowBar(page, screen)
    below_bar_container = Container(below_bar,bottom=20)

    page.add(
        Stack(
            controls=[
                screen_container, 
                top_menu_container,
                below_bar_container
            ],
            expand=True,
            expand_loose=True,
            alignment=Alignment(0,0)
        )
    )

app(target=main, view=AppView.FLET_APP_WEB, assets_dir="assets")
