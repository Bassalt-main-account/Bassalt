# Clase base para widgets responsivos
class ResponsiveWidget:
    # Lista global de widgets responsivos
    _observers = []

    def __init__(self, default_width=1000):
        """
        Inicializa el ResponsiveWidget.

        Args:
            default_width (int): Ancho base para el cálculo del ratio.
        """
        # Registramos el widget actual en la lista global
        ResponsiveWidget._observers.append(self)
        self.default_width = default_width  # Ancho base para el diseño
        self.ratio = 1.0  # Ratio inicial

    def update_layout(self, page):
        """
        Método abstracto para actualizar el layout. Debe implementarse en clases hijas.
        Calcula el ratio basado en el ancho actual de la página.

        Args:
            page (flet.Page): Referencia a la página para obtener el ancho actual.
        """
        # Calcular el ratio basado en el ancho actual de la página
        new_ratio = page.width / self.default_width
        # Limitar el ratio para evitar tamaños extremos
        new_ratio = max(0.5, min(new_ratio, 2.0))
        self.ratio = new_ratio
        self._apply_ratio()
        self.update()

    def _apply_ratio(self):
        """
        Método abstracto para aplicar el ratio a las propiedades del widget.
        Debe implementarse en clases hijas.
        """
        pass

    @classmethod
    def update_all_layouts(cls, page):
        """
        Actualiza el layout de todos los widgets responsivos.

        Args:
            page (flet.Page): Referencia a la página para obtener el ancho actual.
        """
        for widget in cls._observers:
            widget.update_layout(page)
