import flet as ft

def main(page: ft.Page):
    # Inicializamos escala y posición del screen
    scale_factor = 1.0
    offset_x = 0.0
    offset_y = 0.0

    def zoom_in(e):
        nonlocal scale_factor
        scale_factor += 0.1
        update_screen()

    def zoom_out(e):
        nonlocal scale_factor
        scale_factor = max(0.1, scale_factor - 0.1)  # No permitir zoom menor que 0.1
        update_screen()

    def move_screen(e):
        nonlocal offset_x, offset_y
        offset_x += e.delta_x / page.width  # Normalizamos por el ancho de la página
        offset_y += e.delta_y / page.height  # Normalizamos por el alto de la página
        update_screen()

    def update_screen():
        """Actualiza la escala y posición del screen."""
        screen.offset = ft.Offset(offset_x, offset_y)
        screen.scale = ft.Scale(scale_factor)
        page.update()

    # Contenedor del Screen
    screen = ft.Container(
        content=ft.Text("This is the screen content"),
        bgcolor="lightblue",
        width=800,
        height=600,
        alignment=ft.alignment.center,
    )

    # Contenedor principal con gestos para mover y escalar
    screen_gesture = ft.GestureDetector(
        content=ft.Stack([screen]),
        on_pan_update=move_screen,  # Permite mover el screen
        on_double_tap=zoom_in,     # Zoom in con doble clic
        on_secondary_tap=zoom_out, # Zoom out con clic derecho
    )

    # Toolbar fijo abajo
    toolbar = ft.Row(
        controls=[
            ft.ElevatedButton("Zoom In", on_click=zoom_in),
            ft.ElevatedButton("Zoom Out", on_click=zoom_out),
        ],
        alignment="center",
        height=50,
    )

    # Layout principal
    page.add(
        ft.Column(
            controls=[
                ft.Container(screen_gesture, expand=True),  # Screen reescalable
                toolbar,  # Toolbar inmóvil
            ],
            alignment="spaceBetween",
        )
    )

ft.app(target=main)
