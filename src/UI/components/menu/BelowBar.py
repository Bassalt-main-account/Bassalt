from flet import Container, Row
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from assets.colors import get_color

class BelowBar(Row, ThemedWidget):
    def __init__(self, page, screen):
        ThemedWidget.__init__(self)  
        self.page = page
        self.screen = screen
        self.w = 400

        self.buttons = Row([
            Button(page,"ZOOM_IN", screen.zoom_in),
            Button(page,"ZOOM_OUT", screen.zoom_out),
        ], alignment="center", spacing=10)

        color = get_color(self.page.theme_mode, "background")

        super().__init__(                                                                               
            [Container(content=self.buttons, bgcolor=color, height=60, width=self.w, border_radius=15)],
            alignment="center"
        )

    def update_theme(self):
        """
        Actualiza el color del texto según el tema actual.
        """
        self.controls[0].bgcolor = get_color(self.page.theme_mode, "background")
        self.controls[0].update()

