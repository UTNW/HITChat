# -*- coding:utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: spider.py
@time: 2017/10/30 8:50
@desc:
'''
import requests
import time
import random
from bs4 import BeautifulSoup
from MysqlConnecttencent import mysql
sql = mysql()
sql.delete('tencentnews')
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}
url = "http://news.qq.com/"

# 请求腾讯新闻的URL，获取其text文本
wbdata = requests.get(url,headers = header)

# 对获取到的文本进行解析
wbdata.encoding = 'gbk'
soup = BeautifulSoup(wbdata.text, 'html.parser')

# 从解析文件中通过select选择器定位指定的元素，返回一个列表
news_titles = soup.select("div.text > em.f14 > a.linkto")
count = 1
# 对返回的列表进行遍历
for n in news_titles:
    newslist = []
    nnews = []
    title = n.get_text()
    link = n.get("href")
    nnews.append(str(count))
    count += 1
    nnews.append(title)
    nnews.append(link)
    newslist.append(tuple(nnews))
    print(title)
    print link
    sql.insert('tencentnews', newslist)
    t1 = random.randint(1,3)
    print "休息%s秒"%t1
    time.sleep(t1)
sql.conn.close()
