import tkinter as tk
from app.pages.basicpage import BasicPage

class ModListPage(BasicPage):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.reload_button = tk.Button(self, text="Reload Mods")
        self.reload_button.pack(fill='x')

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill='both', expand=True, padx=20, pady=20)

        self.config(width=800)
