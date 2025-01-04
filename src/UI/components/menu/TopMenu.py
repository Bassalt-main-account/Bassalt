from flet import  Row, ElevatedButton, ButtonStyle, Container
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from src.UI.components.button.ButtonGroup import ButtonGroup
from src.UI.components.text.Text import Text
from src.UI.components.theming.toggleThemeButton import ToggleThemeButton
from src.UI.components.SideMenus.add import AddMenu
from assets.colors import get_color 


class TopMenu(Container, ThemedWidget):
    def __init__(self, page):
                
        ThemedWidget.__init__(self)
        Container.__init__(self)
        self.page = page
        self.current_menu = None
        
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
                Button(page, "isotipe_transparent.svg", group=button_group, on_click=self.empty_menus),
                Button(page, "ADD_CIRCLE_ROUNDED", group=button_group, on_click=self.add_button_on_click),
                Button(page, "LAYERS_ROUNDED", group=button_group, on_click=self.empty_menus),
                Button(page, "ALT_ROUTE_ROUNDED", group=button_group, on_click=self.empty_menus),
                Button(page, "STORAGE_ROUNDED", group=button_group, on_click=self.empty_menus),
                Button(page, "EXTENSION_ROUNDED", group=button_group, on_click=self.empty_menus),
                ],spacing=25,
            ),
            Row([
                Row(width=10),
                Text(page, "untitled", color_key="text"),
                Text(page, "bassalt.app.untitled", color_key="default"),
                Row(width=10)
                ],spacing=10,
            ),
            Row([
                self.publish_button,
                Button(page, "SHARE_ROUNDED"),
                Button(page, "PLAY_ARROW_ROUNDED"),
                Button(page, "SETTINGS_ROUNDED"),   
                Button(page, "PERSON_ROUNDED"),
                ToggleThemeButton(page),
                ],spacing=25,
            ),
        ],
        alignment="spaceBetween",
        spacing=60,
        expand=True,
        expand_loose=True,
        )
        
        self.bgcolor = get_color(page.theme_mode, "background")
        self.padding = 20
        


    def update_theme(self):
        self.bgcolor = get_color(self.page.theme_mode, "background")
        self.publish_button.bgcolor=get_color(self.page.theme_mode, "primary")
        self.publish_button.update()
        self.update()

    def add_button_on_click(self, e):
        if self.current_menu != "ADD":
            self.empty_menus(e)
            add_menu_container = Container(AddMenu(self.page),left=20)
            self.page.controls[0].controls[0].controls.append(add_menu_container)
            self.page.update()
            self.current_menu = "ADD"

    def empty_menus(self, e):
        try:
            self.current_menu = None
            # Intenta eliminar el control de la página
            self.page.controls[0].controls[0].controls.pop(2)
            self.page.update()
        except Exception:
            pass

    
        if "ADD" in self._observers_id:
            index = self._observers_id.index("ADD")  # Encuentra el índice del ID
            self._observers_id.pop(index)  # Elimina el ID de observers_id
            self._observers.pop(index)  # Elimina el observer correspondiente

        print(self._observers_id)
        print(self._observers)