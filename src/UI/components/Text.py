from flet import Text as FletText
from .ThemedWidget import ThemedWidget
from .TextStyle import TextStyle
from assets.colors import COLORS as c

class Text(FletText, ThemedWidget):
    def __init__(self, value, page, size=14, font="firasansMedium", color_key="text"):
        """
        Inicializa el widget Text con soporte de temas.
        """
        ThemedWidget.__init__(self)  
        self.page = page

        if color_key not in c["light"] or color_key not in c["dark"]:
            raise KeyError(f"La clave '{color_key}' no está definida en los colores.")

        self.text_style = TextStyle(color_key)
        # Obtiene el color inicial basado en el tema actual
        color = self.text_style.get_color(self.page.theme_mode)

        # Inicializa el texto de Flet
        super().__init__(
            value=value,
            size=size,
            color=color,
            font_family=font,
        )

    def update_theme(self):
        """
        Actualiza el color del texto según el tema actual.
        """
        self.color = self.text_style.get_color(self.page.theme_mode)
        self.update()
