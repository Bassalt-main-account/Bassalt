from flet import Container, Row, Text, alignment
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from assets.colors import COLORS

class SliderMenu(Container, ThemedWidget):
    def __init__(self, page, values, on_change=None):
        ThemedWidget.__init__(self)
        Container.__init__(self)

        self.page = page
        self.values = values
        self.on_change = on_change
        self.selected = values[0]

        # Filas para organizar los botones
        self.buttons = []
        for value in values:
            button = self._create_button(value)
            self.buttons.append(button)

        # Configuración del contenedor principal
        self.content = Row(
            controls=self.buttons,
            alignment="center",
            spacing=5,
        )
        self.alignment = alignment.center
        self.bgcolor = COLORS[self.page.theme_mode]["background"]
        self.border_radius = 20

    def _create_button(self, value):
        """Crea un botón con el texto y estilos adecuados."""
        return Container(
            content=Text(
                value=value,
                size=16,
                color=COLORS[self.page.theme_mode]["text"],
                weight="bold",
            ),
            width=100,
            height=40,
            alignment=alignment.center,
            bgcolor=self._get_bgcolor(value),
            border_radius=20,
            on_click=lambda e, v=value: self._on_button_click(v),
        )

    def _get_bgcolor(self, value):
        """Obtiene el color de fondo del botón según el estado."""
        if value == self.selected:
            return COLORS[self.page.theme_mode]["hover"]
        return COLORS[self.page.theme_mode]["default"]

    def _on_button_click(self, value):
        """Maneja el clic en un botón."""
        self.selected = value
        self._update_buttons()
        if self.on_change:
            self.on_change(value)

    def _update_buttons(self):
        """Actualiza el estado de los botones para reflejar la selección."""
        for button, value in zip(self.buttons, self.values):
            button.bgcolor = self._get_bgcolor(value)
            button.content.color = (
                COLORS[self.page.theme_mode]["background"]
                if value == self.selected
                else COLORS[self.page.theme_mode]["text"]
            )
        self.update()

    def update_theme(self):
        """Actualiza los colores del tema para todos los botones."""
        self.bgcolor = COLORS[self.page.theme_mode]["background"]
        for button in self.buttons:
            button.bgcolor = self._get_bgcolor(button.content.value)
            button.content.color = (
                COLORS[self.page.theme_mode]["background"]
                if button.content.value == self.selected
                else COLORS[self.page.theme_mode]["text"]
            )
        self.update()
