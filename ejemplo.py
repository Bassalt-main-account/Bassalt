import flet
from flet import (
    Page,
    Column,
    Row,
    Container,
    Text,
    Draggable,
    DragTarget,
    DragTargetAcceptEvent,
    GestureDetector,
    DragStartEvent,
    DragUpdateEvent,
    Stack,
    alignment,
    # En lugar de colors, usamos Colors para evitar deprecation
    Colors
)

# --------------------------------------------------------------------
# 1) DRAGGABLE DE MENÚ
#    Sin on_drop, sin on_drag_update: solo group="add_menu" y data=...
# --------------------------------------------------------------------
def build_menu_item(item_name: str) -> Draggable:
    """
    Retorna un Draggable clásico (sin callbacks inexistentes),
    con un texto y color de fondo. Esto se arrastra desde el menú.
    """
    drag_container = Container(
        content=Text(item_name, color=Colors.BLACK),
        bgcolor=Colors.BLUE_100,
        padding=10,
        border_radius=5,
        width=120
    )
    return Draggable(
        group="add_menu",  # El DragTarget lo aceptará
        data=item_name,    # Lo que "transportamos"
        content=drag_container
    )

# --------------------------------------------------------------------
# 2) MENÚ LATERAL
# --------------------------------------------------------------------
def build_add_menu() -> Container:
    assets = {
        "Basics": ["Text", "Image", "Frame"],
        "Widgets": ["Button", "Table", "Clock"],
    }

    # Por compatibilidad, evitamos colors.* y UserControl
    menu_column = Column([
        Text("Add Menu", color=Colors.BLACK, size=16, weight="bold"),
    ])

    for title, items in assets.items():
        menu_column.controls.append(
            Text(title, color=Colors.BLACK, size=14, weight="bold")
        )
        subitems_col = Column([
            build_menu_item(it) for it in items
        ])
        menu_column.controls.append(subitems_col)

    return Container(
        width=200,
        bgcolor=Colors.AMBER_50,
        content=menu_column,
        padding=10
    )

# --------------------------------------------------------------------
# 3) ITEM MOVIBLE EN PANTALLA (sin UserControl)
#    Se implementa como una función que retorna un Container
#    con GestureDetector y left, top en un Stack.
# --------------------------------------------------------------------
def build_movable_item(text: str, left: float, top: float) -> Container:
    """
    Retorna un Container posicionado (left, top) en un Stack,
    arrastrable con GestureDetector (on_pan_update).
    """
    # Guardamos variables en un dict, pues no usamos UserControl:
    state = {
        "left": left,
        "top": top
    }

    # Contenido visual
    content = Container(
        width=120,
        height=40,
        bgcolor=Colors.LIGHT_BLUE_100,
        alignment=alignment.center,
        content=Text(text, color=Colors.BLACK),
    )

    # Al arrastrar (on_pan_*), actualizamos la posición en el Stack
    def pan_update(e: DragUpdateEvent):
        # Sumamos el delta al "left"/"top" del contenedor
        c.left += e.delta_x
        c.top += e.delta_y
        c.update()

    gesture = GestureDetector(
        on_pan_start=lambda e: None,  # No haremos nada en pan_start
        on_pan_update=pan_update,
        content=content,
    )

    # El contenedor en el Stack (posición absoluta)
    c = Container(
        left=state["left"],
        top=state["top"],
        content=gesture
    )
    return c

# --------------------------------------------------------------------
# 4) PANTALLA (DragTarget: on_accept -> crea un item en (10,10))
# --------------------------------------------------------------------
def build_screen() -> Container:
    stack = Stack(expand=True)

    def on_accept_drop(e: DragTargetAcceptEvent):
        # No tenemos e.x, e.y ni callbacks en Draggable, así que...
        # Creamos el nuevo ítem siempre en la misma posición:
        item_name = e.control.data  # "Text", "Image", etc.
        movable = build_movable_item(f"New {item_name}", left=10, top=10)
        stack.controls.append(movable)
        stack.update()

    drop_target = DragTarget(
        group="add_menu",
        content=stack,
        on_accept=on_accept_drop
    )

    return Container(
        width=600,
        height=400,
        bgcolor=Colors.GREY_200,
        content=drop_target
    )

# --------------------------------------------------------------------
# 5) MAIN
# --------------------------------------------------------------------
def main(page: Page):
    page.title = "Flet - Legacy Drag & Drop"
    page.window.width = 900  # Evitamos window_width
    page.window.height = 600 # Evitamos window_height

    add_menu = build_add_menu()
    screen = build_screen()

    layout = Row([add_menu, screen], expand=True)
    page.add(layout)

flet.app(target=main)
