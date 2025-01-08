from flet import Container, Row, Column, ScrollMode, padding
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from src.UI.components.text.Text import Text
from assets.colors import get_color

class Layers(Container, ThemedWidget):
    def __init__(self, page, close_menu):
        ThemedWidget.__init__(self)
        self.page = page

        color = get_color(self.page.theme_mode, "background")

        super().__init__(
            bgcolor=color,
            padding=padding.symmetric(20, 20),
            border_radius=15,
            height=700,  # Limita la altura del contenedor principal
        )


    def update_theme(self):
        """
        Actualiza el color de fondo (y potencialmente otros estilos) 
        cuando cambia el tema de la página.
        """
        self.bgcolor = get_color(self.page.theme_mode, "background")
        self.update()
