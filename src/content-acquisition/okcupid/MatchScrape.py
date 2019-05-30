from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from requests import get
from bs4 import BeautifulSoup

url="https://www.okcupid.com/login"


username = 'aj.goldfish@gmail.com'
password = 'rInwu9-giqvaw-viqnin'

driver = webdriver.Chrome("chromedriver")

driver.get(url)
User = driver.find_element_by_name('username')
User.clear()
User.send_keys(username)

Pass = driver.find_element_by_name('password')
Pass.clear()
Pass.send_keys(password)

time.sleep(2)

form = driver.find_element_by_xpath("//input[@type='submit']")
form.submit()

time.sleep(2)
driver.get('https://www.okcupid.com/match')

page = driver.page_source
html_soup = BeautifulSoup(page, 'html.parser')

matches = html_soup.find_all('a',class_ = 'match-results-card')
print(matches[0])
data_dict = {}
for i in range(0,len(matches)):
    data_dict[i] = {}
    temp = matches[i].find('span', class_ = 'userInfo-username-name').text.split(',')
    data_dict[i]['name'] = temp[0]
    data_dict[i]['age'] = temp[1]
    temp = matches[i].find('span',class_='userInfo-meta-location').text
    data_dict[i]['location'] = temp
    # temp = matches[i].find('div', class_ = 'match-info-percentage match-info-percentage--oval').text
    # data_dict[i]['match_per'] = temp
    """The commented code is the buggy bit. Still working on it"""
print(data_dict[0])
