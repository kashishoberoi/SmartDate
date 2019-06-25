import os, json
import pandas as pd
import re
import emoji,regexpip install tweet-preprocessor==0.4.0
import preprocessor as p
import yaml
import spacy

def clean():
	with open('../../../config/tinder.yaml', 'r') as ymlfile:
		cfg = yaml.load(ymlfile)

	#to read the raw data stored in "output"
	path_to_locations=cfg['output_folder']+""
	locations = [places for places in os.listdir(path_to_locations)]
	for place in locations:
		if(place != '.DS_Store'):
			path_to_json = path_to_locations+place
			json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
			print(json_files)  
			for curr_file in json_files:
				print("file being used currently is ",curr_file)
				with open(path_to_json+'/'+curr_file) as json_data:
					data = json.load(json_data, strict=False)
					#res = data['results']
					print("number of profiles in current file are",len(data['results']))
					for profile in data['results']:
						#print(profile['bio'])
						profile['bio']=re.sub(r' \n','\n',profile['bio'])#remove redundant spaces before \n
						profile['bio']=re.sub(r'\t+',' ',profile['bio'])#remove \t 
						profile['bio']=re.sub(r'\n+','. ',profile['bio'])#replace \n with .
						profile['bio']=re.sub(r'[?!]+','. ',profile['bio'])#replace ?,! and their combinations with .
						profile['bio']=re.sub(r'[.]+','.',profile['bio'])#remove multiple full stops
						emojis = extract_emojis(profile['bio']) #to create a list of emojis
						profile['bio'] = p.clean(profile['bio']) #preprocessor to remove the basic redundancies
						profile['bio'] = strip_emoji(profile['bio']) #to remove the newer emojis
						profile['emojis'] = emojis #append emojis as a separate key
						profile['sentences']= sentence_segmentor(profile['bio'])#add segmented sentences as a separate key
						
					#dumping the cleaned json into a new file
					path_to_cleaned_json= cfg['cleaned_output'] + ""
					if not os.path.exists(path_to_cleaned_json+place+""):
						os.mkdir(path_to_cleaned_json+place)
					with open(path_to_cleaned_json+place+'/'+curr_file, 'w') as fp:
						json.dump(data, fp)

if __name__ == '__main__':
	clean()
