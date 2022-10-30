import sys
import tkinter as tk
from tkinter import messagebox

def show_about(self):
    info = "LEXIS\n\nUnreal Engine localization helper tool.\n\nAuthor: Austin Wang (awwang@igs)\nWebsite: www.austinwang.co"
    tk.messagebox.showinfo(title="About", message=info)
    
# todo: this is bad, come back to find the root cause of the problem
def show_about1():
    info = "LEXIS\n\nUnreal Engine localization helper tool.\n\nAuthor: Austin Wang (awwang@igs)\nWebsite: www.austinwang.co"
    tk.messagebox.showinfo(title="About", message=info)

def setup(window):
    # create a menu bar
    menu_bar = tk.Menu(window)

    # add file menu
    file_menu = tk.Menu(menu_bar, tearoff=False)
    
    file_menu.add_command(
        label="About",
        command=show_about1,
        accelerator="(Ctrl+B)"
    )
    
    file_menu.add_command(
        label="Exit",
        command=sys.exit,
        accelerator="(Ctrl+Q)"
    )

    menu_bar.add_cascade(
        label="File",
        menu=file_menu
    )
    
    # add edit menu
    edit_menu = tk.Menu(menu_bar, tearoff=False)
    
    edit_menu.add_command(
        label="Settings",
        command=show_about
    )
    
    menu_bar.add_cascade(
        label="Edit",
        menu=edit_menu,
    )
    
    window.bind_all("<Control-b>", show_about)
    window.bind_all("<Control-q>", sys.exit)
    window.config(menu=menu_bar)
