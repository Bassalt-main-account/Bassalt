from flet import Container, Row, Column, ScrollMode, padding, Stack
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from src.UI.components.menu.SliderMenu import SliderMenu
from assets.colors import get_color

class Layers(Container, ThemedWidget):
    def __init__(self, page, close_menu):
        ThemedWidget.__init__(self)
        self.page = page

        def prueba(e):
            print(slider.get_selected())
            
        color = get_color(self.page.theme_mode, "background")
        slider = SliderMenu(page, ["Pages", "Layers", "Styles"],on_update=prueba)
        
        content = Container(
            content= slider,
            padding=padding.symmetric(30, 30),
        )
        
        super().__init__(
            content=Stack([content, Button(self.page, "CLOSE_ROUNDED",size=20, right=0, top=0, on_click=close_menu)]),
            bgcolor=color,
            padding=padding.symmetric(20, 20),
            border_radius=15,
            height=700,  # Limita la altura del contenedor principal
        )
        
        


    def update_theme(self):
        """
        Actualiza el color de fondo (y potencialmente otros estilos) 
        cuando cambia el tema de la página.
        """
        self.bgcolor = get_color(self.page.theme_mode, "background")
        
        self.update()
