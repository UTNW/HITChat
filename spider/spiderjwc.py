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
from multiprocessing import Pool
import random
from bs4 import BeautifulSoup
from MysqlConnectjwc import mysql

def spiderbottom():
    res = requests.get('http://jwc.hit.edu.cn/2591/list1.htm',headers = header)
    res.encoding = 'utf8'
    soup = BeautifulSoup(res.text,'html.parser')
    news = soup.select('.col_news_list')[0]
    span = news.select('#wp_paging_w6')[0].select('.page_jump')[0].select('.all_pages')[0].text
    return span

def spiderArtitle():
    res = requests.get(host+"list1.htm",headers = header)
    res.encoding = 'utf8'
    soup = BeautifulSoup(res.text,'html.parser')
    news = soup.select('.col_news_list')[0]
    s = news.select('#wp_news_w6')[0].select('li')
    for i in range(len(s)):
        jwc = []
        jwcArticle = []
        span = s[i]
        article = span.text
        articleurl = host1+span.select('.news_title')[0].select('a')[0]['href'] 
        print article,articleurl
        jwcArticle.append(article)
        jwcArticle.append(articleurl)
        try:
            res = requests.get(articleurl,headers = header)
            res.encoding = 'utf8'
            soup = BeautifulSoup(res.text,'html.parser')
            message = soup.select('.article')[0]
        except:
            try:
                url = articleurl.split('.')
                url[-1] = 'psp'
                articleurl = ''
                for i in range(len(url)-1):
                    articleurl += url[i]+"."
                articleurl += url[len(url)-1]
                res = requests.get(articleurl,headers = header)
                print host1+articleurl
                res.encoding = 'utf8'
                soup = BeautifulSoup(res.text,'html.parser')
                message = soup.select('.article')
            except:
                pass
            
        print message
        jwcArticle.append(message)
        jwc.append(tuple(jwcArticle))
        try:
            sql.insert('jwcArticle', jwc)
        except:
            print 'error!!!'
        t1 = random.randint(1,3)
        print "休息%s秒"%t1
        time.sleep(t1)

sql = mysql()  # 连接数据库，并初始化游标
host = 'http://jwc.hit.edu.cn/2591/'
host1 = 'http://jwc.hit.edu.cn'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}

if __name__ == "__main__":
    #num = spiderbottom()
    spiderArtitle()
