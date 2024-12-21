from assets.colors import COLORS as c

class TextStyle:
    def __init__(self,color_key):
        self.light = c["light"][color_key]
        self.dark = c["dark"][color_key]

    def get_color(self,theme):
        if theme == "light":
            return self.light
        elif theme == "dark":
            return self.dark
     