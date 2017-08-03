import urllib.request
import bs4
from bs4 import BeautifulSoup as soup
import json
import requests
import time
import os

url = "https://www.google.com/search?site=imghp&tbm=isch&sa=1&q="
pic = input()
pic = urllib.request.quote(pic)
my_url = url + pic
usr_agent = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
        }

request = urllib.request.Request(my_url,headers = usr_agent)
Client = urllib.request.urlopen(request)
html_page = Client.read()
Client.close()

images = []
soup_page = soup(html_page,"html.parser")
results = soup_page.findAll("div",{"class":"rg_meta"})

for re in results:
    link = json.loads(re.text)["ou"]
    images.append(link)

counter = 1

path_dir = os.getcwd()+'/'+urllib.request.unquote(pic)
if not os.path.exists(path_dir):
    os.makedirs(path_dir)

for re in images:
    rs = requests.get(re)
    time.sleep(3)
    with open(path_dir+'/'+str(counter)+'.jpg','wb') as file:
        file.write(rs.content)
        counter += 1
    if counter > 70:
        break
