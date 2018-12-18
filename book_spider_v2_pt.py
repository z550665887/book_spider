import requests
from lxml import html
from lxml import etree
from chinese_to_int import *
from send_to_qq import sendmail4
import re
import threading
import time
import sys
from config import configs
from urllib import parse

path = configs['path']    ###文件路径
book_name = configs['book_name']     ###文件姓名
num = configs['num'] ##线程数
headers  = configs['headers_pt']
proxies = configs['proxies']
message = configs['message']        ###邮件发送配置

def search(book_name):
    # book_name = parse.quote(book_name, encoding='gbk')
    print(book_name)
    url  = "https://www.piaotian.com/modules/article/search.php"
    s = requests.session()
    print(url)
    bookname = parse.quote(book_name, encoding='gbk')
    data = "searchtype=articlename&searchkey={0}&action=login".format(bookname)
    a = s.post(url=url,headers=headers, data=data, allow_redirects=False)
    url_back = ""
    if a.status_code == 302:
        url_back = a.headers['Location']
    elif a.status_code == 200:
        tree = html.fromstring(a.content.decode('gbk'))
        url_title = tree.xpath("//tr/td[@class='odd']/a/text()")
        url_date = tree.xpath("//tr/td[@class='odd']/a/@href")
        print(url_title, url_date)
        info = {url_title[x].replace("\r\n","").strip():url_date[x] for x in range(len(url_title))}
        print(info)
        for key, value in info.items():
            if key == book_name:
                url_back = value
                break
    else:
        print("search为空")
        sys.exit(0)
    if not url_back:
        url_back =''
    return url_back

def run(url):
    global path,book_name,headers,proxies,message
    if not os.path.exists(path+"/"+book_name):
        os.mkdir(path+"/"+book_name)
    url = url.replace("bookinfo", "html")[:-5]
    s = requests.get(url=url)
    tree = html.fromstring(s.text)
    url_date = tree.xpath("//div[@class='centent']/ul/li/a/@href")
    # print(url_date)
    url_date = [x for x in url_date if re.search("html$", x)]
    # print(url_date)
    for x in range(len(url_date)):
        if url_date[x] != -1:
            urls = url+ '/' +url_date[x]
            # page = page_title[x]
            try:
                pass
                threading.Thread(target=deal, args=[urls, x])
                # deal(urls,x)
                time.sleep(0.5)
            except:
                traceback.print_exc()
        # if x % num == 0:
        #     time.sleep(0.1)
    time.sleep(5)
    print(merge_txt(path,book_name))     ###将分散的TXT单章合并
    sendmail4(path,book_name,message)
    print("已发送到邮箱")

def deal(url,x):
    global path,book_name,headers,proxies
    s = requests.get(url)
    tree = etree.HTML(s.text)
    # print(s.text)
    title = tree.xpath("//h1/text()")
    message = tree.xpath("//body/text()")
    # print(title)
    message[0] ='\n'+message[0]         ###增加标题和正文的换行
    for y in range(len(message)):
        message[y] = message[y].replace("\xa0\xa0\xa0\xa0","").replace("\u3000",'\n')
    print("开始写入"+title[0])
    with open('{0}/{1}/{2}.txt'.format(path,book_name,x), 'a' ,encoding='utf-8') as f:
        f.write(title[0])
        for line in message:
            f.write(line)
        f.write('\r\n')
    print("完成写入")



if __name__  == "__main__":
    url = search(book_name)
    # url = "https://www.qu.la/book/398"
    print(url)
    run(url)