import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self, counter_manager):
        self.counter_manager = counter_manager
        self.root = tk.Tk()
        self.root.title("Tally Counter")
        self.root.geometry("275x384")
        self.root.resizable(False, False)
        self.root.configure(background="#484454")

        self.create_widgets()

    def create_widgets(self):
        self.create_counter_dropdown()
        self.create_counter_display()
        self.create_increment_button()
        self.create_decrement_button()

    def create_counter_dropdown(self):
        counter_names = self.counter_manager.get_counter_names()

        self.counter_dropdown = ttk.Combobox(
            self.root,
            state="readonly",
            values=counter_names
        )

        self.counter_dropdown.current(0)
        self.counter_dropdown.pack()
        self.counter_dropdown.bind("<<ComboboxSelected>>", self.counter_selected)

    def create_counter_display(self):
        initial_count = self.current_counter().count

        self.counter_display = tk.Label(
            self.root,
            text= initial_count,
            font=("Arial", 40),
            bg=self.root["bg"]
        )

        self.counter_display.pack()

    def create_increment_button(self):
        self.increment_button = ttk.Button(
            self.root,
            text="+",
            command= self.increment
        )

        self.increment_button.pack()

    def create_decrement_button(self):
        self.decrement_button = ttk.Button(
            self.root,
            text="-",
            command= self.decrement
        )

        self.decrement_button.pack()

    def increment(self):
        selected_counter = self.current_counter()
        selected_counter.increment_count()
        self.update_counter_display(selected_counter.count)

    def decrement(self):
        selected_counter = self.current_counter()
        selected_counter.decrement_count()
        self.update_counter_display(selected_counter.count)

    def current_counter(self):
        selected_counter_name = self.counter_dropdown.get()
        selected_counter = self.counter_manager.get_counter(selected_counter_name)
        return selected_counter

    def counter_selected(self, event):
        selected_counter = self.current_counter()
        self.update_counter_display(selected_counter.count)

    def update_counter_display(self, count):
        self.counter_display.config(text=count)

    def run(self):
        self.root.mainloop()

class Counter:
    def __init__(self, count, increment_value, decrement_value, symbol):
        self.count = count
        self.increment_value = increment_value
        self.decrement_value = decrement_value
        self.symbol = symbol

    def increment_count(self):
        self.count += self.increment_value

    def decrement_count(self):
        self.count -= self.decrement_value


class CounterManager:
    def __init__(self):
        self.counters_dict = {}

    def create_new_counter(self, counter_name="Unnamed Counter", count=0, increment_value=1, decrement_value=1, symbol=None):
        counter_name = self.validate_unique_counter_name(counter_name)
        self.counters_dict[counter_name] = Counter(count, increment_value, decrement_value, symbol)

    def delete_counter(self, counter_name):
        del self.counters_dict[counter_name]

    def get_counter_names(self):
        return list(self.counters_dict.keys())
    
    def get_counter(self, counter_name):
        return self.counters_dict[counter_name]
    
    def validate_unique_counter_name(self, name):
        if name not in self.counters_dict:
            return name
        else:
            i = 2

        while True:
            new_name = f"{name} {i}"
            
            if new_name not in self.counters_dict:
                return new_name
            i += 1

def TallyCounterApp():
    counter_manager = CounterManager()

    if len(counter_manager.counters_dict) == 0:
        counter_manager.create_new_counter()
 
    gui = GUI(counter_manager)
    gui.run()