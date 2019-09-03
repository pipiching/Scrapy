import requests
from bs4 import BeautifulSoup as bs
import re

## 驗證
rs = requests.Session()
payload ={
    "from" : "/bbs/Beauty/index.html",
    "yes" : "yes"
}
res = rs.post('https://www.ptt.cc/ask/over18',  data=payload)

img = []  #圖片網址
name = input('請輸入人名 : ')
sheets = eval(input('請輸入張數 : '))
url = 'https://www.ptt.cc/bbs/Beauty/index.html'

while len(img) < sheets:     
    
    res = rs.get(url)
    soup_out = bs(res.text, 'html.parser')
    titles = soup_out.select('div.title a')
    page = soup_out.select('div.btn-group.btn-group-paging a')
    
    for i in titles:
        if name in i.text:
            titleUrl = 'https://www.ptt.cc' + i['href']
            res_in = rs.get(titleUrl)
            soup_in = bs(res_in.text, 'html.parser')
            images = soup_in.find_all('a', href=re.compile('^https://i.imgur'))

            for k in images:    
                pic = k['href']
                image = requests.get(pic)
                img.append(pic)
                
                if len(img) == sheets + 1:
                    break
                with open(str(len(img)) + pic[-4:], 'wb') as file:    
                    for l in image:
                        file.write(l)
        if len(img) == sheets:
            break
    
    url = 'https://www.ptt.cc' + page[1]['href']  # 換頁
    
    
