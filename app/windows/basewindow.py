import tkinter as tk
from app.utils.properties import APP_NAME, VERSION, AUTHOR

class BasicWindow:
    def __init__(self, window_title=f"{APP_NAME}_{VERSION} by {AUTHOR}"):
        self.window = tk.Tk()
        self.window.title(window_title)

        # set window to 640x480
        self.window.geometry("640x480")

        # create container for pages
        self.page_container = tk.Frame(self.window)
        self.page_container.pack()

        # make container background black
        self.page_container.config(bg="black")


    def navigate_to(self, page):
        self.page_container.pack_forget()
        self.page_container = page


    def run(self):
        self.window.mainloop()
