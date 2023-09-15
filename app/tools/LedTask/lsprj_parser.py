# convert 123.lsprj  to json
# read file (123.lsprj) 
# parse it to json save to file (123.json)

# the 123.lsprj is a xml file 
import json
import xmltodict


def convert_file_to_json(file_path):
    with open(file_path, 'r',encoding='utf-8') as file:
        data = file.read()

    json_data = xmltodict.parse(data)

    return json_data

