from flet import Container, GestureDetector, Stack, Offset, Scale, Row
from src.UI.components.theming.ThemedWidget import ThemedWidget
from assets.colors import get_color

class Screen(Row, ThemedWidget):
    def __init__(self, page, width=700, height=400):
        ThemedWidget.__init__(self)
        self.page = page
        self.scale_factor = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

        # Configurar color inicial basado en el tema
        color = get_color(self.page.theme_mode, "background")

        # Contenedor principal del screen
        self.container = Container(
            bgcolor=color,
            width=width,
            height=height,
        )

        # Detector de gestos para mover y escalar
        self.screen_gesture = GestureDetector(
            content=Stack([self.container]),
            on_pan_update=self.move_screen,  # Permite mover el screen
            on_double_tap=self.zoom_in,     # Zoom in con doble clic
            on_secondary_tap=self.zoom_out, # Zoom out con clic derecho
        )

        super().__init__(
            controls=[self.screen_gesture],
            alignment="center",
            expand=True
        )

    def zoom_in(self, e):
        self.scale_factor += 0.1
        self.update_screen()

    def zoom_out(self, e):
        self.scale_factor = max(0.1, self.scale_factor - 0.1)  # No permitir zoom menor que 0.1
        self.update_screen()

    def move_screen(self, e):
        self.offset_x += e.delta_x / self.page.width  # Normalizamos por el ancho de la página
        self.offset_y += e.delta_y / self.page.height  # Normalizamos por el alto de la página
        self.update_screen()

    def update_screen(self):
        """Actualiza la escala, posición y tema del screen."""
        self.container.offset = Offset(self.offset_x, self.offset_y)
        self.container.scale = Scale(self.scale_factor)
        self.container.update()

    def update_theme(self):
        """
        Actualiza el color del contenedor según el tema actual.
        """
        self.container.bgcolor = get_color(self.page.theme_mode, "background")
        self.container.update()

    def get_widget(self):
        """Devuelve el widget del screen con gestos incluidos."""
        return self.screen_gesture
