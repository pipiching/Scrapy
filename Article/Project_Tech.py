import requests
from bs4 import BeautifulSoup as bs
import threading
import queue
#import pyodbc



def Main_Tech(n, semaphore, queue):
    url = 'https://technews.tw/'
        
    res = requests.get(url, headers=headers)
    soup = bs(res.text, 'html.parser')
    title = soup.find(class_='nav-menu').next_element
    li = [title]
    for i in title.next_siblings:
        if i != '\n':
            li.append(i)
    del li[-3:]    
    
    for i in range(len(li)):
        li[i] = li[i].next['href'] # 各大分類的網址
        
    li[5] = 'https:' + li[5]
    threads_1 = []
    for i in range(len(li)):
        threads_1.append(threading.Thread(target=Get_titles, args=(li[i], n, queue, semaphore)))
        threads_1[i].start()      
    
    for i in range(len(threads_1)):
        threads_1[i].join()
            
def Get_titles(url, n, queue, semaphore):
    print(url, ' start')
    global counts
    
    while url:
        if counts > n:
            return        
        res = requests.get(url, headers=headers)
        soup = bs(res.text, 'html.parser')
        titles = soup.select('article h1 a') #取得各文章tag及連結
        
        threads_2 = []  
        for i in range(len(titles)):
            threads_2.append(threading.Thread(target=Get_String, args=(titles[i]['href'], n, queue, semaphore)))
            threads_2[i].start() 
        for i in range(len(threads_2)):
            threads_2[i].join()

        url = Next_page(soup)


def Get_String(url, n, queue, semaphore):
    global counts        
    semaphore.acquire()
    if counts > n:
        semaphore.release()
        return     
    res = requests.get(url, headers=headers)
    soup = bs(res.text, 'html.parser')
    
    cla = soup.select('span.body a') #取得文章分類
    content = soup.select('p')[:-11] #取得文章內容
    
#    del cla[0]
#    del cla[-1]
#    for i in range(len(cla)):
#        cla[i] = cla[i].text
    cla = cla[1].text

    string = ''
    for text in content:
        if text.text:
            string += text.text
    queue.put([cla, url, string])
    counts += 1
    print('完成{}篇'.format(counts))
    semaphore.release()    

def Next_page(soup):
    titles = soup.select('div.pagination a')
    for i in titles:
        if '下一頁' in i.text:
            next_url = i['href']
            return next_url
    return None

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
counts = 0
my_queue = queue.Queue()
semaphore = threading.Semaphore(10)
Main_Tech(100, semaphore, my_queue)

