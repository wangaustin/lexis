# author: Austin Wang (awwang@igs)
# website: www.austinwang.co
# date: October 28, 2022


# python script to read json file
import json
import glob, os

# ask user which key they want to check the translations for
prompt = input("Input text string: ")

# open json file
zhHans_file = open('zhHans.json', encoding="utf-8")
fr_file = open('fr.json', encoding="utf-8")

# load json files
zhHans_data = json.load(zhHans_file)
fr_data = json.load(fr_file)

# populate translation outputs for all languages
zhHans_output = ""
fr_output = ""

# try to find the key in unnamed subnamespace
for i in zhHans_data["Children"]:
    if i["Key"] == prompt:
        zhHans_output = i["Translation"]["Text"]

# try to find the key in named subnamespaces
for i in zhHans_data["Subnamespaces"]:
    for j in i["Children"]:
        if j["Key"] == prompt:
            zhHans_output = j["Translation"]["Text"]
    
for i in fr_data["Children"]:
    if i["Key"] == prompt:
        fr_output = i["Translation"]["Text"]
        
for i in fr_data["Subnamespaces"]:
    for j in i["Children"]:
        if j["Key"] == prompt:
            fr_output = j["Translation"]["Text"]

# print translation outputs
print("Simplified Chinese: " + zhHans_output)
print("French: " + fr_output + "\n")

# close files
zhHans_file.close()
fr_file.close()