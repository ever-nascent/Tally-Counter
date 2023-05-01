from tkinter import ttk

class CounterDisplay():
    def __init__(self, counter_dropdown, parent):
        self.parent = parent
        self.counter_dropdown = counter_dropdown
        self.create_counter_display()
        
        self.counter_dropdown.dropdown.bind("<<ComboboxSelected>>", self.update_counter_display)

    def create_counter_display(self):
        self.font_family = "Arial"
        self.font_size = 80

        initial_count = self.counter_dropdown.get_current_counter().count

        self.counter_label = ttk.Label(
            self.parent,
            text=initial_count,
            font=(self.font_family, self.font_size),
            background=self.parent["bg"],
            foreground="#7289DA"
        )

        self.counter_label.grid()
    
    def update_counter_display(self, event=None):
        current_counter = self.counter_dropdown.get_current_counter()
        current_counter_count = current_counter.count

        self.counter_label.config(text=current_counter_count)