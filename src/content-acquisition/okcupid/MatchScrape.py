from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from requests import get
from bs4 import BeautifulSoup
import json
import os
from datetime import date

today = date.today().strftime("%d-%m-%Y")
if not os.path.exists("./"+today):
    os.makedirs("./"+today)

path = "./"+today

url="https://www.okcupid.com/login"


username = 'aj.goldfish@gmail.com'
password = 'rInwu9-giqvaw-viqnin'

driver = webdriver.Chrome("chromedriver")


print("Logging in!")
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

print("Matches please!")
url = "https://www.okcupid.com/match" 
driver.get(url)
reloads=100
pause=5
for i in range(reloads):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print(i)
    time.sleep(pause)
page = driver.page_source
html_soup = BeautifulSoup(page, 'html.parser')

print("Getting all matches...!")
matches = html_soup.find_all('a',class_ = 'match-results-card')
traverse_url = "https://www.okcupid.com"
print(len(matches))

for i in range(0,len(matches)):
    #empty json intialization
    data_dict = {}

    #jumping to profile and retrieving source
    next_profile_url = traverse_url + matches[i]['href']
    driver.get(next_profile_url)
    print("Entered profile", i)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')

    #retrieving Name, Age, Location and Match Percentage
    data_dict['name'] = soup.find('div', class_='userinfo2015-basics-username').text
    data_dict['age'] = soup.find('span',class_='userinfo2015-basics-asl-age').text
    data_dict['location'] = soup.find('span', class_ = 'userinfo2015-basics-asl-location').text
    match_parent = soup.find('span', class_ = 'userinfo2015-basics-asl-match')
    data_dict['match_per'] = match_parent.find('a').text

    #Initialising for category, question and answers
    category = []
    question = []
    answer = []

    #retrieving category, question and answers
    for cat in soup.find_all('h2', class_ = "profile-essay-category"):
        category.append(cat.text)
    for ques in soup.find_all('h2', class_ = "profile-essay-title"):
        question.append(ques.text)
    for ans in soup.find_all('p', class_ = "profile-essay-contents"):
        answer.append(ans.text)
    
    #appending to json in required format
    for j in range(0,len(category)):
        data_dict[category[j]] = {question[j]:answer[j]}
    
    #Side bar 
    items = soup.find_all('div',class_ = "matchprofile-details-text")
    print(items)
    data_dict['info'] = items[0].text
    data_dict['perferences'] = items[len(items)-1].text

    if(len(items)==4):
        data_dict['background'] = items[1].text+','+items[2].text
    elif(len(items)==3):
        data_dict['background'] = items[1].text
    
    #Back tracking to matches
    driver.get(url)
    print("Exited profile",i)
    with open(path+data_dict['name'].strip()+str(i)+'.json','w') as fp:
        json.dump(data_dict, fp)