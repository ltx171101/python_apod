#20210904 1237
#20210904 2145
import requests
import re
from urllib.request import urlretrieve
from multiprocessing import Pool
import time
from bs4 import BeautifulSoup
import csv

path ='E://Python/mydatas/APOD/'
url_main = 'https://apod.nasa.gov/apod/archivepixFull.html'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
head_url = 'https://apod.nasa.gov/apod/'

#--------------------------------------------------------
#--------------------------------------------------------
def download(url):
    res = requests.get(head_url+url,headers = header)
    if(res.status_code != 200):
        return
    else:
        res.encoding = res.apparent_encoding
        #正则表达式
        #根据HTML文件不同情况来添加
        #暂时不能处理需要翻墙的情况
        img_url = re.findall('<a href="(.*?)">\n<IMG SRC="',res.text)
        if (img_url==[]):
            img_url = re.findall('<a href="(.*?)">\n<img src="',res.text)
        if (img_url == []):
            img_url = re.findall('<a href="(.*?)"\nonMouseOver="',res.text)
        if (img_url == []):
            img_url = re.findall('<IMG SRC="(.*?)"',res.text)
        if (img_url == []):
            #向文件中输入错误信息
            f = open(path+url+'.csv','w',encoding='UTF-8',newline='')
            csv_writer = csv.writer(f)
            csv_writer.writerow([url])
            f.close()
            print(url+'无法下载')
            return
        
        else:   
            name = url[:8] + img_url[0][len(img_url[0])-4:len(img_url[0])]
            urlretrieve(head_url+img_url[0],path+name)
            print(url+'下载完毕')
#--------------------------------------------------------
#--------------------------------------------------------    
if __name__ == '__main__':  
    print('正在获取链接……')
    res = requests.get(url_main,headers = header)

    print('主网页已经打开')
    son_urls = re.findall(':  <a href="(.*?)">',res.text)
    '''
    
    titles = re.findall('.html">(.*?)</a><br>',res.text)
    f = open(path+'aatitle.csv','w',encoding='UTF-8',newline='')
    csv_writer = csv.writer(f)
    for i in range(0,len(titles)):
       csv_writer.writerow([titles[i]])
    f.close()
    f = open(path+'aaurls.csv','w',encoding='UTF-8',newline='')
    csv_writer = csv.writer(f)
    for i in range(0,len(son_urls)):
       csv_writer.writerow([son_urls[i]])
    f.close()
    '''
    groups = []
           
    print('已经获取{}个子网页url，前五项为：'.format(len(son_urls)))

    for i in range(0,5):
            strbuff = '%d\t'+son_urls[i]
            print(strbuff % (i+1))
            
    while(1):
        first = int(input('从哪个文件开始下载（顺序号）：'))
        last  = int(input('到哪个文件结束下载（顺序号）：'))
        print('请确认要下载的文件\n')
        
        if(last-first<=10):
            for i in range(first-1,last):
                strbuff = '%d\t'+son_urls[i]
                print(strbuff % (i+1))
        else:
            for i in range(first-1,first+5):
                strbuff = '%d\t'+son_urls[i]
                print(strbuff % (i+1))
            print('……\t……')
            for i in range(last-5,last):
                strbuff = '%d\t'+son_urls[i]
                print(strbuff % (i+1))
        YN = input('是否下载 Y/N：')
        if(YN == 'Y'):
            break       
    pools = int(input('请输入进程数：'))
        
    for i in range(first-1,last):
            groups.append(son_urls[i])

            
        
    pool = Pool(processes = pools)    
    start1 = time.time()
    print('开始下载')
    pool.map(download,groups)
    end1 = time.time()
    print('下载完毕，耗时{:.1f}秒'.format(end1-start1))
#单进程
#    for url in groups:
#        start1 = time.time()
#        download(url)
#        end1 = time.time()
#        print('下载完毕，耗时{:.1f}秒'.format(i+1,end1-start1))
