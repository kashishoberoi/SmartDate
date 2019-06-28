### Contains scrapers for okcupid

###Pre Requisites:
1. Install required libraries
  pip install selenium
  pip install bs4
  pip install PIL
3. Install ChromeDriver ( Refer http://chromedriver.chromium.org/getting-started for help )

###Writing onto the config file
```
User_agent: okCupid
city: Type in City
host: https://www.okcupid.com/login
url_match: https://www.okcupid.com/match
url_traverse: https://www.okcupid.com
chromedriver_path: chromedriver
name: Your Name
username: Type Username
password: Type Passward
output_folder: "../../../output/okcupid/"
pincode: Pin Code
country_name: Country name
backfill: False
backfill_folder: '../../../output/images/okcupid/'
reloads: Number of scrolls (Suggested 100)
pause: Pause seconds (suggested 5)
cleaned_output: '../../../output/okcupid/cleaned'
```
###Running The Code
Navigate to src/content-acquisition/okcupid
python MatchScrape.py
