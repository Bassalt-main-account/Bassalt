from src.UI.components.button.Button import Button
from .ThemedWidget import ThemedWidget
from assets.colors import get_color

class ToggleThemeButton(Button):
    def __init__(self, page):
        super().__init__(page, "BRIGHTNESS_5", on_click=self.toggle_theme)
    
    def toggle_theme(self, e):
        self.page.theme_mode = "dark" if self.page.theme_mode == "light" else "light"
        self.content.name = "BRIGHTNESS_3" if self.page.theme_mode == "light" else "BRIGHTNESS_5"
        # Actualizar el color de fondo según el tema
        self.page.bgcolor = get_color(self.page.theme_mode, "background2") 
        # Actualizar la página y los widgets temáticos
        self.page.update()
        self.update_theme()
        ThemedWidget.update_all()