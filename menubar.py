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
    
    def setup(self):
        
        file_menu = Menu(self.master)
        file_menu.add_command(label="Undo")
        file_menu.add_command(label="Redo")
        file_menu.add_command(label="About", command=self.show_about, accelerator="Ctrl+W")
        
        self.menu.add_cascade(label="File", menu=file_menu)
        
        self.master.bind("<Control-w>", lambda e:self.show_about())