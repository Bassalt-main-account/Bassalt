class ButtonGroup:
    def __init__(self):
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)
        button.group = self

    def select_button(self, selected_button):
        for button in self.buttons:
            if button is selected_button:
                button.set_selected(True)
            else:
                button.set_selected(False)
