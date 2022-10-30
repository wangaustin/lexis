from tkinter import filedialog
from tkinter import *
root = Tk()
root.title("Austin's Test")
#root.withdraw()

def browse_file():
    label_file_explorer = filedialog.askdirectory()
    folder_path.set(label_file_explorer)
    print(label_file_explorer)


folder_path = StringVar()

label_file_explorer = Label(root, textvariable=folder_path, width = 100, height = 4, fg = "blue")

button_explore = Button(root, text="Browse Folder", command=browse_file)

button_explore.grid(row=0, column=0)
label_file_explorer.grid(row=1, column=0)

root.mainloop()