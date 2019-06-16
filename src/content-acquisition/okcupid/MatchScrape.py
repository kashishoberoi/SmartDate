from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from requests import get
from bs4 import BeautifulSoup
import json
import os
from datetime import date
import urllib.request 
import yaml
from PIL import Image
import imghdr
import random

def download_img(image_url,image_name,path):
    urllib.request.urlretrieve(image_url, path+'/'+image_name)

def create_dir(output_folder,backfill):
    today = date.today().strftime("%d-%m-%Y")
    path = output_folder+today
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(backfill+today):
        os.makedirs(backfill+today)
    return path,backfill+today

def login(username,password,driver):
    print("Logging in!")
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

def scrolling(reloads, pause, driver):
    for i in range(reloads):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(pause)
    page = driver.page_source
    html_soup = BeautifulSoup(page, 'html.parser')
    return html_soup

def retreive_source(count,driver,matches,traverse_url):    
    next_profile_url = traverse_url + matches[count]['href']
    driver.get(next_profile_url)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    return src,soup

def retreive_data(count,driver,data_dict,soup,likes,matches):
    data_dict['name'] = soup.find('div', class_='userinfo2015-basics-username').text
    data_dict['age'] = soup.find('span',class_='userinfo2015-basics-asl-age').text
    data_dict['location'] = soup.find('span', class_ = 'userinfo2015-basics-asl-location').text
    match_parent = soup.find('span', class_ = 'userinfo2015-basics-asl-match')
    data_dict['match_per'] = match_parent.find('a').text
    category = []
    question = []
    answer = []
    for cat in soup.find_all('h2', class_ = "profile-essay-category"):
        category.append(cat.text)
    for ques in soup.find_all('h2', class_ = "profile-essay-title"):
        question.append(ques.text)
    for ans in soup.find_all('p', class_ = "profile-essay-contents"):
        answer.append(ans.text)
    if(not(len(category)==len(answer)==len(question))):
        length= min(len(category),len(question),len(answer))
    else:
        length=len(category)
    
    for j in range(0,length):
        data_dict[category[j]] = {question[j]:answer[j]}

    items = soup.find_all('div',class_ = "matchprofile-details-text")
    data_dict['info'] = items[0].text
    data_dict['perferences'] = items[len(items)-1].text

    if(len(items)==4):
        data_dict['background'] = items[1].text+','+items[2].text
    elif(len(items)==3):
        data_dict['background'] = items[1].text
    
    img = soup.find('img', class_='active')['src']
    img_filename=data_dict['name'].strip()+str(count)+'.webp'
    download_img(img,img_filename,path2)
    im_loc=path2+"/"+img_filename
    im = Image.open(im_loc).convert("RGB")
    im.save(path2+"/"+data_dict['name'].strip()+str(count)+'.jpg',"jpeg")
    os.remove(im_loc)

    pass_button = driver.find_element_by_css_selector('#pass-button')
    like_button = driver.find_element_by_css_selector('#like-button')
    if(random.random() and likes/len(matches) < 0.2):
        like_button.click()
        likes = likes+1
    else:
        pass_button.click()

    return data_dict,likes

def dumponfile(count,driver,data_dict,url):
    driver.get(url)
    with open(path1+'/'+data_dict['name'].strip()+str(count)+'.json','w') as fp:
        json.dump(data_dict, fp)

if __name__ == '__main__':
    with open('../../../config/okcupid.yaml', 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    path1,path2 = create_dir(cfg['output_folder'],cfg['backfill_folder'])

    url=cfg['host']
    username = cfg['username']
    password = cfg['password']
    driver = webdriver.Chrome(cfg['chromedriver_path'])
    driver.get(url)
    login(username,password,driver)

    print("Matches please!")
    url = cfg['url_match']
    driver.get(url)
    html_soup = scrolling(cfg['reloads'],cfg['pause'],driver)

    print("Getting all matches...!")
    matches = html_soup.find_all('a',class_ = 'match-results-card')
    traverse_url = cfg['url_traverse']
    likes=0
    for i in range(0,len(matches)):
        data_dict = {'collector':cfg['name'],'city':cfg['city'],'pincode':cfg['pincode'],'country':cfg['country_name']}
        src,soup= retreive_source(i,driver,matches,traverse_url)
        data_dict,likes = retreive_data(i,driver,data_dict,soup,likes,matches)
        dumponfile(i,driver,data_dict,url)

    driver.quit()
    print(len(matches),"New profiles Entered in output file \nExiting Code")