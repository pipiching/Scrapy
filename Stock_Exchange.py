import requests
from bs4 import BeautifulSoup as bs
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import re

############### 存取圖片 ###############
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

for count in range(10):  
    url = 'http://bsr.twse.com.tw/bshtm/bsMenu.aspx'
    res = requests.get(url, headers=headers)
    soup = bs(res.text, 'html.parser')
    img = soup.find_all('img')[1]
    
    imgUrl = 'http://bsr.twse.com.tw/bshtm/' + img['src']
    picRes = requests.get(imgUrl, headers=headers)
    fileName = 'test.jpg'
    
    with open(fileName, 'wb') as file:
        for i in picRes:
            file.write(i)
      
    ############### 處理圖片 ###############
            
    pic = Image.open('test.jpg')
    
    pic = pic.filter(ImageFilter.BLUR)
    pic = pic.filter(ImageFilter.BLUR)
    pic = pic.convert('L')
    pic = ImageEnhance.Contrast(pic)
    pic = pic.enhance(5.0)
        
    pixdata = pic.load()
    
    for x in range(pic.size[0]):
        for y in range(pic.size[1]):
            if pixdata[x, y] != (255):
                pixdata[x, y] = (0)
    
    pic.save('try.jpg')          
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    checkImange = pytesseract.image_to_string(pic, config='--psm 7')
    
    ############### 爬取資料 ###############
    
    EVENTTARGET = soup.select_one('#__EVENTTARGET')['value']
    EVENTARGUMENT = soup.select_one('#__EVENTARGUMENT')['value']
    LASTFOCUS = soup.select_one('#__LASTFOCUS')['value']
    VIEWSTATE = soup.select_one('#__VIEWSTATE')['value']
    VIEWSTATEGENERATOR = soup.select_one('#__VIEWSTATEGENERATOR')['value']
    EVENTVALIDATION = soup.select_one('#__EVENTVALIDATION')['value']
    RadioButton_Normal = soup.select_one('#RadioButton_Normal')['value']
    
    payload={
                '__EVENTTARGET':EVENTTARGET,
                '__EVENTARGUMENT':EVENTARGUMENT,
                '__LASTFOCUS':LASTFOCUS,
                '__VIEWSTATE':VIEWSTATE,
                '__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR,
                '__EVENTVALIDATION':EVENTVALIDATION,
                'RadioButton_Normal':RadioButton_Normal,
                'TextBox_Stkno': '2305',
                'CaptchaControl1':checkImange,
                'btnOK':'查詢'
            }
    rs = requests.session()
    newRes = rs.post(url, headers=headers, data = payload)
    newRes = rs.get('https://bsr.twse.com.tw/bshtm/bsContent.aspx?v=t')
    newSoup = bs(newRes.text, 'html.parser')
    point = newSoup.find_all(class_=re.compile('^price'))
    if len(point) == 4:
        print('辨識次數:', count)
        break
    
print('開盤價: ', point[0].text)
print('最高價: ', point[1].text)
print('最低價: ', point[2].text)
print('收盤價: ', point[3].text)





