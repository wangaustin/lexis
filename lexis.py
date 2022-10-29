# author: Austin Wang (awwang@igs)
# website: www.austinwang.co
# date: October 28, 2022

# python script to read json file
import json
import os
import shutil
import time
import sys

_DEBUG = False

def find_all_by_key():
    # ask user which key they want to check the translations for
    prompt = input("Input text string key: ")

    # start timing execution
    start_time = time.time()

    # finds all json files in the current directory
    original_dir = os.getcwd()
    localization_dir = ""

    # assuming this python script is placed in \Beef\Sheik

    # go to the localization/game folder
    try:
        os.chdir("Content/Localization/Game")
    except FileNotFoundError:
        print("ERROR: Directory does not exist, exiting.")
        sys.exit("Script terminated.")
    except NotADirectoryError:
        print("ERROR: Not a directory, exiting.")
        sys.exit("Script terminated.")
    except PermissionError:
        print("ERROR: You do not have permissions to change to that directory, exiting.")
        sys.exit("Script terminated.")
        
    localization_dir = os.getcwd()
        
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
        if (_DEBUG):
            print(subfolder)
        
        # build the path where we retrieve the archive file
        archive_file_name = "\\" + subfolder + "\\Game.archive"
        archive_file_path = localization_dir + archive_file_name
        # print(archive_file_path)
        
        # build the path where we store the json file (we store it in temp_folder)
        json_file_path = localization_dir + "{}"
        json_file_path = json_file_path.format("\\" + temp_folder + "\\" + subfolder + ".json")
        
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

    # assuming this python script is placed in \Beef\Sheik

    # go to the localization/game folder
    try:
        os.chdir("Content/Localization/Game")
    except FileNotFoundError:
        print("ERROR: Directory does not exist, exiting.")
        sys.exit("Script terminated.")
    except NotADirectoryError:
        print("ERROR: Not a directory, exiting.")
        sys.exit("Script terminated.")
    except PermissionError:
        print("ERROR: You do not have permissions to change to that directory, exiting.")
        sys.exit("Script terminated.")
        
    localization_dir = os.getcwd()
        
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
        
        print(os.path.splitext(file)[0] + ":" + "\n\tTranslated count:\t%s" %curr_translated_count + "\n\tUntranslated count:\t%s" %curr_untranslated_count)
                
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
    os.chdir(original_dir)

    # report execution time
    print("\n" + "--- Execution time: %s seconds ---" % (time.time() - start_time) + "\n")
    print("[stats] DONE.\n")

def find_duplicate_by_source_text():
    # ask user which key they want to check the translations for
    prompt = input("Input source text (case sensitive): ")
    
    # start timing execution
    start_time = time.time()

    # finds all json files in the current directory
    original_dir = os.getcwd()
    localization_dir = ""

    # assuming this python script is placed in \Beef\Sheik

    # go to the localization/game folder
    try:
        os.chdir("Content/Localization/Game")
    except FileNotFoundError:
        print("ERROR: Directory does not exist, exiting.")
        sys.exit("Script terminated.")
    except NotADirectoryError:
        print("ERROR: Not a directory, exiting.")
        sys.exit("Script terminated.")
    except PermissionError:
        print("ERROR: You do not have permissions to change to that directory, exiting.")
        sys.exit("Script terminated.")
        
    localization_dir = os.getcwd()
        
    # create a new temp folder
    temp_folder = "lexis-temp"
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
            if i["Source"]["Text"] == prompt:
                curr_output_array.append(i["Key"])
                
        # in unnamed subnamespace, add key to array if its source text is the same as prompt
        for i in curr_file_data["Subnamespaces"]:
            for j in i["Children"]:
                if j["Source"]["Text"] == prompt:
                    curr_output_array.append(j["Key"])
        
        if (len(curr_output_array) > 0):
            print("All keys found:" + "\n\t")
        else:
            print("*** NO KEY FOUND! ***")
        
        for i in curr_output_array:
            print(i)
                
        curr_file.close()
        break

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
    os.chdir(original_dir)

    # report execution time
    print("\n" + "--- Execution time: %s seconds ---" % (time.time() - start_time) + "\n")
    print("[stats] DONE.\n")


# start of the script
print("\nWelcome to LEXIS!\n")

# enable viewing characters like Chinese and Japanese
print("Setting things up...")
print("Enabling viewing of characters like Chinese and Japanese...")
os.system("chcp 936")
print("Setup is complete.")
print("LEXIS is ready for use.\n")

while True:
    command = input(">")
    if command == "quit" or command == 'q':
        sys.exit("Terminated script.")
    elif command == "h" or command == "help":
        print("\nList of available commands:\n")
        print("[k]\tFind all translations according to a LOCTEXT key.")
        print("[s]\tShow localization stats: how many LOCTEXT keys has been translated, and how many have not.")
        print("[d]\tFind all keys which have the same source text. Helps find duplicates.")
        print("[debug_on]\tTurn debug mode on.")
        print("[debug_off]\tTurn debug mode off.")
        print("")
    elif command == "k" or command == "findkey":
        find_all_by_key()
    elif command == "s" or command == "stats":
        print_localization_stats()
    elif command == "d" or command == "findduplicate":
        find_duplicate_by_source_text()
    elif command == "debug_on":
        _DEBUG = True
        print("Debug mode: ON")
    elif command == "debug_off":
        _DEBUG = False
        print("Debug mode: OFF")
