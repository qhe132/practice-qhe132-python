import bs4
import requests
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import urllib.request
import os
import time

my_url = "http://www.qdaily.com/tags/1068.html"
url = "http://www.qdaily.com"
Client = uReq(my_url)
html_page = Client.read()
Client.close()

soup_page = soup(html_page,"html.parser")
news_list = soup_page.findAll("div",{"class":"pic imgcover"})
news_list_message = soup_page.findAll("span",{"class":"iconfont icon-message"})
news_list_heart = soup_page.findAll("span",{"class":"iconfont icon-heart"})
news_list_href = soup_page.findAll("div",{"class":"packery-item article size1x2"})
img = []
alt = []

for i in range(len(news_list)):
    img.append(news_list[i].img["data-src"])
    alt.append(news_list[i].img["alt"])
    print(news_list[i].img["alt"])
    print(news_list_message[i].text)
    print(news_list_heart[i].text)
    print(url+news_list_href[i].a["href"])
    print("*"*150)

path_dir = os.getcwd() + '/daily_img'
if not os.path.exists(path_dir):
    os.makedirs(path_dir)

counter = 0
for re_img in img:
    re = requests.get(re_img)
    time.sleep(3)
    with open(path_dir + '/' + alt[counter] + '.jpg','wb') as file:
        file.write(re.content)
    counter += 1
