import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import *

class MenuBar(Frame):
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        
    def show_about(self):
        info = "LEXIS\n\nUnreal Engine localization helper tool.\n\nAuthor: Austin Wang (awwang@igs)\nWebsite: www.austinwang.co"
        tk.messagebox.showinfo(title="About", message=info)
        
    def open_settings(self):
        msg = "Settings page has not been implemented yet :P"
        tk.messagebox.showinfo(title="About", message=msg)
    
    def setup(self):
        
        # file menu
        file_menu = Menu(self.master)
        file_menu = Menu(self.menu, tearoff=0)
        file_menu.add_command(label="About", command=self.show_about, accelerator="Ctrl+B")
        # file menu divider
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.show_about, accelerator="Ctrl+Q")
        
        self.menu.add_cascade(label="File", menu=file_menu)
        
        self.master.bind("<Control-b>", lambda e:self.show_about())
        self.master.bind("<Control-q>", sys.exit)
        
        # TODO: determine what we want for settings
        # edit menu
        edit_menu = Menu(self.master)
        edit_menu = Menu(self.menu, tearoff=0)
        edit_menu.add_command(label="Settings", command=self.open_settings, accelerator="Ctrl+S")
        
        self.menu.add_cascade(label="Edit", menu=edit_menu)
        self.master.bind("<Control-s>", lambda e:self.open_settings())