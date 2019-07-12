import json
import random
import requests
import datetime
import time
import os, sys
import urllib.request
import yaml, pgeocode

def create_directory():
    #create loacation,image,date folder
    l = ['output','tinder',cfg['city'],"images",date]
    # path = cfg['output_folder']
    path = '../../..'
    for i in range(5):
        path = path+'/'+l[i]
        if not os.path.exists(path):
            os.mkdir(path)

def get_self():
    url = cfg['host'] + '/profile'
    try:
        r = requests.get(url, headers=headers)
        return r.json()
    except requests.exceptions.RequestException as e:
        print(e)

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
    except requests.exceptions.RequestException as e:
        print(e)

def get_geolocation(cn, pincode):
    nomi = pgeocode.Nominatim(cn)
    res = dict(nomi.query_postal_code(pincode))
    lat = res['latitude']
    lon = res['longitude']
    return lat, lon

def update_location():
    '''
    Updates your location to the given latitude and longitude - cannot call the API multiple times at one go. Give a 20-25 mins gap between calls.
    '''
    lat, lon = get_geolocation(cfg['country_name'], cfg['pincode'])
    try:
        url = cfg['host'] + '/user/ping'
        r = requests.post(url, headers=headers, data=json.dumps({"lat": lat, "lon": lon}))
    except requests.exceptions.RequestException as e:
        print(e)

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


def swipe(profiles, rcounter):
    last_swipe_count = 0
    rightswipe = set()
    for i in range(random.randint(0,3)): #level 1 of randomness(0-5 swipes)
        rightswipe.add(random.randint(0,len(profiles)))  #level 2 of randomness(profile no 0-22)

    rightswipe = list(rightswipe)
    for index, user in enumerate(profiles):
        try:
            if index in rightswipe and rcounter < cfg['right_swipes']:
                url = cfg['host'] + '/like/%s' % user['_id']
                r = requests.get(url, headers=headers)
                rcounter+=1
                last_swipe_count +=1
                print(user['_id'], "swiped right")
            else:
                url = cfg['host'] + '/pass/%s' % user['_id']
                r = requests.get(url, headers=headers)
                print(user['_id'], "swiped left")
        except requests.exceptions.RequestException as e:
            print(e)
    return last_swipe_count, rcounter

def extract_images(profiles):
    if cfg['gender_filter']==1:
        gender = "_female"
    else:
        gender = "_male"
    for profile in profiles:
        count = 1
        _id = profile['_id']
        path = image_path+'/'+_id+gender
        if not os.path.exists(path):
            os.mkdir(path);
        for photo in profile['photos']:
            filename = path+'/%d.jpg'%count
            url = photo['processedFiles'][0]['url']
            try:
                urllib.request.urlretrieve(url, filename)
            except:
                pass
            count+=1

def export_results(dump,path):
    with open(path, 'w+') as fp:
        json.dump(dump, fp)

def import_results(path):
    with open(path) as fp:
        return json.load(fp)

def retrieve_lostdata(path, flag):
    print("## BACKFILL INITIATED ##")

    file = cfg['output_folder']+path.split('/')[4]+'/'+path.split('/')[-1]+'.json'
    try:
        temp_dict = import_results(file)
    except json.decoder.JSONDecodeError:
        temp_dict = {
        "name" : cfg['name'],
        "city" : cfg['city'],
        "position" : {},
        "date" : date,
        "last_swipe_count" : 0,
        "results" : []
        }
    
    if flag is True:
            temp_dict['results'] = []
        
    _ids = list(map(lambda d: d['_id'], temp_dict['results']))
    for num, folder in enumerate(os.listdir(path)):
        _id = folder.split('_')[0]
        if flag is False and _id in _ids:
            print("ID already present", _id)
            continue

        print(num, "BACKFILL ID: ", _id)
        url = cfg['host'] + '/user/%s' % _id
        rec = requests.get(url, headers=headers)
        if rec.status_code == 401:
            print("TOKEN EXPIRED")
        try:
            if rec.status_code == 200:
                temp_dict['results'].append(rec.json()['results'])
        except KeyboardInterrupt:

            export_results(temp_dict,file) 

            break

    export_results(temp_dict,file)
    print("## BACKFILL COMPLETE ##")

def get_extractions():
    # set preferences
    # checking if the script is being run for the first time during the day(file exists or not)
    rcounter = 0
    file_exists = os.path.isfile("%s.json" % op_file_path)
    if not file_exists:
        #get source profile location
        temp_dict = {
        "name" : cfg['name'],
        "city" : cfg['city'],
        "position" : {},
        "date" : date,
        "last_swipe_count" : 0,
        "results" : []

        }
        coordinates = get_self()['pos_info']
        temp_dict['position'] = coordinates
        # export_results(temp_dict,"%s.json" % op_file_path)

    else:
        temp_dict = import_results("%s.json" % op_file_path)
    while(rcounter<cfg['right_swipes'] and temp_dict['last_swipe_count']+rcounter<=90):
        try:
            print("### Image and text extraction started ###")
            rec = get_recommendations()
            print("got", len(rec['results']), "profiles")
            temp_dict['results'] = temp_dict['results'] + rec['results']
            export_results(temp_dict,"%s.json" % op_file_path)
            last_swipe_count, rcounter = swipe(rec['results'], rcounter)
            temp_dict['last_swipe_count']+=last_swipe_count
            extract_images(rec['results'])
        except KeyboardInterrupt:
            break

    export_results(temp_dict,"%s.json" % op_file_path)
    print(len(temp_dict['results']),"profiles done")

if __name__ == '__main__':
    date = str(datetime.date.today())
    with open('../../../config/tinder.yaml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    main_path = cfg['output_folder']+'/tinder/'+cfg['city']
    op_file_path = main_path+'/'+date
    image_path = main_path+"/images/"+date
    headers = {
        'app_version': str(cfg['app_version']),
        'platform': cfg['platform'],
        "content-type": "application/json",
        "User-agent": cfg['User_agent'],
        "X-Auth-Token": cfg['tinder_token'],
    }
    if cfg['backfill']:
        retrieve_lostdata(cfg['backfill_folder'], cfg['backfill_force'])
    else:
        create_directory()
        update_location()
        change_preferences(age_filter_min=cfg['min_age'], age_filter_max=cfg['max_age'],  gender_filter = cfg['gender_filter'], gender = cfg['gender'])
        get_extractions()
