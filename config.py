configs = {
    "path":"D:/小说爬虫",       ####文件存储路径
    
    "book_name":"修真聊天群",     ###文件姓名

    "num":20,                      ##线程数

    "header":{                      ###模拟浏览器头
        "Host" :"www.biqu.cm",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"  
    },

    "proxies":{                     ###代理IP
        "http":'http://58.16.42.112:80'
    }

    "message":{                     ###邮件发送信息
        "toaddr" : "xxxxxxx@qq.com",
        "fromaddr":"xxxxxx@126.com",
        "host":"smtp.126.com",
        "user":"xxxxx",
        "pwd":"xxxxxxx"
    }
}