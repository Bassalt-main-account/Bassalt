COLORS = {
    "dark": {
        "primary": "#3b4187",
        "background": "#101011",
        "background2": "#2B2A2A",
        "hover": "#ffffff",
        "selected": "#ffffff",
        "text": "#ffffff",
        "text2": "#898889",
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
        "text2": "#898889",
        "default": "#898889",
        "icon": "#ffffff",
    }
}


def get_color(theme, color_key):
    return COLORS[theme][color_key]