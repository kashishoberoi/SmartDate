### Contain extractors for tinder
## Steps to get the extractor working :
1. Run phone_auth_token.py . You'll be asked for your phone number at runtime, once you've entered the phone number you'll have to type in the code you received by SMS, and it will return your token. 
2. Place this token in the config file as the value for 'tinder_token' (this token is valid for 24 hrs, repeat step 1 and 2 once the token expires)
3. Fill in the other details in the configuration file as follows :

```
User_agent: Tinder/10.13.0 (iPhone; iOS 12.2.0; Scale/2.00)  #tinder/<app version> (<phone model>; <os> <os_version>; Scale/2.00)
app_version: 10.13.0  #enter your tinder app version
city: Doha  #City at which you're extracting data
gender: 0 #your gende
gender_filter: 1  #gender you're seeking for
host: https://api.gotinder.com
max_age: 30 #max age preference
min_age: 18 #min age preference
name: Pallavi #your name
output_folder: '../../../output/' #path to the output folder where the data will be stored
ph_user_agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6
  (KHTML, like Gecko) Mobile/15D60 AKiOSSDK/4.29.0 #do not edit this field
platform: ios #your mobile os
right_swipes: 1 #number of right swipes you would like to make
tinder_token: be080cf1-0b27-4662-a34d-40c994987507 #token received after running phone_auth_token.py

```
4. Create "output" folder in the "Smartdate" directory
5. Create "images" directory inside the "output" directory
6. Run data_extractor.py
