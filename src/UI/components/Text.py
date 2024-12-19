from flet import Text
from .ThemedWidget import ThemedWidget
from assets.colors import COLORS as c


# Nuevo widget que también hereda de ThemedWidget
class Text(Text, ThemedWidget):
    def __init__(self, value, page, size=14, font="firasansMedium", color=None):
        self.page = page
        self.original_size = 14
        color = color if color is not None else self._get_color("text")
        super().__init__(value=value, size=size, color=color, font_family=font)
        ThemedWidget.__init__(self)
        
    def _get_color(self, color_key):
        theme = self.page.theme_mode 
        return c[theme][color_key]
    
    def update_theme(self):
        """Actualiza el color del texto según el tema actual."""
        self.color = self._get_color("text")
        self.update()
