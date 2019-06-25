import os, json
import pandas as pd
import re
import emoji,regex #to extract all emojis
import yaml
import spacy
import json
import preprocessor as p
import unicodedata2 as UC

def textcleaner(text):
    text=re.sub(r' \n','\n',text)#remove redundant spaces before \n
    text=re.sub(r'\t+',' ',text)#remove \t 
    text=re.sub(r'\n+','. ',text)#replace \n with .
    text=re.sub(r'[?!]+','. ',text)#replace ?,! and their combinations with .
    text=re.sub(r'[.]+','.',text)#remove multiple full stops
    text = str(UC.normalize('NFKD', text).encode('ascii','ignore'))
    text = text[2:]
    text = text[:-1]
    return text

def clean(data_dict):
    list1 = data_dict.keys()
    for tag in list1:
        if(type(data_dict[tag])==type("abc")):
            data_dict[tag]=textcleaner(data_dict[tag])
        if(type(data_dict[tag])==type(dict())):
            list2 = data_dict[tag].keys()
            for tag2 in list2:
                data_dict[tag][tag2]=textcleaner(data_dict[tag][tag2])
    return data_dict

def dumpfile(data_dict,place):
    #dumping the cleaned json into a new file
	path_to_cleaned_json= cfg['cleaned_output'] + ""
	if not os.path.exists(path_to_cleaned_json+place+""):
		os.mkdir(path_to_cleaned_json+place)
	with open(path_to_cleaned_json+place+'/'+curr_file, 'w') as fp:
		json.dump(data_dict, fp)

if __name__ == '__main__':
    with open('../../../config/okcupid.yaml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

	#to read the raw data stored in "output"
    path_to_locations=cfg['output_folder']+""
    locations = [places for places in os.listdir(path_to_locations)]
    for place in locations:
        if(place != '.DS_Store'):
            path_to_json = path_to_locations+place
            json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
            for curr_file in json_files:
                print("file being used currently is ",curr_file)
                with open(path_to_json+'/'+curr_file) as json_data:
                    data_dict = json.load(json_data, strict=False)
                data_dict = clean(data_dict)
                dumpfile(data_dict,place)

					
