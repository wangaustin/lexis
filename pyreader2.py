# author: Austin Wang (awwang@igs)
# website: www.austinwang.co
# date: October 28, 2022


# python script to read json file
import json
import os
import shutil

# # ask user which key they want to check the translations for
# prompt = input("Input text string: ")

# # open json file
# zhHans_file = open('zhHans.json', encoding="utf-8")
# fr_file = open('fr.json', encoding="utf-8")

# # load json files
# zhHans_data = json.load(zhHans_file)
# fr_data = json.load(fr_file)

# # populate translation outputs for all languages
# zhHans_output = ""
# fr_output = ""

# for i in zhHans_data["Children"]:
    # if i["Key"] == prompt:
        # zhHans_output = i["Translation"]["Text"]
    
# for i in fr_data["Children"]:
    # if i["Key"] == prompt:
        # fr_output = i["Translation"]["Text"]

# # print translation outputs
# print("Simplified Chinese: " + zhHans_output)
# print("French: " + fr_output + "\n")

# # close files
# zhHans_file.close()
# fr_file.close()

# finds all json files in the current directory
original_dir = os.getcwd()
print("Current working dir: " + original_dir + "\n")

# for file in os.listdir(current_dir):
    # if file.endswith(".archive"):
        # print(os.path.join(current_dir, file))
        

# assuming this python script is placed in \Beef\Sheik

# go to the localization folder
try:
    os.chdir("Content/Localization/Game")
    print("Current working dir again: " + os.getcwd() + "\n")
except FileNotFoundError:
    print("Directory: does not exist")
except NotADirectoryError:
    print("Not a directory")
except PermissionError:
    print("You do not have permissions to change to that dir")

# find all folder names of the different languages
list_subfolders_names = [f.name for f in os.scandir(os.getcwd()) if f.is_dir()]

for subfolder in list_subfolders_names:
    print(subfolder)
    
testfile = open('test.archive')
testfile.close()

# create a temp corresponding json file for archive
shutil.copy("test.archive", "test.json")

# going back to the directory where this python script resides
print("\n" + "Going back to start directory...")
os.chdir(original_dir)
original_dir = os.getcwd()
print("Current working dir: " + original_dir + "\n")