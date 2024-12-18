from flet import Text
from .ThemedWidget import ThemedWidget
from assets.colors import COLORS as c


# Nuevo widget que también hereda de ThemedWidget
class ThemedText(Text, ThemedWidget):
    def __init__(self, value, page):
        self.page = page
        super().__init__(value=value, size=20, color=self._get_color("text"))
        ThemedWidget.__init__(self)
        
        
    def _get_color(self, color_key):
        theme =  self.page.theme_mode 
        return c[theme][color_key]
    

    def update_theme(self):
        """Actualiza el color del texto según el tema actual."""
        self.color = self._get_color("text")
        self.update()
