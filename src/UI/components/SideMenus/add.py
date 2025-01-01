from flet import Container, Row, Column
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from src.UI.components.text.Text import Text
from assets.colors import get_color
from src.data.assets import assets

class AddMenu(Container, ThemedWidget):
    def __init__(self, page):
        ThemedWidget.__init__(self)  
        self.page = page

        color = get_color(self.page.theme_mode, "background")   

        # Initialize rows with the ExpansionPanelList structure
        self.rows = Column([
            self.create_expansion_panel(title, items)
            for title, items in assets.items()
        ])

        super().__init__(
            content=self.rows,
            bgcolor=color,
            padding=10,
            border_radius=15,
        )

    def create_expansion_panel(self, title, items):
        """
        Creates a single expansion panel with items.
        """
        if not items:
            items = ["No items available"]

        # Create buttons for each item
        item_buttons = [Row([Container(width=20),Button(self.page,"PAGES"), Text(self.page,item)]) for item in items]

        # Return a container representing the panel
        return Container(
            content=Column([
                Row([Button(self.page,"MENU_ROUNDED"), Text(self.page, title)]),
                Column(item_buttons, visible=False),  # Initially hidden
            ]),
            padding=10,
        )

    def update_theme(self):
        """
        Actualiza el color del texto según el tema actual.
        """
        self.bgcolor = get_color(self.page.theme_mode, "background")
        self.update()
