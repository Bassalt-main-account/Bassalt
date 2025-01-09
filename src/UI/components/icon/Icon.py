from flet import Image,Container
from flet import Icon as fletIcon
from src.UI.components.theming.ThemedWidget import ThemedWidget
from assets.colors import get_color
from src.data.cache import get_theme_mode

class Icon(Container, ThemedWidget):
    def __init__(self, page, icon, size=30, color_key="default"):

        ThemedWidget.__init__(self)
        Container.__init__(self)
        
        self.page = page
        self.color_key = color_key
        self.color = get_color(get_theme_mode(), color_key)
        self.size = size
        
        self.content = self._create_icon(icon)
        
        
    def _create_icon(self, icon):
        if icon:  # Si se proporciona un icono, seguimos la lógica existente
            if icon.endswith(".svg"):
                self.padding = self.size * 0.1
                return Image(src="icons/" + icon, color=self.color)
            return fletIcon(name=icon, color=self.color, size=self.size * 0.8)
        return None  # Si no hay ni texto ni icono, devolvemos None


    def update_theme(self):
        self.content.color = get_color(get_theme_mode(), self.color_key)
        if self.page:
            self.update()
        
