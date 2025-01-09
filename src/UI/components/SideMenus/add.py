from flet import Container, Row, Column, ScrollMode, padding, Stack
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from src.UI.components.text.Text import Text
from assets.colors import get_color
from src.data.assets import assets, assets_icons

class AddMenu(Container, ThemedWidget):
    def __init__(self, page, close_menu):
        ThemedWidget.__init__(self)
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
        
        content = Container(
            content=self.rows,
            padding=padding.symmetric(30, 30),
        )   
        
        super().__init__(
            content=Stack([content, Button(self.page, "CLOSE_ROUNDED",size=20, right=0, top=0, on_click=close_menu)]),
            bgcolor=color,
            padding=padding.symmetric(20, 20),
            border_radius=15,
            height=600,  # Limita la altura del contenedor principal
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
                    Button(self.page, icon=sub_icons[i]),  # Ícono proveniente de la lista sub_icons
                    Text(self.page, item, color_key="text2",size=16),            # Texto del subitem
                    Container(width=20)
                ])
                for i, item in enumerate(items)
            ],
            visible=False
        )

        def toggle_visibility():
            """Muestra/oculta el contenedor de subitems al hacer clic en el botón."""
            item_container.visible = not item_container.visible
            item_container.update()

        # Encabezado (botón de toggle + texto de la sección).
        text = Text(self.page, title, size=18, color_key="text2")
        
        def click(e):
            toggle_visibility()
            text.toggle_selected()
        
        panel_header = Row([
            Button(self.page, icon_key, on_click=click, selectable=True, size=40),  # Ícono de la sección
            text,  # Texto de la sección
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
