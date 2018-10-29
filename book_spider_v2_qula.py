import requests
from lxml import html
from lxml import etree
from chinese_to_int import *
from send_to_qq import sendmail4
import re
import threading
import time
from config import configs
from urllib import parse

path = configs['path']    ###文件路径
book_name = configs['book_name']     ###文件姓名
num = configs['num'] ##线程数
headers  = configs['headers_qula']
proxies = configs['proxies']
message = configs['message']        ###邮件发送配置

def search(book_name):
    # book_name = parse.quote(book_name, encoding='gbk')
    print(book_name)
    url  = "https://sou.xanbhx.com/search?siteid=qula&q={0}".format(book_name)
    s = requests.session()
    print(url)
    a = s.get(url=url,headers=headers,proxies=proxies)
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
    s = requests.get(url=url,proxies = proxies)
    tree = html.fromstring(s.text)
    url_date = tree.xpath("//dd/a/@href")
    # print(s.content)
    url_date = [x for x in url_date if '/book/' in x]
    print(url_date)
    for x in range(len(url_date)):
        if url_date[x] != -1:
            urls = "https://www.qu.la/"+url_date[x]
            # page = page_title[x]
            try:
                pass
                deal(urls)
            except:
                traceback.print_exc()
        # if x % num == 0:
        #     time.sleep(0.1)
    time.sleep(5)
    # print(merge_txt(path,book_name))     ###将分散的TXT单章合并
    sendmail4(path,book_name,message)
    print("已发送到邮箱")

def deal(url):
    global path,book_name,headers,proxies
    s = requests.get(url,proxies = proxies)
    tree = etree.HTML(s.content)
    title = tree.xpath("//div[@class='bookname']/h1/text()")
    message = tree.xpath("//div[@id='content']/text()")
    # print(message)
    # print(title, message)
    message[0] ='\n'+message[0]         ###增加标题和正文的换行
    for y in range(len(message)):
        message[y] = message[y].replace("\xa0\xa0\xa0\xa0","").replace("\u3000",'\n')
    print("开始写入"+title[0])
    with open('{0}/{1}/{2}.txt'.format(path,book_name,book_name), 'a' ,encoding='utf-8') as f:
        f.write(title[0])
        for line in message:
            f.write(line)
        f.write('\r\n')
    print("完成写入")



if __name__  == "__main__":
    url = search(book_name)
    # url = "http://www.biqu.cm/7_7067/"
    print(url)
    run(url)