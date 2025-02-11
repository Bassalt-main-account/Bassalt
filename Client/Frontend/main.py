from flet import Page, app, Stack, Container, Alignment, AppView
from src.UI.components.menu.TopMenu import TopMenu
from src.UI.components.menu.BelowBar import BelowBar
from src.UI.components.screen.Screen import Screen
from assets.colors import get_color

def configure_page(page: Page):
    page.title = "Bassalt"
    page.window.icon = "isotipe.ico"
    page.theme_mode = "dark"
    page.bgcolor = get_color(page.theme_mode, "background2")
    page.window.maximized = True
    page.padding = 0
    page.horizontal_alignment = "center"
    page.fonts = {
        "firasansBold": "fonts/FiraSans-Bold.ttf",
        "firasansSemiBold": "fonts/FiraSans-SemiBold.ttf",
        "firasansMedium": "fonts/FiraSans-Medium.ttf",
        "firasansRegular": "fonts/FiraSans-Regular.ttf",
        "firasansLight": "fonts/FiraSans-Light.ttf",
    }

def build_main_stack(page: Page) -> Stack:
    top_menu_container = Container(TopMenu(page))
    screen_container = Container(Screen(page), top=0, left=0, right=0, bottom=0)
    below_bar_container = Container(BelowBar(page, screen_container.content), bottom=20)
    
    widgets = [screen_container, below_bar_container]
    
    page.add(
        Stack(
            controls=[
                Stack(
                    controls=widgets,
                    expand=True,
                    expand_loose=True,
                    alignment=Alignment(0, 0),
                ),
                top_menu_container
            ],
            expand=True,
        )
    )

    top_menu_container.content.load_menus()
    

def main(page: Page):
    configure_page(page)
    build_main_stack(page)
    


    

app(target=main, assets_dir="assets", view=AppView.FLET_APP)
