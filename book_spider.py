import requests
from lxml import html
from lxml import etree
from chinese_to_int import *
from send_to_qq import sendmail4
import re
import threading
import time
import traceback
from config import configs
from urllib import parse

path = configs['path']    ###文件路径
book_name = configs['book_name']     ###文件姓名
num = configs['num'] ##线程数
headers  = configs['headers']
proxies = configs['proxies']
message = configs['message']        ###邮件发送配置

if not os.path.exists(path+"/"+book_name):
    os.mkdir(path+"/"+book_name)

def search(book_name):
    book_name = parse.quote(book_name, encoding='gbk')
    data ="searchtype=articlename&searchkey={0}&action=login&submit=%26%23160%3B%CB%D1%26%23160%3B%26%23160%3B%CB%F7%26%23160%3B".format(book_name)
    url  = "http://www.biqu.cm/modules/article/search.php"
    s = requests.session()
    s.get(url="http://www.biqu.cm/modules/article/search.php")
    a = s.post(url=url,data=data,headers=headers,proxies=proxies, allow_redirects=False)
    if a.status_code == 302:
        url_back = a.headers['Location']
    elif a.status_code == 200:
        tree = html.fromstring(a.content.decode('gbk'))
        url_title = tree.xpath("//tr[@id='nr']/td[@class='odd']/a/text()")
        url_date = tree.xpath("//tr[@id='nr']/td[@class='odd']/a/@href")
        info = {url_title[x]:url_date[x] for x in range(len(url_title))}
        for key, value in info.items():
            if key == book:
                url_back = value
                break
    if not url_back:
        url_back =''
    return url_back

def run(url):
    global path,book_name,header,proxies,message
    a = requests.session()
    s = a.get(url,headers=header)
    tree = html.fromstring(s.text)
    url_date = tree.xpath("//dd/a/@href")
    url_title = change_to_GBK(tree.xpath("//dd/a/text()"))      ###
    print(s)
    page_title = sort_title(url_title,url_date)         ###去除无关的单章 并将汉字转为阿拉伯数字排序，可以兼容卷的问题
    for x in range(len(url_date)):
        if url_date[x] != -1:
            try:
                url = "http://www.biqu.cm"+url_date[x]
                page = page_title[x]
                deal(url,page)
            except:
                traceback.print_exc()
            # t = threading.Thread(target = deal,args=[url,page])
            # t.start()
            # time.sleep(0.1)

    time.sleep(5)
    print(merge_txt(path,book_name))     ###将分散的TXT单章合并
    sendmail4(path,book_name,message)
    print("已发送到邮箱")

def deal(url,page):
    global path,book_name,header,proxies
    s = requests.get(url,headers=header)
    tree = etree.HTML(s.text.encode('latin-1').decode('GBK'))
    title = tree.xpath("//h1/text()")
    message = tree.xpath("//div[@id='content']/text()")
    # print(message)
    print(len(message),url,title)
    message[0] ='\n'+message[0]         ###增加标题和正文的换行
    for y in range(len(message)):
        message[y] = message[y].replace(r"\xa0\xa0\xa0\xa0","")
    print("开始写入"+str(page)+"章"+title[0])
    with open('{0}/{1}/{2}.txt'.format(path,book_name,str(page)), 'w' ,encoding='utf-8') as f:
        f.write(title[0])
        for line in message:
            f.write(line)
    print("完成写入")



if __name__  == "__main__":
    url = "http://www.biqu.cm"+search(book_name)
    print(url)
    run(url)
    # sendmail4(path,book_name,message)