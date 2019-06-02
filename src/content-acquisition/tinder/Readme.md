### Contain extractors for tinder
## Steps to get the extractor working :

<b>Requirements:</b> `pip install pgeocode`
> pgeocode helps in finding latitude, longitude from the given country code and pin code. We need to provide both the details in the `tinder.yaml` file to update our location.

#### ACCESS-TOKEN GENERATION
To initiate the extractions, we need to get access-token which is active for 24 hrs. After it, we need to get a fesh access-token. To get access token run: `python3 phone_auth_token` . 
1. Provide phone number example, +919876543210, which would trigger an OTP on that number. After providing the correct OTP, an access-token will be returned which is valid for 24hrs.
2. Place this token in the config file as the value for 'tinder_token' (this token is valid for 24 hrs, repeat step 1 and 2 once the token expires)

#### SETTING UP TINDER CONFIG
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
backfill_folder: '../../../output/<city-name>/images/<yyyy-mm-dd>'
```
* In gender- male:0, female:1. `gender_filter` means which gender extraction needs to be done
* max_age and min_age are age filters
* name, city are used as metadata in the extracted json file
* output_folder - is where the extractions are to be dumped
* right_swipes - total right swipes to do on profiles. Max 100 can be done in a day
* tinder_token - unique token recieved from `phone_auth_token.py`
* pincode - area in the city where the extractions need to be done
* backfill - if there is an error in extracting text data for 'some' city on 'some' date. Then by setting backfill: True, a run triggers extracting the missing profiles. Default set- False
* backfill_folder - directory path of the image folder where images are extracted but not the bios. For example: if for a date `2019-06-30`, profiles bios were not extracted for city `Sydney` then we would set `backfill_folder: ../../../output/Sydney/images/2019-06-30`
* country codes to use:
> Andorra (AD), Argentina (AR), American Samoa (AS), Austria (AT), Australia (AU), Åland Islands (AX), Bangladesh (BD), Belgium (BE), Bulgaria (BG), Bermuda (BM), Brazil (BR), Belarus (BY), Canada (CA), Switzerland (CH), Colombia (CO), Costa Rica (CR), Czechia (CZ), Germany (DE), Denmark (DK), Dominican Republic (DO), Algeria (DZ), Spain (ES), Finland (FI), Faroe Islands (FO), France (FR), United Kingdom of Great Britain and Northern Ireland (GB), French Guiana (GF), Guernsey (GG), Greenland (GL), Guadeloupe (GP), Guatemala (GT), Guam (GU), Croatia (HR), Hungary (HU), Ireland (IE), Isle of Man (IM), India (IN), Iceland (IS), Italy (IT), Jersey (JE), Japan (JP), Liechtenstein (LI), Sri Lanka (LK), Lithuania (LT), Luxembourg (LU), Latvia (LV), Monaco (MC), Republic of Moldova (MD), Marshall Islands (MH), The former Yugoslav Republic of Macedonia (MK), Northern Mariana Islands (MP), Martinique (MQ), Malta (MT), Mexico (MX), Malaysia (MY), New Caledonia (NC), Netherlands (NL), Norway (NO), New Zealand (NZ), Philippines (PH), Pakistan (PK), Poland (PL), Saint Pierre and Miquelon (PM), Puerto Rico (PR), Portugal (PT), Réunion (RE), Romania (RO), Russian Federation (RU), Sweden (SE), Slovenia (SI), Svalbard and Jan Mayen Islands (SJ), Slovakia (SK), San Marino (SM), Thailand (TH), Turkey (TR), Ukraine (UA), United States of America (US), Uruguay (UY), Holy See (VA), United States Virgin Islands (VI), Wallis and Futuna Islands (WF), Mayotte (YT), South Africa (ZA)

#### SET OUTPUT FOLDER FOR EXTRACTIONS
Create "output" folder in the "Smartdate" directory

#### INITIATE EXTRACTIONS
Run: `data_extractor.py`
