
# Clase base para widgets temáticos
class ThemedWidget:
    # Lista global de widgets que deben actualizarse
    _observers = []
    _observers_id = []

    def __init__(self,):
        # Registramos el widget actual en la lista global
        super().__init__()  # Llamada a super para soporte de herencia múltiple
        ThemedWidget._observers.append(self) 

    def update_theme(self):
        """Método abstracto para actualizar el tema. Debe implementarse en clases hijas."""
        pass

    @classmethod
    def update_all(cls):
        """Actualiza el tema de todos los widgets observadores."""
        for widget in cls._observers:
            widget.update_theme()
