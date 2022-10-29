# author: Austin Wang (awwang@igs)
# website: www.austinwang.co
# date: October 28, 2022

# python script to read json file
import json
import os
import shutil
import time

# enable viewing characters like Chinese and Japanese
print("Enabling viewing of characters like Chinese and Japanese...")
os.system("chcp 936")
print("Viewing enabled." + "\n")

# ask user which key they want to check the translations for
prompt = input("Input text string key: ")

start_time = time.time()

# finds all json files in the current directory
original_dir = os.getcwd()
localization_dir = ""

# assuming this python script is placed in \Beef\Sheik

# go to the localization/game folder
try:
    os.chdir("Content/Localization/Game")
    localization_dir = os.getcwd()
except FileNotFoundError:
    print("Directory does not exist")
except NotADirectoryError:
    print("Not a directory")
except PermissionError:
    print("You do not have permissions to change to that directory")
    
# create a new temp folder
temp_folder = "lexis-temp"
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
    # print(subfolder)
    
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

# still in localization_dir, so we need to change to temp_folder now
os.chdir(temp_folder)

# -----------------------------------------------------------------------
# find all translations for the key the user inputted
print("\n" + "---------------------------------")

all_json_files = os.listdir(os.getcwd())

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
    
    if not found:
        curr_output = "***NO TRANSLATION!***"
    print(os.path.splitext(file)[0] + ":" + "\n" + "\t" + curr_output)
            
    curr_file.close()

print("---------------------------------" + "\n")

# -----------------------------------------------------------------------
# delete temp folder
files = os.listdir(os.getcwd())

for file in files:
    os.chmod(file, 0o0777)
    os.remove(file)

os.chdir(localization_dir)
os.rmdir(temp_folder)

# -----------------------------------------------------------------------
# going back to the directory where this python script resides
# idk why i'm doing this but just in case
os.chdir(original_dir)

print("\n" + "--- Execution time: %s seconds ---" % (time.time() - start_time) + "\n")

print("DONE.")