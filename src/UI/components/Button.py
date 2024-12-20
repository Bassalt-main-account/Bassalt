from flet import Container, Image, Icon
from .ThemedWidget import ThemedWidget
from assets.colors import COLORS as c

class Button(Container, ThemedWidget):
    def __init__(self, icon, page, on_click = None, group=None, size=40):
                
        ThemedWidget.__init__(self)
        Container.__init__(self)
        
        self.page = page
        self.icon = icon
        self.size = size
        self.default_color = self._get_color("default")
        self.bgcolor = self.default_color
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
        color = self._get_color("icon")
        if icon.endswith(".svg"):
            return Image(src=f"assets/{icon}", width=self.size * 0.8, height=self.size * 0.8, color=color)
        return Icon(name=icon, size=self.size * 0.8, color=color)

    def _on_hover(self, e):
        if not self.is_selected:
            hover_color = self._get_color("hover")
            self.bgcolor = hover_color if e.data == "true" else self.default_color
            self.update()

    def update_theme(self):
        self.default_color = self._get_color("default")
        self.bgcolor = self.default_color if not self.is_selected else self._get_color("selected")
        self.content.color = self._get_color("icon")
        self.update()
        
    def set_selected(self, selected):
        if self.group:
            self.is_selected = selected
            self.bgcolor = self._get_color("selected") if selected else self.default_color
        else:
            self.bgcolor = self._get_color("hover")
        self.update()
    
    def handle_click(self, e):
        if self.group:
            self.group.select_button(self)
            self.set_selected(True)
        
        if callable(self.original_on_click):
            self.original_on_click(e)
