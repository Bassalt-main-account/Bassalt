from flet import Container, Row
from src.UI.components.theming.ThemedWidget import ThemedWidget
from assets.colors import get_color

class Screen(Row, ThemedWidget):
    def __init__(self, page):
        ThemedWidget.__init__(self)  
        self.page = page

        color = get_color(self.page.theme_mode, "background")

        # Contenedor desplazable
        self.container = Container(
            width=800,
            height=450,
            bgcolor=color 
        )

        super().__init__(
            controls=[self.container],
            alignment="center",
            expand=True
        )

    def update_theme(self):
        """
        Actualiza el color del contenedor según el tema actual.
        """
        self.container.bgcolor = get_color(self.page.theme_mode, "background")
        self.container.update()
        
