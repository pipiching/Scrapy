import requests
from bs4 import BeautifulSoup as bs
import re

url = 'https://www.ptt.cc/bbs/Beauty/index.html'
title = []  #標題名稱
titleUrl = []   #標題網址
img = []  #圖片網址
input = ('請輸入關鍵字') 

while len(title) < 3:   #   三個標題

    res_out = requests.get(url)
    soup_out = bs(res_out.text, 'html.parser')
    titles = soup_out.select('div.title a')
    page = soup_out.select('div.btn-group.btn-group-paging a')
    
    for i in titles:
        if input in i.text:
            title.append(i.text)
            titleUrl.append('https://www.ptt.cc' + i['href'])
            
            if len(title) == 3:
                break
    
    url = 'https://www.ptt.cc' + page[1]['href']  # 換頁
 

for j in titleUrl:
    res_in = requests.get(j)
    soup_in = bs(res_in.text, 'html.parser')
    images = soup_in.find_all('a', href=re.compile('^https://i.imgur'))
    
    
    for k in images:
        
        pic = k['href']
        image = requests.get(pic)
        img.append(pic)
        
        with open(str(len(img)) + pic[-4:], 'wb') as file:
        
            for l in image:
                file.write(l)