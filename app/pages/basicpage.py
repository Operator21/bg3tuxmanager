import tkinter as tk

class BasicPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.widgets = []

    def add_widget(self, widget):
        widget.pack()
        self.widgets.append(widget)

    def remove_widget(self, widget):
        widget.pack_forget()
        self.widgets.remove(widget)
