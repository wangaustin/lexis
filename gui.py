import json
import os
import shutil
import time
import sys
# custom menubar module
import menubar

import tkinter as tk

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
    localization_dir = ""

    # assuming this python script is placed in \Beef\Sheik

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
        
        if (_DEBUG):
            print(json_file_path + "\n")
        
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
        
        # lbl_result["text"]+=(os.path.splitext(file)[0] + ":" + "\n" + "\t" + curr_output + "\n")
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

def print_localization_stats():
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
        
        lbl_result["text"]+=(os.path.splitext(file)[0] + ":" + "\n\tTranslated count:\t%s" %curr_translated_count + "\n\tUntranslated count:\t%s\n" %curr_untranslated_count)
                
        curr_file.close()

    print("---------------------------------" + "\n")

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


# Set up the window
window = tk.Tk()
window.title("LEXIS GUI")
window.minsize(1000, 600)

#setup root window's menubar
menubar.setup(window)

# window.resizable(width=False, height=False)

frm_prompt = tk.Frame(master=window)
ent_lockey = tk.Entry(master=frm_prompt, width=50)
lbl_temp = tk.Label(master=frm_prompt, text="Enter LOCTEXT key: ", font=(10))

# using the .grid() geometry manager
lbl_temp.grid(row=1, column=0, sticky="w")
ent_lockey.grid(row=1, column=1, sticky="w")

# Create the conversion Button and result display Label
btn_find_by_key = tk.Button(
    master=frm_prompt,
    text="Find Translations",
    command=lambda: find_all_by_key(ent_lockey.get()),
    anchor="w",
    justify="left"
)

# Create the conversion Button and result display Label
btn_clear_output = tk.Button(
    master=window,
    text="Clear Output",
    command=clear_output,
    anchor="w",
    justify="left"
)

textbox = tk.Text(master=window, height=1, borderwidth=0)

frm_prompt.grid(row=1, column=0, pady=20, sticky="w")
btn_find_by_key.grid(row=2, column=0, pady=2, sticky="w")
btn_clear_output.grid(row=3, column=0, pady=2, sticky="w")

textbox.grid(row=4, column=0, pady=2, sticky="w")
textbox["width"] = 140
textbox["height"] = 30
textbox.configure(state="disabled")
textbox.configure(inactiveselectbackground=textbox.cget("selectbackground"))

# window.bind('<Control-q>', sys.exit)
window.bind('<Control-e>', clear_output)

# Run the application
window.mainloop()