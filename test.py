import requests
from urllib import parse
from lxml import html
from lxml import etree
headers = {
    # POST /modules/article/search.php HTTP/1.1
"Host": "www.biqu.cm",
"Connection": "keep-alive",
"Content-Length": "144",
"Cache-Control": "max-age=0",
"Origin": "http://www.biqu.cm",
"Upgrade-Insecure-Requests": "1",
"Content-Type": "application/x-www-form-urlencoded",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Referer": "http://www.biqu.cm/modules/article/search.php",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "zh-CN,zh;q=0.9",
}
book = "大王饶命"
book_name = parse.quote(book, encoding='gbk')
print(book_name)
data ="searchtype=articlename&searchkey={0}&action=login&submit=%26%23160%3B%CB%D1%26%23160%3B%26%23160%3B%CB%F7%26%23160%3B".format(book_name)
url  = "http://www.biqu.cm/modules/article/search.php"
s = requests.session()
proxies={                     ###代理IP
        # "http":'http://59.67.152.230:3128'
        # "http":'http://50.205.36.168:8080'
        "http":"127.0.0.1:1080"
    }
s.get(url="http://www.biqu.cm/modules/article/search.php")
a = s.post(url=url,data=data,headers=headers,proxies=proxies, allow_redirects=False)
# print(a.content.decode('gbk'))
# print(a.content)
if a.status_code == 302:
    print(dir(a))
    print(a.history)
    print(a.headers['Location'])
elif a.status_code == 200:
    tree = html.fromstring(a.content.decode('gbk'))
    url_title = tree.xpath("//tr[@id='nr']/td[@class='odd']/a/text()")
    url_date = tree.xpath("//tr[@id='nr']/td[@class='odd']/a/@href")
    info = {url_title[x]:url_date[x] for x in range(len(url_title))}
    for key, value in info.items():
        if key == book:
            print (value)
    print(url_title, url_date)
# print(a.headers['Location'])
# print(a.headers)
# import json
# m=json.dumps({"id":5,"dd":"dsf"})
# print(type(json.dumps({"id":5,"dd":"dsf"})))
# a="q=stringify&oq=stringify&aqs=chrome..69i57j0l5.7305j0j7&sourceid=chrome&ie=UTF-8"
# print(json.loads(m))
# print(json.loads(a))

