from flet import Page, app
from src.UI.components.menu.TopMenu import TopMenu
from assets.colors import get_color

def main(page: Page):
    
    #region Page config
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

    # Layout de la página
    page.add(TopMenu(page))
    page.add
    page.update() 


app(target=main)
