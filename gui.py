import json
import os
import shutil
import time
import sys
# custom menubar module
import menubar

import tkinter as tk
from tkinter import *

_DEBUG = False
_CACHED = False
_LOCALIZATION_GAME_DIR = "Content/Localization/Game"
_TEMP_FOLDER_NAME = "lexis-temp"

# helper functions
def delete_temp_folder(localization_dir, temp_folder):
    if not _CACHED:
        files = os.listdir(os.getcwd())

        for file in files:
            os.chmod(file, 0o0777)
            os.remove(file)

        os.chdir(localization_dir)
        os.rmdir(temp_folder)
    else:
        files = os.listdir(os.getcwd())
        
        for file in files:
            os.chmod(file, 0o0777)
            os.remove(file)
        os.chdir("..")
        os.rmdir(temp_folder)

def clear_output(event=None):
    textbox.configure(state="normal")
    textbox.delete(1.0, "end")
    textbox.configure(state="disabled")

def find_all_by_key(prompt):
    # ask user which key they want to check the translations for
    textbox.configure(state="normal")
    textbox.configure(wrap="none")
    textbox.delete(1.0, "end")

    # start timing execution
    start_time = time.time()

    # finds all json files in the current directory
    original_dir = os.getcwd()
    print(original_dir)
    localization_dir = ""

    # go to the localization/game folder
    try:
        os.chdir(_LOCALIZATION_GAME_DIR)
    except FileNotFoundError:
        print("ERROR: Directory does not exist, exiting.")
        sys.exit("LEXIS terminated.")
    except NotADirectoryError:
        print("ERROR: Not a directory, exiting.")
        sys.exit("LEXIS terminated.")
    except PermissionError:
        print("ERROR: You do not have permissions to change to that directory, exiting.")
        sys.exit("LEXIS terminated.")
        
    localization_dir = os.getcwd()
        
    # create a new temp folder
    temp_folder = _TEMP_FOLDER_NAME
    os.mkdir(temp_folder)

    # find all folder names of the different languages
    list_subfolders_names = [f.name for f in os.scandir(os.getcwd()) if f.is_dir()]

    # -----------------------------------------------------------------------
    # create json files for archive files
    for subfolder in list_subfolders_names:
        # skip the temp subfolder
        if subfolder == temp_folder:
            continue

        # show which language we're working with
        if (_DEBUG):
            print(subfolder)
        
        # build the path where we retrieve the archive file
        archive_file_name = "\\" + subfolder + "\\Game.archive"
        archive_file_path = localization_dir + archive_file_name
        # print(archive_file_path)
        
        # build the path where we store the json file (we store it in temp_folder)
        json_file_path = localization_dir + "\\" + temp_folder + "\\" + subfolder + ".json"
        
        # print(json_file_path + "\n")
        
        # create a temp corresponding json file for archive
        shutil.copy(archive_file_path, json_file_path)

    # still in localization_dir, so we need to change to temp_folder now
    os.chdir(temp_folder)

    # -----------------------------------------------------------------------
    # find all translations for the key the user inputted

    # get all the json files for all the languages
    all_json_files = os.listdir(os.getcwd())
    
    if (_DEBUG):
        print("JSON file count: %s\n" % (len(all_json_files)))

    for file in all_json_files:
        curr_file = open(file, encoding="utf-16")
        curr_file_data = json.load(curr_file)
        curr_output = ""
        found = False
        
        # try to find the key in unnamed subnamespace
        for i in curr_file_data["Children"]:
            if i["Key"] == prompt:
                curr_output = i["Translation"]["Text"]
                found = True
                
        # try to find the key in named subnamespaces
        if not found:
            for i in curr_file_data["Subnamespaces"]:
                for j in i["Children"]:
                    if j["Key"] == prompt:
                        curr_output = j["Translation"]["Text"]
                        found = True
        
        # no translation found in the current language
        if not found:
            curr_output = "*** NO TRANSLATION! ***"

        textbox.insert("end", (os.path.splitext(file)[0] + ":" + "\n" + "\t" + curr_output + "\n"))
                
        curr_file.close()
    
    textbox.configure(state="disabled")

    # -----------------------------------------------------------------------
    # delete temp folder
    if not _CACHED:
        delete_temp_folder(localization_dir, temp_folder)
    else:
        os.chdir(localization_dir)

    # -----------------------------------------------------------------------
    # going back to the directory where this python script resides
    os.chdir(original_dir)

    # report execution time
    print("\n" + "--- Execution time: %s seconds ---" % (time.time() - start_time) + "\n")

    print("[f] DONE.\n")

def find_duplicate_by_source_text(prompt, bool_case_sensitive = 1):
    
    textbox.configure(state="normal")
    textbox.configure(wrap="none")
    textbox.delete(1.0, "end")
    # start timing execution
    start_time = time.time()

    # finds all json files in the current directory
    original_dir = os.getcwd()
    localization_dir = ""

    # go to the localization/game folder
    try:
        os.chdir(_LOCALIZATION_GAME_DIR)
    except FileNotFoundError:
        print("ERROR: Directory does not exist, exiting.")
        sys.exit("LEXIS terminated.")
    except NotADirectoryError:
        print("ERROR: Not a directory, exiting.")
        sys.exit("LEXIS terminated.")
    except PermissionError:
        print("ERROR: You do not have permissions to change to that directory, exiting.")
        sys.exit("LEXIS terminated.")
        
    localization_dir = os.getcwd()
        
    # create a new temp folder
    temp_folder = _TEMP_FOLDER_NAME
    os.mkdir(temp_folder)

    # find all folder names of the different languages
    list_subfolders_names = [f.name for f in os.scandir(os.getcwd()) if f.is_dir()]

    # -----------------------------------------------------------------------
    # create just one json file for just one archive file
    for subfolder in list_subfolders_names:
        # skip the temp subfolder
        if subfolder == temp_folder:
            continue
        
        # build the path where we retrieve the archive file
        archive_file_name = "\\" + subfolder + "\\Game.archive"
        archive_file_path = localization_dir + archive_file_name
        # print(archive_file_path)
        
        # build the path where we store the json file (we store it in temp_folder)
        json_file_path = localization_dir + "{}"
        json_file_path = json_file_path.format("\\" + temp_folder + "\\" + subfolder + ".json")
        # print(json_file_path + "\n")
        
        # create a temp corresponding json file for archive
        shutil.copy(archive_file_path, json_file_path)
        break

    # still in localization_dir, so we need to change to temp_folder now
    os.chdir(temp_folder)

    # -----------------------------------------------------------------------
    # find all translations for the key the user inputted
    print("\n" + "---------------------------------")

    # get all the json files for all the languages
    all_json_files = os.listdir(os.getcwd())
    
    if (_DEBUG):
        print("JSON file count: %s\n" % (len(all_json_files)))

    for file in all_json_files:
        curr_file = open(file, encoding="utf-16")
        curr_file_data = json.load(curr_file)
        curr_output_array = []
        
        # in unnamed subnamespace, add key to array if its source text is the same as prompt
        for i in curr_file_data["Children"]:
            if not bool_case_sensitive:
                if i["Source"]["Text"].lower() == prompt.lower():
                    curr_output_array.append(i["Key"])
            else:
                if i["Source"]["Text"] == prompt:
                    curr_output_array.append(i["Key"])
                
        # in unnamed subnamespace, add key to array if its source text is the same as prompt
        for i in curr_file_data["Subnamespaces"]:
            for j in i["Children"]:
                if not bool_case_sensitive:
                    if j["Source"]["Text"].lower() == prompt.lower():
                        curr_output_array.append(j["Key"])
                else:
                    if j["Source"]["Text"] == prompt:
                        curr_output_array.append(j["Key"])
        
        if (len(curr_output_array) > 0):
            textbox.insert("end", ("All keys found:" + "\n\n"))
        else:
            textbox.insert("end", ("*** NO KEY FOUND! ***"))
        
        for i in curr_output_array:
            textbox.insert("end", (i + "\n"))
                
        curr_file.close()
        break

    textbox.configure(state="disabled")

    # -----------------------------------------------------------------------
    # delete temp folder
    if not _CACHED:
        delete_temp_folder(localization_dir, temp_folder)
    else:
        os.chdir(localization_dir)

    # -----------------------------------------------------------------------
    # going back to the directory where this python script resides
    os.chdir(original_dir)

    # report execution time
    print("\n" + "--- Execution time: %s seconds ---" % (time.time() - start_time) + "\n")
    print("[d] DONE.\n")
    
def print_localization_stats():
    textbox.configure(state="normal")
    textbox.configure(wrap="none")
    textbox.delete(1.0, "end")
    # start timing execution
    start_time = time.time()

    # finds all json files in the current directory
    original_dir = os.getcwd()
    localization_dir = ""

    # go to the localization/game folder
    try:
        os.chdir(_LOCALIZATION_GAME_DIR)
    except FileNotFoundError:
        print("ERROR: Directory does not exist, exiting.")
        sys.exit("LEXIS terminated.")
    except NotADirectoryError:
        print("ERROR: Not a directory, exiting.")
        sys.exit("LEXIS terminated.")
    except PermissionError:
        print("ERROR: You do not have permissions to change to that directory, exiting.")
        sys.exit("LEXIS terminated.")
        
    localization_dir = os.getcwd()
        
    # create a new temp folder
    temp_folder = _TEMP_FOLDER_NAME
    os.mkdir(temp_folder)

    # find all folder names of the different languages
    list_subfolders_names = [f.name for f in os.scandir(os.getcwd()) if f.is_dir()]

    # -----------------------------------------------------------------------
    # create json files for archive files
    for subfolder in list_subfolders_names:
        # skip the temp subfolder
        if subfolder == temp_folder:
            continue
        
        # build the path where we retrieve the archive file
        archive_file_name = "\\" + subfolder + "\\Game.archive"
        archive_file_path = localization_dir + archive_file_name
        if (_DEBUG):
            print(archive_file_path)
        
        # build the path where we store the json file (we store it in temp_folder)
        json_file_path = localization_dir + "\\" + temp_folder + "\\" + subfolder + ".json"
        if (_DEBUG):
            print(json_file_path + "\n")
        
        # create a temp corresponding json file for archive
        shutil.copy(archive_file_path, json_file_path)

    # still in localization_dir, so we need to change to temp_folder now
    os.chdir(temp_folder)

    # -----------------------------------------------------------------------
    # find all translations for the key the user inputted
    print("\n" + "---------------------------------")

    # get all the json files for all the languages
    all_json_files = os.listdir(os.getcwd())

    for file in all_json_files:
        curr_file = open(file, encoding="utf-16")
        curr_file_data = json.load(curr_file)
        curr_translated_count = 0
        curr_untranslated_count = 0
        
        # try to find the key in unnamed subnamespace
        for i in curr_file_data["Children"]:
            if i["Translation"]["Text"] == "":
                curr_untranslated_count += 1
            else:
                curr_translated_count += 1
                
        # try to find the key in named subnamespaces
        for i in curr_file_data["Subnamespaces"]:
            for j in i["Children"]:
                if j["Translation"]["Text"] == "":
                    curr_untranslated_count += 1
                else:
                    curr_translated_count += 1
        
        textbox.insert("end", (os.path.splitext(file)[0] + ":" + "\n\tTranslated count:\t%s" %curr_translated_count + "\n\tUntranslated count:\t%s\n" %curr_untranslated_count))
                
        curr_file.close()

    textbox.configure(state="disabled")

    # -----------------------------------------------------------------------
    # delete temp folder
    if not _CACHED:
        delete_temp_folder(localization_dir, temp_folder)
    else:
        os.chdir(localization_dir)

    # -----------------------------------------------------------------------
    # going back to the directory where this python script resides
    os.chdir(original_dir)

    # report execution time
    print("\n" + "--- Execution time: %s seconds ---" % (time.time() - start_time) + "\n")
    print("[stats] DONE.\n")


# --------------------- (setup root window) ----------------------------------
root = tk.Tk()
root.title("LEXIS")
root.minsize(1000, 700)

# set LEXIS logo
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
elif __file__:
    application_path = os.path.dirname(__file__)
    
icon_file = "lexis-logo.ico"
root.iconbitmap(default=os.path.join(application_path, icon_file))

#setup root window's menubar
menu = menubar.MenuBar(root)
menu.setup()

# root.resizable(width=False, height=False)

# --------------------- (setup frame layout) ----------------------------------
# frame
Frame_Title = tk.Frame(master=root)
Frame_Title.grid(row=0, column=0, pady=2, sticky="w")

Frame_Find_By_Key = tk.Frame(master=root)
Frame_Find_By_Key.grid(row=1, column=0, pady=10, padx=(10,0), sticky="w")

Frame_Unimplemnted_Functionality = tk.Frame(master=root)
Frame_Unimplemnted_Functionality.grid(row=1, column=1, pady=10, padx=(10,0),sticky="w")

Frame_Find_By_Source_Text = tk.Frame(master=root)
Frame_Find_By_Source_Text.grid(row=2, column=0, pady=20, padx=(10,0),sticky="w")

# Frame_New_Functionality = tk.Frame(master=root)
# Frame_New_Functionality.grid(row=2, column=1, pady=20, sticky="w")

Frame_Atomic_Operations = tk.Frame(master=root)
Frame_Atomic_Operations.grid(row=3, column=0, pady=5, padx=(10,0),sticky="w")

Frame_Output_Box = tk.Frame(master=root)
Frame_Output_Box.grid(row=4, column=0, pady=5, padx=(10,0),sticky="w")


# --------------------- FIND TRANSLATIONS ----------------------------------
# input box
ent_lockey = tk.Entry(master=Frame_Find_By_Key, width=50)
# label
lbl_temp = tk.Label(master=Frame_Find_By_Key, text="Enter LOCTEXT Key: ", font=(10))

# using the .grid() geometry manager
lbl_temp.grid(row=0, column=0, sticky="w")
ent_lockey.grid(row=0, column=1, sticky="w")

# Button (Find Translations)
btn_find_by_key = tk.Button(
    master=Frame_Find_By_Key,
    text="Find Translations",
    command=lambda: find_all_by_key(ent_lockey.get()),
    anchor="w",
    justify="left"
)
btn_find_by_key.grid(row=1, column=0, pady=2, sticky="w")


# --------------------- FIND DUPLICATES ----------------------------------
# label
lbl_source_text = tk.Label(master=Frame_Find_By_Source_Text, text="Enter Source Text: ", font=(10))
lbl_source_text.grid(row=0, column=0, sticky="w")
# input box
ent_source_text = tk.Entry(master=Frame_Find_By_Source_Text, width=50)
ent_source_text.grid(row=0, column=1, sticky="w")

# Button (Find Duplicates)
btn_find_by_source_text = tk.Button(
    master=Frame_Find_By_Source_Text,
    text="Find Duplicates",
    command=lambda: find_duplicate_by_source_text(ent_source_text.get(), checkbox_case_sensitive.get()),
    anchor="w",
    justify="left"
)
btn_find_by_source_text.grid(row=1, column=0, pady=2, sticky="w")

# Checkbox (Case Sensitive)
checkbox_case_sensitive = IntVar(value=0)

checkbox_button = Checkbutton(
    master=Frame_Find_By_Source_Text,
    text="Case Sensitive",
    variable = checkbox_case_sensitive,
    onvalue=1,
    offvalue=0,
    height=2,
    width=10
)
checkbox_button.grid(row=1, column=1, pady=2, sticky="w")

# --------------------- (atomic operations, like "CLEAR OUTPUT") ----------------------------------
# Button (Clear Output)
btn_clear_output = tk.Button(
    master=Frame_Atomic_Operations,
    text="Clear Output",
    command=clear_output,
    anchor="w",
    justify="left"
)
btn_clear_output.grid(row=0, column=0, pady=2, sticky="w")

# Button (Show Stats)
btn_clear_output = tk.Button(
    master=Frame_Atomic_Operations,
    text="Show Stats",
    command=print_localization_stats,
    anchor="w",
    justify="left"
)
btn_clear_output.grid(row=0, column=1, pady=2, padx=(10,0), sticky="w")



# scrollbar
y_scrollbar = Scrollbar(Frame_Output_Box, orient="vertical")
x_scrollbar = Scrollbar(Frame_Output_Box, orient="horizontal")
# -------------------------------------------------------
# Textbox (output)
textbox = tk.Text(master=Frame_Output_Box, height=1, borderwidth=0, yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
y_scrollbar.config(command=textbox.yview)
x_scrollbar.config(command=textbox.xview)

textbox.grid(row=0, column=0, pady=(2,0), sticky="w")
textbox["width"] = 160
textbox["height"] = 30
textbox.configure(state="disabled")
textbox.configure(inactiveselectbackground=textbox.cget("selectbackground"))

root.bind('<Control-e>', clear_output)
ent_lockey.bind('<Return>', lambda e: find_all_by_key(ent_lockey.get()))
ent_source_text.bind('<Return>', lambda e: find_duplicate_by_source_text(ent_source_text.get(), checkbox_case_sensitive.get()))
# ent_lockey.bind('<Control-x>', lambda x: print(root.focus_get()))


y_scrollbar.grid(row=0, column=2, sticky="nse")
x_scrollbar.grid(row=1, column=0, sticky="wse")

# Run the application
root.mainloop()