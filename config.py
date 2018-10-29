configs = {
    "path":"D:/小说爬虫",       ####文件存储路径
    
    "book_name":"雪中悍刀行",     ###文件姓名

    "num":5,                      ##线程数

    "headers":{
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
},
    "headers_qula":{
    "Host": "sou.xanbhx.com",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
"Referer": "https://sou.xanbhx.com/search",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9"
    },

    "proxies":{                     ###代理IP
        "http":'http://127.0.0.1:1080'
        # "http":'http://59.67.152.230:3128'
    },

    "message":{                     ###邮件发送信息
        "toaddr" : "11111@qq.com",
        "fromaddr":"z550665885@163.com",
        "host":"smtp.163.com",
        "user":"11111@163.com",
        "pwd":"11111"
    }

}