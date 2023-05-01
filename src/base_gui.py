import tkinter as tk

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