from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

#PChome_Url = 'https://shopping.pchome.com.tw/'
#Yahoo_Url = 'https://tw.bid.yahoo.com/'
Shopee_Url = 'https://shopee.tw/'
#PCprices = []
#PCtitles = []
#YAprices = []
#YAtitles = []
SHprices = []
SHtitles = []

#options = webdriver.ChromeOptions()
#options.add_argument('--headless')
keyword = '五月花衛生紙'#input('請輸入要查詢的商品: ')
driver = webdriver.Chrome()

###########  PCHOME  ###########

#driver.get(PChome_Url)
#element = driver.find_element_by_id('keyword')
#element.send_keys(keyword)
#driver.find_element_by_id('doSearch').click()
#sleep(2)
#
#PC_text = driver.page_source
#
#PC_soup = bs(PC_text, 'html.parser')
#PCtitle = PC_soup.find_all('img', src = re.compile('.jpg'))
#for k in PCtitle:
#    PCtitles.append(k['title'])
#
#PCprice = soup.find_all(class_='value', id=re.compile('^price'))
#for i in PCprice:
#    PCprices.append(i.text)
#
#PC_df = pd.DataFrame(columns = ['PC_titles', 'PC_prices'])
#PC_df['PC_titles'] = PCtitles
#PC_df['PC_prices'] = PCprices  

###########  YAHOO  ###########

#driver.get(Yahoo_Url)
#element = driver.find_element_by_css_selector("suggest-module")
#shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
#inner = shadow_root.find_element_by_class_name("entry")
#inner.send_keys(keyword)
#
#element = driver.find_element_by_class_name('button')
#element.click()
#sleep(2)
#
#YA_text = driver.page_source
#
#YA_soup = bs(YA_text, 'html.parser')
#YAtitle = YA_soup.find_all(class_='BaseGridItem__title___2HWui')
#for k in YAtitle:
#    YAtitles.append(k.text)
#    
#YAprice = YA_soup.find_all('span', class_='BaseGridItem__price___31jkj')
#for i in YAprice:
#    YAprices.append(i.text)   
#    
#YA_df = pd.DataFrame(columns = ['Ya_titles', 'Ya_prices'])
#YA_df['Ya_titles'] = YAtitles
#YA_df['Ya_prices'] = YAprices

###########  SHOPEE  ###########

driver.get(Shopee_Url)
element = driver.find_element_by_class_name('shopee-searchbar-input__input')
element.send_keys(keyword)
submit = driver.find_element_by_xpath("//button[@type='button']").click()
sleep(2)
SH_text = driver.page_source

SH_soup = bs(SH_text, 'html.parser')

SH_ALL = SH_soup.find(class_='shopee-search-item-result__items')
SHtitle = SH_ALL.find_all('a')
for k in SHtitle:
    SHtitles.append(k['href'])
    
SHprice = SH_ALL.find_all('span')
for i in SHprice:
    SHprices.append(i.text)    
    
SH_df = pd.DataFrame(columns = ['SH_titles', 'SH_prices'])
SH_df['SH_titles'] = SHtitles
SH_df['SH_prices'] = SHprices

  