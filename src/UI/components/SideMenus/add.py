from flet import Container, Row, Column, ScrollMode, padding
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from src.UI.components.text.Text import Text
from assets.colors import get_color
from src.data.assets import assets, assets_icons

class AddMenu(Container, ThemedWidget):
    def __init__(self, page):
        ThemedWidget.__init__(self,"ADD")
        self.page = page

        color = get_color(self.page.theme_mode, "background")

        # Construimos la columna principal con la lista de paneles.
        self.rows = Column(
            [
                self.create_expansion_panel(title, items)
                for title, items in assets.items()
                if items  # si la lista de ítems no está vacía
            ],
            scroll=ScrollMode.ALWAYS  # Activamos scroll para el contenedor principal
        )
            
        
        super().__init__(
            content=self.rows,
            bgcolor=color,
            padding=padding.symmetric(20, 20),
            border_radius=15,
            height=500,  # Limita la altura del contenedor principal
        )

    def create_expansion_panel(self, title, items):
        """
        Crea un panel desplegable para cada sección (p.ej., "Basics"),
        usando el diccionario `assets_icons` en base al nombre del título
        convertido en minúsculas y añadiendo "_icon.svg".
        """
        # Generamos la clave para buscar en assets_icons, p.ej. "basics_icon.svg"
        icon_key = f"{title.lower()}_icon.svg"

        # Si la clave existe en assets_icons, usamos esa lista de íconos; en caso contrario, usamos "MENU_ROUNDED".
        sub_icons = assets_icons.get(icon_key, ["MENU_ROUNDED"] * len(items))

        # Contenedor de subitems (inicialmente oculto).
        item_container = Column(
            [
                Row([
                    Container(width=20),
                    Button(self.page, sub_icons[i]),  # Ícono proveniente de la lista sub_icons
                    Text(self.page, item),            # Texto del subitem
                    Container(width=20)
                ])
                for i, item in enumerate(items)
            ],
            visible=False
        )

        def toggle_visibility(e):
            """Muestra/oculta el contenedor de subitems al hacer clic en el botón."""
            item_container.visible = not item_container.visible
            item_container.update()

        # Encabezado (botón de toggle + texto de la sección).
        panel_header = Row([
            Button(self.page, icon_key, on_click=toggle_visibility, selectable=True),
            Text(self.page, title)
        ])

        # Retornamos el contenedor con el encabezado y los subitems.
        return Container(
            content=Column([
                panel_header,
                item_container,
            ]),
            padding=padding.symmetric(10, 20)
        )

    def update_theme(self):
        """
        Actualiza el color de fondo (y potencialmente otros estilos) 
        cuando cambia el tema de la página.
        """
        self.bgcolor = get_color(self.page.theme_mode, "background")
        self.update()
