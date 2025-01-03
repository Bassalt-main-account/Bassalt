from flet import Container, Image, Icon, ImageFit
from src.UI.components.theming.ThemedWidget import ThemedWidget
from .ButtonStyle import ButtonStyle
from assets.colors import COLORS as c

class Button(Container, ThemedWidget):
    def __init__(self, page, icon, on_click = None, group=None, color_key="icon",  bgcolor_key="default", hover_key = "hover", selected_key="selected",  size=30):
                
        ThemedWidget.__init__(self)
        Container.__init__(self)
        
        self.page = page
        self.icon = icon
        self.size = size
        
        #Colors
        self.button_style = ButtonStyle(color_key, bgcolor_key, hover_key, selected_key)
        self.color = self.button_style.get_color(self.page.theme_mode)
        self.bgcolor = self.button_style.get_bgcolor(self.page.theme_mode)
        self.default_color = self.bgcolor
        self.hover_color = self.button_style.get_hover(self.page.theme_mode)
        self.selected_color = self.button_style.get_selected(self.page.theme_mode)
        
        self.border_radius = self.size * 0.25
        self.width = size 
        self.height = size
        self.content = self._create_content(icon)
        self.original_on_click = on_click
        self.on_click = self.handle_click
        self.on_hover = self._on_hover
        self.is_selected = False
        self.group = group
        if group:
            group.add_button(self)
        
        
    def _get_color(self, color_key):
        theme = self.page.theme_mode 
        return c[theme][color_key]

    def _create_content(self, icon):
        if icon.endswith(".svg"):
            return Image(src="icons/"+icon, width=self.size * 0.8, height=self.size * 0.8, color=self.color, fit=ImageFit.FIT_WIDTH)
        return Icon(name=icon, size=self.size * 0.8, color=self.color)

    def _on_hover(self, e):
        if not self.is_selected:
            self.bgcolor = self.hover_color if e.data == "true" else self.default_color
            self.update()

    def update_theme(self):
        self.default_color = self.button_style.get_bgcolor(self.page.theme_mode)
        self.selected_color = self.button_style.get_selected(self.page.theme_mode)
        self.hover_color = self.button_style.get_hover(self.page.theme_mode)
        self.bgcolor = self.selected_color if self.is_selected else self.default_color
        self.content.color = self.button_style.get_color(self.page.theme_mode)
        self.update()
        
    def set_selected(self, selected):
        if self.group:
            self.is_selected = selected
            self.bgcolor = self.button_style.get_selected(self.page.theme_mode) if selected else self.default_color
        else:
            self.bgcolor = self.button_style.get_hover(self.page.theme_mode)
        self.update()
    
    def handle_click(self, e):
        if self.group:
            self.group.select_button(self)
            self.set_selected(True)
        
        if callable(self.original_on_click):
            self.original_on_click(e)
