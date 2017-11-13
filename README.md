'''

    #拟在解决小说软件收费的问题。针对部分免费的小说软件存在广告的问题。
    
    #采用爬取盗版网站的小说，借用离线观看。
    
    #目前测试的是笔趣网的。

'''


python3版本	(改一改python2也可以用)

python book_spider.py	即可

'''

    拟在解决小说软件收费的问题。针对部分免费的小说软件存在广告的问题。
    采用爬取盗版网站的小说，借用离线观看。
    目前测试的是笔趣网的。

'''

import requests
from lxml import html
from lxml import etree
from chinese_to_int import *
import re
import threading
import time

path = "D:/小说爬虫"    ###文件路径
name = "火影之活久见"     ###文件姓名
url = "http://www.biqu.cm/28_28691/"        ##起始IP 
num = 20 ##线程数
header  = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"
}



def run():
    global path,name,url,header
    s = requests.get(url,headers=header)
    print(s)
    tree = html.fromstring(s.text)
    url_date = tree.xpath("//dd/a/@href")
    url_title = change_to_GBK(tree.xpath("//dd/a/text()"))      ###
    page_title = sort_title(url_title,url_date)         ###去除无关的单章 并将汉字转为阿拉伯数字排序，可以兼容卷的问题

    for x in range(len(url_date)):
        if url_date[x] != -1:
            url = "http://www.biqu.cm"+url_date[x]
            page = page_title[x]
            t = threading.Thread(target = deal,args=[url,page])
            t.start()
        if x % num == 0:
            time.sleep(0.1)
    print(merge_txt(path,name))     ###将分散的TXT单章合并

def deal(url,page):
    global path,name,header
    s = requests.get(url,headers=header)
    tree = etree.HTML(s.text.encode('latin-1').decode('GBK'))
    title = tree.xpath("//h1/text()")
    message = tree.xpath("//div[@id='content']/text()")
    message[0] ='\n'+message[0]         ###增加标题和正文的换行
    for y in range(len(message)):
        message[y] = message[y].replace("\xa0\xa0\xa0\xa0","")
    print("开始写入"+str(page)+"章"+title[0])
    with open('{0}/{1}/{2}.txt'.format(path,name,str(page)), 'w' ,encoding='utf-8') as f:
        f.write(title[0])
        for line in message:
            f.write(line)
    print("完成写入")




if __name__  == "__main__":
    run()