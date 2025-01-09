from flet import Container, Image
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.text.Text import Text
from src.UI.components.icon.Icon import Icon
from src.data.cache import get_theme_mode
from .ButtonStyle import ButtonStyle

class Button(Container, ThemedWidget):
    def __init__(self, page, icon=None, text=None, on_click=None, group=None, selectable=False, color_key="icon", bgcolor_key="default", hover_key="hover", selected_key="selected", size=30, right=None, left=None, top=None, bottom=None):

        ThemedWidget.__init__(self)
        Container.__init__(self)
        
        self.page = page
        self.icon = icon
        self.text = text 
        self.size = size
        self.selectable = selectable

        # Colors
        self.button_style = ButtonStyle(color_key, bgcolor_key, hover_key, selected_key)
        self.color_key = color_key
        self.color = self.button_style.get_color(get_theme_mode())
        self.bgcolor = self.button_style.get_bgcolor(get_theme_mode())
        self.default_color = self.bgcolor
        self.hover_color = self.button_style.get_hover(get_theme_mode())
        self.selected_color = self.button_style.get_selected(get_theme_mode())
        
        self.border_radius = self.size * 0.25
        self.width = size
        self.height = size
        self.content = self._create_content(icon, text)
        self.original_on_click = on_click
        self.on_click = self.handle_click
        self.on_hover = self._on_hover
        self.is_selected = False
        self.group = group
        if group:
            group.add_button(self)
            
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right


    def _create_content(self, icon, text):
        if text:  # Si se proporciona texto, creamos un widget de texto
            print("Baliza", text)
            return Text(self.page, value=text, color_key=self.color_key,size=self.size)
        elif icon:  # Si se proporciona un icono, seguimos la lógica existente
            return Icon(self.page, icon=icon, color_key=self.color_key, size=self.size)
        
    def _on_hover(self, e):
        if not self.is_selected:
            self.bgcolor = self.hover_color if e.data == "true" else self.default_color
            self.update()

    def update_theme(self):
        self.default_color = self.button_style.get_bgcolor(get_theme_mode())
        self.selected_color = self.button_style.get_selected(get_theme_mode())
        self.hover_color = self.button_style.get_hover(get_theme_mode())
        self.bgcolor = self.selected_color if self.is_selected else self.default_color
        self.content.color = self.button_style.get_color(get_theme_mode())
        if self.page:
            self.update()
        
    def set_selected(self, selected):
        # Set group selected button
        if self.group:
            self.is_selected = selected
            self.bgcolor = self.button_style.get_selected(get_theme_mode()) if selected else self.default_color
        else:
            self.bgcolor = self.button_style.get_hover(get_theme_mode())
        self.update()
    
    def handle_click(self, e):
        if self.group:
            self.group.select_button(self)
            self.set_selected(True)
        elif self.selectable:
            self.is_selected = not self.is_selected
            self.bgcolor = self.selected_color if self.is_selected else self.default_color
            self.update()
        
        if callable(self.original_on_click):
            self.original_on_click(e)
