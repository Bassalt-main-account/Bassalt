import flet
from flet import (
    Page,
    Container,
    Column,
    Row,
    Text,
    GestureDetector,
    DragStartEvent,
    DragUpdateEvent,
    DragEndEvent,
    Stack,
    alignment,
    Colors
)

# Importa la lista global "layers" donde almacenarás la info de los widgets creados
from src.data.layers import layers


class ManualDragSystem:
    """
    Implementa un drag & drop manual:
      - Menú a la izquierda con ítems (arrastrables con GestureDetector).
      - "Pantalla" a la derecha, dentro de un Stack (screen_stack) para colocar
        los widgets finales (con posicionamiento absoluto).
      - Un Stack global (top_stack) que cubre toda la ventana, para mostrar el
        "fantasma" en posición absoluta incluso sobre el menú.
      
      Al soltar, añade un nuevo widget a screen_stack y guarda su info en 'layers'.
    """

    def __init__(self, page: Page, menu_items: list[str]):
        self.page = page
        self.menu_items = menu_items
        
        # Donde guardaremos info de los widgets creados
        self.layers = layers
        
        # Estado para arrastre manual
        self.dragging = False
        self.drag_data = None
        self.ghost_container = None
        self.pointer_x = 0.0
        self.pointer_y = 0.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        
        self.screen_left = 200  # ancho del menú
        self.screen_stack = Stack(expand=True)  # Widgets definitivos (pantalla)
        self.top_stack = Stack(expand=True)     # Capa global (menú + pantalla + fantasma)
        
        self._layout = None
        self._build_layout()
    
    def _build_layout(self):
        """
        Crea el layout principal:
         - Menú en un contenedor de 200 px
         - "Pantalla" a la derecha con un Stack (screen_stack)
         - Ambos se ponen en un Row, que es hijo del top_stack
        """
        # 1) Menú a la izquierda
        menu_col = Column()
        menu_col.controls.append(Text("Manual Menu", color=Colors.BLACK, weight="bold"))
        
        for item_name in self.menu_items:
            # Cada ítem: Container + GestureDetector
            menu_item = Container(
                width=120,
                padding=5,
                bgcolor=Colors.AMBER_50,
                content=Text(item_name, color=Colors.BLACK),
            )
            item_gd = GestureDetector(
                content=menu_item,
                drag_interval=1,
                on_pan_start=lambda e, n=item_name: self.on_pan_start(e, n),
                on_pan_update=self.on_pan_update,
                on_pan_end=self.on_pan_end
            )
            menu_col.controls.append(item_gd)

        menu_container = Container(
            width=self.screen_left,  # 200 px
            height=600,
            bgcolor=Colors.AMBER_50,
            content=menu_col
        )
        
        # 2) La "pantalla" a la derecha: un Container con screen_stack dentro
        screen_container = Container(
            width=self.page.window.width - self.screen_left,
            height=600,
            bgcolor=Colors.GREY_200,
            content=self.screen_stack  # <-- Stack para posicionar widgets absolutos
        )
        
        # 3) Un Row con [menú, pantalla]
        row = Row([menu_container, screen_container], expand=True)

        # 4) top_stack: donde iremos poniendo "row" (nivel base) y, encima, el "fantasma"
        self.top_stack.controls.append(row)
        self._layout = self.top_stack

    def build(self):
        """Retorna el control principal a añadir en la page."""
        return self._layout

    # ----------------------------------------------------------------
    #  HANDLERS DE GESTURE DETECTOR (drag manual)
    # ----------------------------------------------------------------
    def on_pan_start(self, e: DragStartEvent, item_name: str):
        self.dragging = True
        self.drag_data = item_name
        
        self.pointer_x = e.global_x
        self.pointer_y = e.global_y
        self.offset_x = e.local_x
        self.offset_y = e.local_y
        
        # Creamos un "fantasma" para feedback visual
        # (Personalízalo como quieras; debe ser hijo de un Stack)
        ghost = Container(
            width=120,
            height=40,
            bgcolor=Colors.BLUE_100,
            border_radius=5,
            alignment=alignment.center,
            left=self.pointer_x - self.offset_x,
            top=self.pointer_y - self.offset_y,
            content=Text(f"Ghost {item_name}", color=Colors.BLACK),
        )

        self.ghost_container = ghost
        self.top_stack.controls.append(ghost)  # Lo ponemos en el stack global
        self.top_stack.update()

    def on_pan_update(self, e: DragUpdateEvent):
        if self.dragging and self.ghost_container:
            # Actualizamos la posición global del puntero
            self.pointer_x += e.delta_x
            self.pointer_y += e.delta_y
            # Movemos el fantasma
            self.ghost_container.left = self.pointer_x - self.offset_x
            self.ghost_container.top = self.pointer_y - self.offset_y
            self.ghost_container.update()

    def on_pan_end(self, e: DragEndEvent):
        if self.dragging and self.ghost_container:
            # Posición donde se soltó
            final_x = self.pointer_x - self.offset_x
            final_y = self.pointer_y - self.offset_y
            
            # Vemos si soltó dentro de la pantalla (x >= 200)
            if final_x >= self.screen_left:
                # Lo añadimos en la screen_stack con coordenadas relativas
                rel_x = final_x - self.screen_left
                rel_y = final_y
                # Crea el widget final con su propio arrastre interno
                item = self.create_final_widget(self.drag_data, rel_x, rel_y)
                self.screen_stack.controls.append(item)
                self.screen_stack.update()

                # Guardar info en layers
                self.layers.append({
                    "name": self.drag_data,
                    "x": rel_x,
                    "y": rel_y
                })
                
                print(self.layers)
            
            # Quitamos el fantasma
            self.top_stack.controls.remove(self.ghost_container)
            self.top_stack.update()
        
        # Reiniciamos estados
        self.dragging = False
        self.drag_data = None
        self.ghost_container = None
    
    # ----------------------------------------------------------------
    #  WIDGET FINAL (movible dentro de la pantalla)
    # ----------------------------------------------------------------
    def create_final_widget(self, label: str, left: float, top: float) -> Container:
        """
        Crea el control definitivo que se mostrará en la pantalla.
        También lo envolvemos en un GestureDetector para moverlo.
        """
        def item_pan_update(e: DragUpdateEvent):
            c.left += e.delta_x
            c.top += e.delta_y
            c.update()

        content = Container(
            width=120,
            height=40,
            bgcolor=Colors.LIGHT_BLUE_100,
            alignment=alignment.center,
            content=Text(f"New {label}", color=Colors.BLACK),
        )
        gd = GestureDetector(
            content=content,
            on_pan_update=item_pan_update
        )
        c = Container(left=left, top=top, content=gd)
        return c


def main(page: Page):
    page.title = "Manual Drag & Drop System"
    page.window.width = 900
    page.window.height = 600

    menu_items = ["Text", "Image", "Frame", "Button", "Table", "Clock"]
    
    drag_system = ManualDragSystem(page, menu_items)
    page.add(drag_system.build())

flet.app(target=main)
