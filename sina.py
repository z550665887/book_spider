import requests
from lxml import html
from lxml import etree
url  = "https://s.weibo.com/top/summary?cate=realtimehot"
headers  =  {

"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",

}
s = requests.session()
# print(url)
a = s.get(url=url,headers=headers)
# print(a.text)
tree = html.fromstring(a.content.decode())
url_title = tree.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[@class='td-02']/a/text()")[1:]
url_link = tree.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[@class='td-02']/a/@href")[1:]
url_span = tree.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[@class='td-02']/span/text()")
url_type = tree.xpath("//div[@id='pl_top_realtimehot']/table/tbody/tr/td[@class='td-03']/i/text()")[1:]
# print(url_title)
# print(url_link)
# print(url_span)
# print(url_type)
url = "https://s.weibo.com/weibo?q=%23%E8%B5%B5%E4%B8%BD%E9%A2%96%E6%96%B0%E5%89%A7%23&Refer=top"
a = s.get(url=url, headers=headers)
print(a.text)