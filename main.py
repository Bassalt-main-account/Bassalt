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
    screen_container = Container(screen,top=100,left=page.window.width/2-screen.get_width()/2)

    below_bar = BelowBar(page, screen)
    below_bar_container = Container(below_bar,bottom=20,left=page.window.width/2-below_bar.w/2)

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
        if str(e.type) in [
            "WindowEventType.RESIZE",
            "WindowEventType.RESIZED",
            "WindowEventType.MINIMIZE",
            "WindowEventType.MAXIMIZE",
        ]:
            screen_container.left = page.window.width/2-screen.get_width()/2
            below_bar_container.left = page.window.width/2-below_bar.w/2
            screen_container.update()
            below_bar_container.update()

    page.window.on_event = resize
    page.update()


app(target=main, view=AppView.FLET_APP_WEB, assets_dir="assets")
