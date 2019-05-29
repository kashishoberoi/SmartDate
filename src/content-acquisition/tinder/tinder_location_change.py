# coding=utf-8
import json

import tinder_config_ex as config
import requests

headers = {
    'app_version': '6.9.4',
    'platform': 'ios',
    "content-type": "application/json",
    "User-agent": "Tinder Android Version 10.15.0",
	"X-Auth-Token": config.tinder_token,
}



#def get_recommendations():
    '''
    Returns a list of users that you can swipe on
    '''
 #   try:
  #      r = requests.get('https://api.gotinder.com/user/recs', headers=headers)
   #     return r.json()
    #except requests.exceptions.RequestException as e:
     #   print("Something went wrong with getting recomendations:", e)


def update_location(lat, lon):
    '''
    Updates your location to the given latitude and longitude - cannot call the API multiple times at one go. Give a 20-25 mins gap between calls.
    '''
    try:
        #url = config.host + '/passport/user/travel'
        url = config.host + '/user/ping'
        r = requests.post(url, headers=headers, data=json.dumps({"lat": lat, "lon": lon}))
        print(r.json())
    except requests.exceptions.RequestException as e:
        print("Something went wrong. Could not update your location:", e)

#def trending_gifs():
 #   try:
        #url = config.host + '/passport/user/travel'
  #      url = config.host + '/giphy/trending?limit={'+'10'+'}'
   #     r = requests.post(url, headers=headers, data=json.dumps({}))
    #    print(r.json())
    #except requests.exceptions.RequestException as e:
     #   print("Something went wrong. Could not find trending GIFs", e)

#add lat,long as parameters in below function call to change location
update_location(14.802231,74.435172)
#trending_gifs()
#get_recommendations()
