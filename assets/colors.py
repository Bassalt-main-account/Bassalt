COLORS = {
    "dark": {
        "primary": "#3b4187",
        "background": "#101011",
        "hover": "#ffffff",
        "selected": "#ffffff",
        "text": "#ffffff",
        "default": "#898889",
        "icon": "#101011",
    },
    "light": {
        "primary": "#5D64AC",
        "background": "#ffffff",
        "hover": "#101011",
        "selected": "#101011",
        "text": "#101011",
        "default": "#898889",
        "icon": "#ffffff",
    }
}


def get_color(theme, color_key):
    return COLORS[theme][color_key]