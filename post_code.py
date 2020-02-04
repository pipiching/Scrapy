import requests
from bs4 import BeautifulSoup as bs
from PIL import Image   #, ImageFilter, ImageEnhance
import pytesseract

############### 存取圖片 ###############

url = 'https://www.post.gov.tw/post/internet/Postal/index.jsp?ID=208'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
res = requests.get(url, headers=headers)
soup = bs(res.text, 'html.parser')

images = soup.find('img', id='imgCaptcha3')
 
url_images = 'https://www.post.gov.tw/post/internet' + images['src'][2:]
img = requests.get(url_images, headers=headers)

with open('test.jpg', 'wb') as file:
    for i in img:
        file.write(i)
        
############### 辨識圖片驗證碼 ###############
 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'       
pic = Image.open('test.jpg')

checkImange = pytesseract.image_to_string(pic, config='--psm 7')


############### 得到郵遞區碼 ###############

list_=soup.find('input', attrs={'name':'list'})['value']
list_type=soup.find('input', attrs={'name':'list_type'})['value']
firstView=soup.find('input', attrs={'name':'firstView'})['value']
vKey=soup.find('input', attrs={'name':'vKey'})['value']

payload = {
            'list':list_,
            'list_type':list_type,
            'firstView':firstView,
            'vKey':vKey,
            'city':'城市',
            'cityarea':'區域',
            'street':'路',
            'checkImange':checkImange,
            'Submit':'查詢'
           }
resp = requests.post(url, data = payload, headers=headers)
soup2 = bs(resp.text, 'html.parser')
postnumber = soup2.find('td', align='center')
print(postnumber.text)



        
