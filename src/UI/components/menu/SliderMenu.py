
from flet import Container, Row, Stack, alignment, animation
from src.UI.components.theming.ThemedWidget import ThemedWidget
from src.UI.components.text.Text import Text
from assets.colors import get_color

class SliderMenu(Container, ThemedWidget):
    def __init__(
        self,
        page,
        values,
        size=16,
        text_key="text",
        bgcolor_key="background2",
        selected_key="default",
        on_update = None
    ):
        ThemedWidget.__init__(self)
        Container.__init__(self)

        self.page = page
        self.values = values
        self.selected = values[0]
        self.size = size
        
        self.original_on_update = on_update

        self.text_key = text_key
        self.bgcolor_key = bgcolor_key
        self.selected_key = selected_key

        # Precompute button width. By default, each button uses _get_max_width() * 12.
        self._max_width = self._get_max_width() * 12
        
        # Build the buttons.
        self.buttons = []
        for value in values:
            btn = self._create_button(value)
            self.buttons.append(btn)

        # We no longer use a simple Row as self.content. Instead, we wrap a Row in a Stack.
        # 1) The highlight_pill is a single Container that slides behind the selected button.
        # 2) The row (with the button containers) sits on top of that highlight container.
        self.highlight_pill = Container(
            # Make it the same size as a button (or slightly bigger if desired).
            width=self._max_width,
            height=self.size * 2,
            bgcolor=get_color(self.page.theme_mode, self.selected_key),
            border_radius=self.size,
            left=0,       # Will animate from one button to another
            top=0,
            animate_position=animation.Animation(duration=300, curve="easeInOut"),
        )

        # The row with our actual button controls
        self.row = Row(
            controls=self.buttons,
            spacing=self.size / 3,
            alignment="center",
        )

        # The stack that holds the highlight pill behind the row of buttons
        self.stack = Stack(
            controls=[self.highlight_pill, self.row],
            # We need enough width to hold all buttons + spacing.
            # For example: total width = (#buttons * _max_width) + (#buttons - 1)*spacing
            width=len(values)*self._max_width + (len(values)-1)*(self.size/3),
            height=self.size * 2,
        )
        
        # Finally, set self.content to the Stack so it renders in the UI.
        self.content = self.stack

        # Container (itself) styling
        self.bgcolor = get_color(self.page.theme_mode, bgcolor_key)
        self.border_radius = self.size * 1.2
        self.padding = self.size / 3

        # Position the highlight pill on the first (default-selected) button.
        self._update_highlight_pill(self.selected)


    def _create_button(self, value):
        """Create one button for each item in `values`."""
        return Container(
            content=Text(
                self.page,
                value=value,
                size=self.size,
                color_key=self.text_key
            ),
            alignment=alignment.center,
            width=self._max_width,
            height=self.size * 2,
            border_radius=self.size,
            on_click=lambda e, v=value: self._on_button_click(v),
        )

    def _get_max_width(self):
        """Returns the length of the longest text in `values` (for uniform button width)."""
        return max(len(value) for value in self.values)


    def _update_highlight_pill(self, value):
        """Repositions the highlight pill underneath the given `value` button."""
        index = self.values.index(value)
        # Each button has width = self._max_width. Spacing is self.size/3 for each gap to the left.
        new_left = index * (self._max_width + self.size/3)
        self.highlight_pill.left = new_left
        self.highlight_pill.width = self._max_width 
        self.highlight_pill.bgcolor = get_color(self.page.theme_mode, self.selected_key)
        # Trigger an update so the position animates.
        try:
            self.highlight_pill.update()
        except Exception as e:
            print(e)

    def _on_button_click(self, value):
        """Handle what happens when a user clicks a button."""
        self.selected = value
        self._update_highlight_pill(value)
        self.handle_update(self)


    def update_theme(self):
        """Called if the theme changes; re-apply the correct colors."""
        self.bgcolor = get_color(self.page.theme_mode, self.bgcolor_key)
        for button in self.buttons:
            button.content.color = (
                get_color(self.page.theme_mode, self.bgcolor_key)
                if button.content.value == self.selected
                else get_color(self.page.theme_mode, self.text_key)
            )
        # Also update the highlight pill color:
        self.highlight_pill.bgcolor = get_color(self.page.theme_mode, self.selected_key)
        self.update()

    
    
    def handle_update(self,e):
        
        if callable(self.original_on_update):
            self.original_on_update(e)
            
            
    def get_selected(self):
        return self.selected
