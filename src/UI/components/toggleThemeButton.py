from .Button import Button
from .ThemedWidget import ThemedWidget

class ToggleThemeButton(Button):
    def __init__(self, page):
        super().__init__("BRIGHTNESS_HIGH_SHARP", page, self.toggle_theme)
    
    def toggle_theme(self, e):
        self.page.theme_mode = "dark" if self.page.theme_mode == "light" else "light"
        self.content.name = "NIGHTLIGHT_ROUNDED" if self.page.theme_mode == "light" else "BRIGHTNESS_HIGH_SHARP"
        self.page.update()
        self.update_theme()
        ThemedWidget.update_all()