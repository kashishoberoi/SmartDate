import json
import random
import requests
import datetime
import time
import os
import yaml

date = str(datetime.date.today())

conf_path = os.path.relpath('../../../config/tinder.yaml', os.getcwd())
with open(conf_path, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

file_name = cfg['city']+"_"+date
op_file_path = cfg['output_folder']+file_name


rcounter = 0

headers = {
    'app_version': str(cfg['app_version']),
    'platform': cfg['platform'],
    "content-type": "application/json",
    "User-agent": cfg['User_agent'],
	"X-Auth-Token": cfg['tinder_token'],
}


temp_dict = {
    "name" : cfg['name'],
    "city" : cfg['city'],
    "position" : {},
    "date" : date,
    "last_swipe_count" : 0,
    "results" : []

}

def get_self():
    url = cfg['host'] + '/profile'
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not get your data:", e)

def change_preferences(**kwargs):
    '''
    ex: change_preferences(age_filter_min=30, gender=0)
    kwargs: a dictionary - whose keys become separate keyword arguments and the values become values of these arguments
    age_filter_min: 18..46
    age_filter_max: 22..55
    age_filter_min <= age_filter_max - 4
    gender: 0 == seeking males, 1 == seeking females
    distance_filter: 1..100
    discoverable: true | false
    {"photo_optimizer_enabled":false}
    '''
    try:
        url = cfg['host'] + '/profile'
        r = requests.post(url, headers=headers, data=json.dumps(kwargs))
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not change your preferences:", e)


def get_recommendations():
    '''
    Returns a list of users that you can swipe on
    '''
    url = cfg['host']+'/user/recs'
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Something went wrong with getting recomendations:", e)


def swipe(db):
    
    global temp_dict
    global rcounter

    rightswipe = []
    for i in range(random.randint(0,5)): #level 1 of randomness(0-5 swipes)
        rightswipe.append(random.randint(0,len(db['results'])))  #level 2 of randomness(profile no 0-22)

    for i in range(0,len(db['results'])):
        id = db["results"][i]['_id']
        url = cfg['host'] + '/like/%s' % id

        if i in rightswipe and rcounter<cfg['right_swipes']:
            try:
                r = requests.get(url, headers=headers)
                rcounter+=1
                temp_dict['last_swipe_count'] +=1
                print(id, "swiped right")
                

                time.sleep(random.randint(3,5))
            except requests.exceptions.RequestException as e:
                print("Something went wrong with swiping right:", e)

        else:
            try:
                r = requests.get(url, headers=headers)
                print(id, "swiped left")
                time.sleep(random.randint(3,5))
            except requests.exceptions.RequestException as e:
                print("Something went wrong with swiping left:", e)




def main():

    global temp_dict
    global rcounter
# set preferences
    preferences = change_preferences(age_filter_min=cfg['min_age'], age_filter_max=cfg['max_age'],  gender_filter = cfg['gender_filter'], gender = cfg['gender'])



# checking if the script is being run for the first time during the day(file exists or not)

    for i in range(2):
        file_exists = os.path.isfile("%s.json" % op_file_path)
                
        if not file_exists:
            #get source profile location
            coordinates = get_self()['pos_info']
            temp_dict['position'] = coordinates
            #first set of recs
            r = get_recommendations()
            print("got", len(r['results']), "profiles")
            temp_dict['results'] = r['results']
            swipe(temp_dict)

            with open("%s.json" % op_file_path, 'w+') as fp:
                json.dump(temp_dict, fp)
            print(len(temp_dict['results']),"profiles done")

            with open("%s.json" % op_file_path) as fp:
                    temp_dict = json.load(fp)

        else:
            try:
                with open("%s.json" % op_file_path) as fp:
                    temp_dict = json.load(fp)

                while(rcounter<cfg['right_swipes'] and temp_dict['last_swipe_count']+rcounter<=90):
           
                    rec = get_recommendations()
                    print("got", len(rec['results']), "profiles")
                    swipe(rec)
                    temp_dict['results'].extend(rec['results'])

                    with open("%s.json" % op_file_path, 'w+') as fp:
                        json.dump(temp_dict, fp)

                    print(len(temp_dict['results']),"profiles done")
                    print("total right swipe count :", temp_dict['last_swipe_count'])
                    time.sleep(random.randint(180,300))

            except KeyboardInterrupt:
                with open("%s.json" % op_file_path, 'w+') as fp:
                    json.dump(temp_dict, fp)
            break

    



if __name__ == '__main__':
    main()
