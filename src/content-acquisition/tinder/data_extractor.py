import json
import random
import requests
import datetime
import time
import os, sys
import urllib.request
import yaml, pgeocode
from phone_auth_token import sendCode, getToken


def set_token():
    if get_self()['meta']['status'] == 401:
        print("TOKEN EXPIRED \n")
        phone_number = cfg['phone_number']
        log_code = sendCode(phone_number)
        otp = input("ENTER OTP: ")
        getToken(phone_number, otp, log_code)
        log_code = sendCode(phone_number)
        sms_code = input("Please enter the code you've received by sms")
        print("Here is your Tinder token :" + str(getToken(phone_number, sms_code, log_code)))

def create_directory():
    #create loacation,image,date folder
    l = [cfg['city'],"images",date]
    path = cfg['output_folder']
    for i in range(3):
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


def swipe(profiles):
    global temp_dict
    global rcounter

    rightswipe = set()
    for i in range(random.randint(0,5)): #level 1 of randomness(0-5 swipes)
        rightswipe.add(random.randint(0,len(profiles)))  #level 2 of randomness(profile no 0-22)

    rightswipe = list(rightswipe)
    for index, user in enumerate(profiles):
        try:
            if index in rightswipe and rcounter < cfg['right_swipes']:
                url = cfg['host'] + '/like/%s' % user['_id']
                r = requests.get(url, headers=headers)
                rcounter+=1
                temp_dict['last_swipe_count'] +=1
                print(user['_id'], "swiped right")
            else:
                url = cfg['host'] + '/pass/%s' % user['_id']
                r = requests.get(url, headers=headers)
                print(user['_id'], "swiped left")
                time.sleep(random.uniform(0.3,2))
            except requests.exceptions.RequestException as e:
                print(e)

def extract_images(profiles):
    for profile in profiles:
        count = 1
        _id = profile['_id']
        path = image_path+'/'+_id
        if not os.path.exists(path):
            os.mkdir(path);
        for photo in profile['photos']:
            filename = path+'/%d.jpg'%count
            url = photo['processedFiles'][0]['url']
            urllib.request.urlretrieve(url, filename)
            count+=1

def export_results(dump):
    with open("%s.json" % op_file_path, 'w+') as fp:
        json.dump(dump, fp) 

def get_extractions():
    global temp_dict
    global rcounter
    # set preferences
    # checking if the script is being run for the first time during the day(file exists or not)
    file_exists = os.path.isfile("%s.json" % op_file_path)
    if not file_exists:
        #get source profile location
        coordinates = get_self()['pos_info']
        temp_dict['position'] = coordinates

    else:
        with open("%s.json" % op_file_path) as fp:
            temp_dict = json.load(fp)

    while(rcounter<cfg['right_swipes'] and temp_dict['last_swipe_count']+rcounter<=90):
        try:
            rec = get_recommendations()
            print("got", len(rec['results']), "profiles")
            temp_dict['results'] = temp_dict['results'] + rec['results']
            swipe(rec['results'])
            print("### Image extraction started ###")
            extract_images(rec['results'])
            time.sleep(random.randint(120,180))
        except KeyboardInterrupt:
            export_results(temp_dict)

    export_results(temp_dict)
    print(len(temp_dict['results']),"profiles done")

if __name__ == '__main__':
    date = str(datetime.date.today())
    with open('../../../config/tinder.yaml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    
    main_path = cfg['output_folder']+cfg['city']
    op_file_path = main_path+'/'+date
    image_path = main_path+"/images/"+date

    temp_dict = {
        "name" : cfg['name'],
        "city" : cfg['city'],
        "position" : {},
        "date" : date,
        "last_swipe_count" : 0,
        "results" : []

    }
    rcounter = 0
    headers = {
        'app_version': str(cfg['app_version']),
        'platform': cfg['platform'],
        "content-type": "application/json",
        "User-agent": cfg['User_agent'],
        "X-Auth-Token": cfg['tinder_token'],
    }
    set_token()
    create_directory()
    update_location()
    change_preferences(age_filter_min=cfg['min_age'], age_filter_max=cfg['max_age'],  gender_filter = cfg['gender_filter'], gender = cfg['gender'])
    get_extractions()
