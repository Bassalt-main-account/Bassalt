from flet import Page, app, AppView, Column, Container, alignment
from src.UI.components.menu.TopMenu import TopMenu
from src.UI.components.menu.BelowBar import BelowBar
from src.UI.components.screen.Screen import Screen
from assets.colors import get_color

def main(page: Page):
    # Configuración inicial de la página
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

    # Crear componentes principales
    topMenu = TopMenu(page)
    screen = Screen(page)
    belowBar = BelowBar(page, screen)

    # Estructura principal de la página
    page.add(
        Column(
            [
                # Menú superior
                Container(
                    topMenu,
                    alignment=alignment.top_center,
                    expand=False,
                ),
                # Contenedor principal con Screen
                Container(
                    content=screen,
                    expand=True,
                    alignment=alignment.center,
                ),
                # Barra inferior
                Container(
                    content=Column([belowBar,Container(height=20)]),    
                    alignment=alignment.bottom_center,
                    expand=False,
                ),
            ],
            expand=True,
        )
    )

    page.update()

app(target=main, view=AppView.FLET_APP_WEB, assets_dir="assets")
