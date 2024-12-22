from flet import  Row, ElevatedButton, ButtonStyle, Container
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from src.UI.components.button.ButtonGroup import ButtonGroup
from src.UI.components.text.Text import Text
from src.UI.components.theming.toggleThemeButton import ToggleThemeButton
from assets.colors import get_color 


class TopMenu(Container, ThemedWidget):
    def __init__(self, page):
                
        ThemedWidget.__init__(self)
        Container.__init__(self)
        self.page = page
        
        # Crear un grupo de botones
        button_group = ButtonGroup()

        #region Top Menu
        
        self.publish_button = ElevatedButton(
            content=Text(page, "Publish", color_key="text"),
            bgcolor=get_color(page.theme_mode, "primary"),
            style=ButtonStyle(padding=15)
        )
        
        self.content = Row([
            Row([
                Button(page, "isotipe_transparent.svg", group=button_group),
                Button(page, "ADD_CIRCLE_ROUNDED", group=button_group),
                Button(page, "LAYERS_ROUNDED", group=button_group),
                Button(page, "ALT_ROUTE_ROUNDED", group=button_group),
                Button(page, "STORAGE_ROUNDED", group=button_group),
                Button(page, "EXTENSION_ROUNDED", group=button_group),
                ],spacing=25
            ),
            Row([
                Text(page, "untitled", color_key="text"),
                Text(page, "bassalt.app.untitled", color_key="default"),
                ],spacing=10
            ),
            Row([
                self.publish_button,
                Button(page, "SHARE_ROUNDED"),
                Button(page, "PLAY_ARROW_ROUNDED"),
                Button(page, "SETTINGS_ROUNDED"),   
                Button(page, "PERSON_ROUNDED"),
                ToggleThemeButton(page),
                ],spacing=25
            ),
        ],
        alignment="center",
        spacing=60,
        )
        
        self.bgcolor = get_color(page.theme_mode, "background")
        self.padding = 20


    def update_theme(self):
        self.bgcolor = get_color(self.page.theme_mode, "background")
        self.publish_button.bgcolor=get_color(self.page.theme_mode, "primary")
        self.publish_button.update()
        self.update()
        


