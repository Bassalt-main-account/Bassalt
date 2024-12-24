from flet import Container, Row
from src.UI.components.theming.ThemedWidget import ThemedWidget
from assets.colors import get_color

class BelowBar(Row, ThemedWidget):
    def __init__(self, page):
        ThemedWidget.__init__(self)  
        self.page = page

        color = get_color(self.page.theme_mode, "background")

        super().__init__(                                                                               
            [Container(width=400, height=60, bgcolor=color, border_radius=15)],
            alignment="center",
        )

    def update_theme(self):
        """
        Actualiza el color del texto según el tema actual.
        """
        self.controls[0].bgcolor = get_color(self.page.theme_mode, "background")
        self.controls[0].update()
