import requests
from lxml import html
from lxml import etree
from chinese_to_int import *
from send_to_qq import sendmail4
import re
import threading
import time
import copy
from config import configs
from urllib import parse

path = configs['path']    ###文件路径
book_name = configs['book_name']     ###文件姓名
num = configs['num'] ##线程数
headers  = configs['headers_52hk']
proxies = configs['proxies']
message = configs['message']        ###邮件发送配置
error_list = []

def search(book_name):
    book_name = parse.quote(book_name, encoding='gbk')
    data = "searchtype=articlename&searchkey={0}&action=login&submit=%26%23160%3B%CB%D1%26%23160%3B%26%23160%3B%CB%F7%26%23160%3B".format(book_name)
    url  = "https://www.52k.hk/modules/article/search.php"
    s = requests.session()
    s.get(url="https://www.52k.hk/modules/article/search.php")
    a = s.post(url=url,data=data,headers=headers,proxies=proxies, allow_redirects=False)
    url_back = ""
    print(a.text)
    if a.status_code == 302:
        url_back = a.headers['Location']
    elif a.status_code == 200:
        tree = html.fromstring(a.content.decode())
        url_title = tree.xpath("//span[@class='s2']/a/text()")
        url_date = tree.xpath("//span[@class='s2']/a/@href")
        info = {url_title[x].replace("\r\n","").strip():url_date[x] for x in range(len(url_title))}
        print(info)
        for key, value in info.items():
            if key == book_name:
                url_back = value
                break
    if not url_back:
        url_back =''
    return url_back

def run(url):
    global path,book_name,headers,proxies,message
    if not os.path.exists(path+"/"+book_name):
        os.mkdir(path+"/"+book_name)
    print(url)
    url = "https://www.52k.hk/modules/article/txtarticle.php?id={0}".format(url.split("/")[-1].replace(".html",""))
    print(url)
    a = requests.get(url=url)
    if a.status_code == 200:
        with open('{0}/{1}/{2}.txt'.format(path,book_name,book_name), 'w' ,encoding='utf-8') as f:
            f.write(a.content.decode('gbk'))
    sendmail4(path,book_name,message)
    print("已发送到邮箱")



if __name__  == "__main__":
    url = search(book_name)
    # url = "https://www.qu.la/book/398"
    print(url)
    run(url)