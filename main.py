from flet import (
    Page, app, AppView,
    Stack, Container
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
    page.fonts = {
        "firasansBold": "fonts/FiraSans-Bold.ttf",
        "firasansSemiBold": "fonts/FiraSans-SemiBold.ttf",
        "firasansMedium": "fonts/FiraSans-Medium.ttf",
        "firasansRegular": "fonts/FiraSans-Regular.ttf",
        "firasansLight": "fonts/FiraSans-Light.ttf",
    }

    top_menu = TopMenu(page)

    screen = Screen(page)
    screen_container = Container(screen,top=100,left=page.width/2-screen.get_width()/2)

    below_bar = BelowBar(page, screen)
    below_bar_container = Container(below_bar,bottom=20,left=page.width/2-below_bar.w/2)

    page.add(
        Stack(
            controls=[
                screen_container, 
                top_menu,
                below_bar_container
            ],
            expand=True,
        )
    )

    def resize(e):

        screen_container.left = e.width/2-screen.get_width()/2
        below_bar_container.left = e.width/2-below_bar.w/2
        screen_container.update()
        below_bar_container.update()

    page.on_resized = resize
    page.update()


app(target=main, view=AppView.WEB_BROWSER, assets_dir="assets")
