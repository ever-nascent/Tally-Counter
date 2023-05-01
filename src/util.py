import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog
from tkinter import messagebox
import os.path
import pickle

class BaseGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.configure_window()

    def configure_window(self):
        self.root.title("Tally Counter")
        self.root.geometry("275x384")
        self.root.resizable(False, False)
        self.root.configure(background="#484454")

    def run(self):
        self.root.mainloop()

class GUI(BaseGUI):
    def __init__(self, counter_manager):
        super().__init__()
        self.counter_manager = counter_manager

        self.create_widgets()
        self.root.after(0, self.start_auto_saving())

    def create_widgets(self):
        self.counter_dropdown = CounterDropdown(self.counter_manager, self.root)
        self.counter_display = CounterDisplay(self.counter_dropdown, self.root)
        self.counter_options = CounterOptions(self.counter_manager, self.counter_dropdown, self.counter_display, self.root)
        self.counter_buttons = CounterButtons(self.counter_manager, self.counter_dropdown, self.counter_display, self.root)

    def start_auto_saving(self):
        self.counter_manager.auto_save_counter_data()
        time_interval = 60000
        self.root.after(time_interval, self.counter_manager.auto_save_counter_data)

class CounterDropdown:
    def __init__(self, counter_manager, parent):
        self.counter_manager = counter_manager
        self.parent = parent
        self.create_dropdown()
    
    def create_dropdown(self):
        counter_names = self.counter_manager.get_counter_names()
        
        self.dropdown = ttk.Combobox(
            self.parent,
            state="readonly",
            values=counter_names
        )

        self.dropdown.current(0)
        self.dropdown.grid()
    
    def get_current_counter_name(self):
        return self.dropdown.get()
        
    def get_current_counter(self):
        selected_counter_name = self.get_current_counter_name()
        selected_counter = self.counter_manager.get_counter(selected_counter_name)
        return selected_counter
    
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
        new_count = self.counter_dropdown.get_current_counter().count
        self.counter_label.config(text=new_count)

class CounterOptions():
    def __init__(self, counter_manager, counter_dropdown, counter_display, parent):
        self.parent = parent
        self.counter_manager = counter_manager
        self.counter_dropdown = counter_dropdown
        self.counter_display = counter_display

        self.create_options_button()

    def create_options_button(self):
        options = {
            'Set Counter To...': self.set_count,
            'Reset Counter': self.reset_count,
            'Delete Counter': self.del_counter
        }

        options_menu = ttk.Menubutton(self.parent)

        menu = tk.Menu(options_menu, tearoff=0)

        for option in options:
            menu.add_command(
                label=option,
                command=options[option]
            )

        options_menu["menu"] = menu 
        options_menu.grid()

    def set_count(self):
        current_counter = self.counter_dropdown.get_current_counter()
        
        new_count = simpledialog.askinteger(
            parent=self.parent,
            title="",
            prompt="Set Counter To New Value"
        )

        if new_count and new_count != current_counter.count:
            current_counter.count = new_count
            self.counter_display.update_counter_display(new_count)
    
    def reset_count(self):
        selected_counter = self.counter_dropdown.get_current_counter()

        confirmed = messagebox.askokcancel("Reset Counter", f"Are you sure you want to reset the current counter?")

        if (confirmed):
            selected_counter.reset()

            new_count = selected_counter.count
            self.counter_display.update_counter_display(new_count)

    def del_counter(self):
        counters_left = self.counter_manager.get_counter_dict_length()

        if counters_left == 1:
            return messagebox.showwarning("Unable to delete Counter", "You cannot remove the last counter.")
        
        confirmed = messagebox.askokcancel("Delete Counter", f"Are you sure you want to delete the current counter?")

        if (confirmed):
            current_counter_name = self.counter_dropdown.get_current_counter_name()
            self.counter_manager.remove_counter(current_counter_name)

            self.counter_dropdown.dropdown['values'] = self.counter_manager.get_counter_names()
            
            last_item_in_dropdown = self.counter_manager.get_counter_dict_length() - 1
            self.counter_dropdown.dropdown.current(last_item_in_dropdown)

            new_count = self.counter_dropdown.get_current_counter().count
            self.counter_display.update_counter_display(new_count)

class CounterButtons():
    def __init__(self, counter_manager, counter_dropdown, counter_display, parent):
        self.parent = parent
        self.counter_manager = counter_manager
        self.counter_dropdown = counter_dropdown
        self.counter_display = counter_display
        self.create_increment_button()
        self.create_decrement_button()

    def create_increment_button(self):
        self.increment_image = tk.PhotoImage(file='assets/increment_button.png')
        self.increment_hover_image = tk.PhotoImage(file='assets/increment_button_hover.png')

        self.increment_button = tk.Button(
            self.parent,
            image=self.increment_image,
            background=self.parent["bg"],
            activebackground=self.parent["bg"],
            borderwidth=0,
            command=self.increment_count
        )

        self.increment_button.bind("<Enter>", lambda event: self.increment_button.config(image=self.increment_hover_image))
        self.increment_button.bind("<Leave>", lambda event: self.increment_button.config(image=self.increment_image))

        self.increment_button.grid()

    def increment_count(self):
        selected_counter = self.counter_dropdown.get_current_counter()
        selected_counter.increment()

        new_count = selected_counter.count
        self.counter_display.update_counter_display(new_count)

    def create_decrement_button(self):
        self.decrement_image = tk.PhotoImage(file='assets/decrement_button.png')
        self.decrement_hover_image = tk.PhotoImage(file='assets/decrement_button_hover.png')

        self.decrement_button = tk.Button(
            self.parent,
            image=self.decrement_image,
            background=self.parent["bg"],
            activebackground=self.parent["bg"],
            borderwidth=0,
            command=self.decrement_count
        )

        self.decrement_button.bind("<Enter>", lambda event: self.decrement_button.config(image=self.decrement_hover_image))
        self.decrement_button.bind("<Leave>", lambda event: self.decrement_button.config(image=self.decrement_image))

        self.decrement_button.grid()

    def decrement_count(self):
        selected_counter = self.counter_dropdown.get_current_counter()
        selected_counter.decrement()

        new_count = selected_counter.count
        self.counter_display.update_counter_display(new_count)

class Counter:
    def __init__(self, count, increment_value, decrement_value, symbol):
        self.count = count
        self.increment_value = increment_value
        self.decrement_value = decrement_value
        self.symbol = symbol

    def increment(self):
        self.count += self.increment_value

    def decrement(self):
        self.count -= self.decrement_value

    def reset(self):
        self.count = 0

class CounterManager:
    def __init__(self, counter_dict):
        self.counter_dict = counter_dict

    def create_new_counter(self, counter_name="Unnamed Counter", count=0, increment_value=1, decrement_value=1, symbol=None):
        counter_name = self.validate_unique_counter_name(counter_name)
        self.counter_dict[counter_name] = Counter(count, increment_value, decrement_value, symbol)

    def remove_counter(self, counter_name):
        del self.counter_dict[counter_name]

    def get_counter_names(self):
        all_counter_names = self.counter_dict.keys()
        return list(all_counter_names)
    
    def get_counter_dict_length(self):
        return len(self.counter_dict)
    
    def get_counter(self, counter_name):
        return self.counter_dict[counter_name]
     
    def auto_save_counter_data(self):
        with open("counter_data.pickle", "wb") as file:
            pickle.dump(self.counter_dict, file)

    def validate_unique_counter_name(self, name):
        if name not in self.counter_dict:
            return name
        else:
            i = 2
        while True:
            new_name = f"{name} {i}"
        
            if new_name not in self.counter_dict:
                return new_name
            i += 1

def data_file_exists():
    if os.path.isfile("counter_data.pickle"):
        with open("counter_data.pickle", "rb") as file:
            return pickle.load(file)
    else:
        counter_dict = {}
        with open("counter_data.pickle", "wb") as file:
            pickle.dump(counter_dict, file)
        return counter_dict

def create_initial_counter(manager):
    counter_dict_length = manager.get_counter_dict_length()

    if counter_dict_length == 0:
        manager.create_new_counter()

    counter_data = data_file_exists()
    return counter_data

def TallyCounterApp():
    counter_data = data_file_exists()

    manager = CounterManager(counter_data)
    create_initial_counter(manager)

    gui = GUI(manager)
    gui.run()