from assets.colors import COLORS as c

class TextStyle:
    def __init__(self,color_key, selected_key):
        self.color_light = c["light"][color_key]
        self.color_dark = c["dark"][color_key]
        self.selected_light = c["light"][selected_key]
        self.selected_dark = c["dark"][selected_key]
        
    def get_color(self,theme):
        if theme == "light":
            return self.color_light
        elif theme == "dark":
            return self.color_dark
     
    def get_selected(self,theme):
        if theme == "light":
            return self.selected_light
        elif theme == "dark":
            return self.selected_dark
     