from base_gui import BaseGUI
from counter_dropdown import CounterDropdown
from counter_display import CounterDisplay
from counter_options import CounterOptions
from counter_buttons import CounterButtons

class GUI(BaseGUI):
    def __init__(self, counter_manager):
        super().__init__()

        self.counter_manager = counter_manager
        self.create_widgets()

    def create_widgets(self):
        self.counter_dropdown = CounterDropdown(self.counter_manager, self.root)
        self.counter_display = CounterDisplay(self.counter_dropdown, self.root)
        self.counter_options = CounterOptions(self.counter_manager, self.counter_dropdown, self.counter_display, self.root)
        self.counter_buttons = CounterButtons(self.counter_dropdown, self.counter_display, self.root)

