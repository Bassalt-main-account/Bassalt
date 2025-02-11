from flet import  Row, ElevatedButton, ButtonStyle, Container
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.button.Button import Button
from src.UI.components.button.ButtonGroup import ButtonGroup
from src.UI.components.text.Text import Text
from src.UI.components.theming.toggleThemeButton import ToggleThemeButton
from src.UI.components.SideMenus.add import AddMenu
from src.UI.components.SideMenus.layers import Layers
from assets.colors import get_color 
from src.data.cache import get_theme_mode


class TopMenu(Container, ThemedWidget):
    def __init__(self, page):
                
        ThemedWidget.__init__(self)
        Container.__init__(self)
        self.page = page
        self.current_menu = None

        self.add_in_page = False
        self.add_menu_container = Container(AddMenu(self.page, self.empty_menus),left=20,visible=False, data="ADD")
        self.layers_menu_container = Container(Layers(self.page, self.empty_menus),left=20,visible=False, data="LAYERS")


        # Crear un grupo de botones
        button_group = ButtonGroup()

        #region Top Menu        
        self.publish_button = ElevatedButton(
            content=Text(page, value="Publish", color_key="text"),
            bgcolor=get_color(get_theme_mode(), "primary"),
            style=ButtonStyle(padding=15)
        )
        
        self.content = Row([
            Row([
                Button(page, icon="isotipe_transparent.svg", group=button_group, on_click=self.empty_menus), #TEMPORAL
                Button(page, icon="ADD_CIRCLE_ROUNDED", group=button_group, on_click=self.add_button_on_click),
                Button(page, icon="LAYERS_ROUNDED", group=button_group, on_click=self.layers_button_on_click),
                Button(page, icon="ALT_ROUTE_ROUNDED", group=button_group, on_click=self.empty_menus), #TEMPORAL
                Button(page, icon="STORAGE_ROUNDED", group=button_group, on_click=self.empty_menus), #TEMPORAL
                Button(page, icon="EXTENSION_ROUNDED", group=button_group, on_click=self.empty_menus), #TEMPORAL
                ],spacing=25,
            ),
            Row([
                Row(width=10),
                Text(page, value="untitled", color_key="text"),
                Text(page, value="bassalt.app.untitled", color_key="default"),
                Row(width=10)
                ],spacing=10,
            ),
            Row([
                self.publish_button,
                Button(page, icon="SHARE_ROUNDED"),
                Button(page, icon="PLAY_ARROW_ROUNDED"),
                Button(page, icon="SETTINGS_ROUNDED"),   
                Button(page, icon="PERSON_ROUNDED"),
                ToggleThemeButton(page),
                ],spacing=25,
            ),
        ],
        alignment="spaceBetween",
        spacing=60,
        expand=True,
        expand_loose=True,
        )
        
        self.bgcolor = get_color(get_theme_mode(), "background")
        self.padding = 20
        

    def update_theme(self):
        self.bgcolor = get_color(get_theme_mode(), "background")
        self.publish_button.bgcolor=get_color(get_theme_mode(), "primary")
        self.publish_button.update()
        
        if self.page:
            self.update()


    def add_button_on_click(self, e):        
        if self.current_menu != "ADD": 
            self.current_menu = "ADD"           
            self.select_menu()
            
    def layers_button_on_click(self, e):        
        if self.current_menu != "LAYERS": 
            self.current_menu = "LAYERS"           
            self.select_menu()
            
    def empty_menus(self, e):  
        self.current_menu = None
        e.control.bgcolor = e.control.button_style.get_bgcolor(get_theme_mode()) # Restaurar el color del boton
        e.control.update()
        self.unselect_buttons()
        self.select_menu()
        

    def select_menu(self):  
        selected = self.current_menu
        menus = self.page.controls[0].controls[0].controls[2:]
        for m in menus:
            if m.data == selected:
                m.visible = True
            else:
                m.visible = False
            m.update()

    def unselect_buttons(self):
        buttons = self.content.controls[0].controls
        for b in buttons:
            b.set_selected(False)

    def load_menus(self):           
        self.page.controls[0].controls[0].controls.append(self.add_menu_container)
        self.page.controls[0].controls[0].controls.append(self.layers_menu_container)
        self.page.update()