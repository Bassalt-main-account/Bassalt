from flet import Container, Row, Column, padding, Stack
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from src.UI.components.text.Text import Text
from src.UI.components.icon.Icon import Icon
from src.UI.components.menu.SliderMenu import SliderMenu
from assets.colors import get_color
from src.data.cache import get_theme_mode

class Layers(Container, ThemedWidget):
    def __init__(self, page, close_menu):
        ThemedWidget.__init__(self)
        self.page = page

        def prueba(e):
            selected = slider.get_selected()

            if selected == "Pages":
                self.screen.content.controls[1] = pages_container
            elif selected == "Layers":
                self.screen.content.controls[1] = layers_container
            elif selected == "Styles": 
                self.screen.content.controls[1] = styles_container
            
            self.screen.update()


        slider = SliderMenu(page, ["Pages", "Layers", "Styles"],on_update=prueba)

        pages_container = Column([
            Text(page, "Pages", size=18),
            Row([
                Icon(page, "HOME_ROUNDED", size=30),
                Text(page, "Home", size=18, color_key="default"),
            ])
        ],spacing=15)
        
        
        layers_container = Column([Text(page, "Layers", size=18)])
        styles_container = Column([Text(page, "Styles", size=18)])
        
        self.screen = Container(
            content= Column([
                slider,
                pages_container
            ],spacing=30),
            padding=padding.symmetric(30, 30),
        )
        
        super().__init__(
            content=Stack([self.screen, Button(self.page, "CLOSE_ROUNDED",size=20, right=0, top=0, on_click=close_menu)]),
            bgcolor=get_color(get_theme_mode(), "background"),
            padding=padding.symmetric(20, 20),
            border_radius=15,
            height=600,  # Limita la altura del contenedor principal
        )
        
        


    def update_theme(self):
        """
        Actualiza el color de fondo (y potencialmente otros estilos) 
        cuando cambia el tema de la página.
        """
        self.bgcolor = get_color(get_theme_mode(), "background")
        if self.page:
            self.update()
