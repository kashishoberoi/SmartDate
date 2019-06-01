### Contain extractors for tinder
## Steps to get the extractor working :

<b>Requirements:</b> `pip install pgeocode`
> pgeocode helps in finding latitude, longitude from the given country code and pin code. We need to provide both the details in the `tinder.yaml` file to update our location.

### ACCESS-TOKEN GENERATION
To initiate the extractions, we need to get access-token which is active for 24 hrs. After it, we need to get a fesh access-token. To get access token run: `python3 phone_auth_token` . 
1. Provide phone number example, +919876543210, which would trigger an OTP on that number. After providing the correct OTP, an access-token will be returned which is valid for 24hrs.
2. Place this token in the config file as the value for 'tinder_token' (this token is valid for 24 hrs, repeat step 1 and 2 once the token expires)

### SETTING UP TINDER CONFIG
Fill in the other details in the configuration file as follows :
```
User_agent: Tinder/10.13.0 (iPhone; iOS 12.2.0; Scale/2.00)
app_version: 10.13.0
gender: 0
gender_filter: 1
host: https://api.gotinder.com
max_age: 25
min_age: 18
name: <your-name>
output_folder: '../../../output/'
ph_user_agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_5 like Mac OS X) AppleWebKit/604.5.6
  (KHTML, like Gecko) Mobile/15D60 AKiOSSDK/4.29.0
platform: ios
right_swipes: <total-right-swipe-to-do>
tinder_token: <your-access-token>
country_name: <country-code>
city: <city-name>
pincode: <area pin code>
backfill: False
backfill_folder: '../../../output/<city-name>/images/<dd-mm-yyyy>'
```
4. Create "output" folder in the "Smartdate" directory
6. Run data_extractor.py
