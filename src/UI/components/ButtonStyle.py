from assets.colors import COLORS as c

class ButtonStyle:
    def __init__(self,color_key, bgcolor_key, hover_key, selected_key):
        
        # LIGHT
        self.color_light = c["light"][color_key]
        self.bgcolor_light = c["light"][bgcolor_key]
        self.hover_light = c["light"][hover_key]
        self.selected_light = c["light"][selected_key]
        
        # DARK
        self.color_dark = c["dark"][color_key]
        self.bgcolor_dark = c["dark"][bgcolor_key]
        self.hover_dark = c["dark"][hover_key]
        self.selected_dark = c["dark"][selected_key]

    def get_color(self,theme):
        if theme == "light":
            return self.color_light
        elif theme == "dark":
            return self.color_dark
     
    def get_bgcolor(self,theme):
        if theme == "light":
            return self.bgcolor_light
        elif theme == "dark":
            return self.bgcolor_dark
        
    def get_hover(self,theme):
        if theme == "light":
            return self.hover_light
        elif theme == "dark":
            return self.hover_dark
        
    def get_selected(self,theme):
        if theme == "light":
            return self.selected_light
        elif theme == "dark":
            return self.selected_dark