COLORS = {
    "dark": {
        "primary": "#3b4187",
        "background": "#101011",
        "background2": "#1E1E1E",
        "hover": "#ffffff",
        "selected": "#ffffff",
        "text": "#ffffff",
        "default": "#898889",
        "icon": "#101011",
    },
    "light": {
        "primary": "#7d87db",
        "background": "#ffffff",
        "background2": "#e4e4e4",
        "hover": "#101011",
        "selected": "#101011",
        "text": "#101011",
        "default": "#898889",
        "icon": "#ffffff",
    }
}


def get_color(theme, color_key):
    return COLORS[theme][color_key]