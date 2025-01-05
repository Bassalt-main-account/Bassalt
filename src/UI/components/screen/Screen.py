from flet import (
    Container,
    GestureDetector,
    Offset,
    Scale,
    Alignment,
    DragStartEvent,
    DragUpdateEvent,
)
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.text.Text import Text
from assets.colors import get_color

class Screen(Container, ThemedWidget):
    def __init__(self, page, width=850, height=550):
        ThemedWidget.__init__(self)
        self.page = page
        
        # Transformaciones acumuladas
        self.scale_factor = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

        # Variables para el arrastre preciso
        self._start_global_x = 0.0
        self._start_global_y = 0.0
        self._initial_offset_x = 0.0
        self._initial_offset_y = 0.0

        # Color inicial según el tema
        color = get_color(self.page.theme_mode, "background")

        # Contenedor visual (fondo)
        self.background_container = Container(
            content=Text(page,"Screen Example"),
            bgcolor=color,
            width=width,
            height=height,
            padding=20
        )

        # GestureDetector que envuelve el contenedor:
        self.screen_gesture = GestureDetector(
            content=self.background_container,
            on_pan_start=self.pan_start,
            on_pan_update=self.pan_update,
            on_double_tap=self.zoom_in,
            on_secondary_tap=self.zoom_out,
        )

        # Hacemos que Screen (self) sea un Container con el GestureDetector
        super().__init__(
            width=width,
            height=height,
            content=self.screen_gesture,
            alignment=Alignment(0, 0),
        )

    # --- EVENTOS DE GESTO ---

    def pan_start(self, e: DragStartEvent):
        """
        Al iniciar el arrastre, guardamos la posición global
        del puntero y el offset actual del contenedor.
        """
        self._start_global_x = e.global_x
        self._start_global_y = e.global_y

        self._initial_offset_x = self.offset_x
        self._initial_offset_y = self.offset_y

    def pan_update(self, e: DragUpdateEvent):
        """
        Mientras se arrastra, calculamos la nueva posición:
        Δx = (puntero global actual) - (puntero global inicial).
        Luego se ajusta el offset con ese Δ.
        """
        dx = e.global_x - self._start_global_x
        dy = e.global_y - self._start_global_y

        # Escalamos el movimiento en función del tamaño de la ventana
        # (opcional, dependiendo de cómo quieras que se mueva)
        self.offset_x = self._initial_offset_x + dx / self.page.width
        self.offset_y = self._initial_offset_y + dy / self.page.height

        self.update_screen()

    # --- ZOOM ---

    def zoom_in(self, e):
        self.scale_factor += 0.1
        self.update_screen()

    def zoom_out(self, e):
        self.scale_factor = max(0.1, self.scale_factor - 0.1)
        self.update_screen()

    # --- REFRESCO ---

    def update_screen(self):
        """Aplica el offset y la escala al contenedor completo (self)."""
        self.offset = Offset(self.offset_x, self.offset_y)
        self.scale = Scale(self.scale_factor)
        self.update()

    def update_theme(self):
        """Actualiza el color del contenedor con el tema actual."""
        self.background_container.bgcolor = get_color(
            self.page.theme_mode, "background"
        )
        self.background_container.update()

    def get_widget(self):
        """Devuelve este contenedor para agregarlo a la página."""
        return self
