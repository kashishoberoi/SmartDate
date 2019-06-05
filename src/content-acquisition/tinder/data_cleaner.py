import os, json
import pandas as pd
import re
import emoji,regex #to extract all emojis
import preprocessor as p
import yaml

def extract_emojis(text):
	emoji_list = []
	flags = regex.findall(u'[\U0001F1E6-\U0001F1FF]', text)
	for c in text:
		if c in emoji.UNICODE_EMOJI:
			emoji_list.append(c)
	return emoji_list + flags 

def strip_emoji(text):
	RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
	return RE_EMOJI.sub(r'', text)


if __name__ == '__main__':
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
						profile['bio']=re.sub(r'\n+','. ',profile['bio'])#replace \n with .
						profile['bio']=re.sub(r'[?!]+','. ',profile['bio'])#replace ?,! and their combinations with .
						profile['bio']=re.sub(r'[.]+','.',profile['bio'])#remove multiple full stops
						emojis = extract_emojis(profile['bio']) #to create a list of emojis
						profile['bio'] = p.clean(profile['bio']) #preprocessor to remove the basic redundancies
						profile['bio'] = strip_emoji(profile['bio']) #to remove the newer emojis
						profile['emojis'] = emojis #append emojis as a separate key

					#dumping the cleaned json into a new file
					path_to_cleaned_json= cfg['cleaned_output'] + ""
					if not os.path.exists(path_to_cleaned_json+place+""):
						os.mkdir(path_to_cleaned_json+place)
					with open(path_to_cleaned_json+place+'/'+curr_file, 'w') as fp:
						sjson.dump(data, fp)


