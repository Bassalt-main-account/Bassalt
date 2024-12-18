from .ThemedButton import ThemedButton
from .ThemedWidget import ThemedWidget

class ToggleThemeButton(ThemedButton):
    def __init__(self, page):
        super().__init__("BRIGHTNESS_HIGH_SHARP", self.toggle_theme, page)
    
    def toggle_theme(self, e):
        self.page.theme_mode = "dark" if self.page.theme_mode == "light" else "light"
        self.content.name = "NIGHTLIGHT_ROUNDED" if self.page.theme_mode == "light" else "BRIGHTNESS_HIGH_SHARP"
        self.page.update()
        self.update_theme()
        ThemedWidget.update_all()