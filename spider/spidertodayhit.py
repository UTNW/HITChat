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
from MysqlConnect import mysql

def spiderLeft():
    res = requests.get('http://today.hit.edu.cn/classList/1.html',headers = header)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res.text,'html.parser')
    # for news in soup.select('.sidelist6'):
    #     span = news.select('span')
    #     a = news.select('a')
    #     for i in range(len(span)):
    #         title1 = span[i].text
    #         title1url = host+a[i]['href']
    #         print title1,title1url
    #         detailtitle = soup.select('.sidelist7')[0]
    #         Dt = detailtitle.select('li')
    #         for j in range(len(Dt)):
    #             # time = detailtitle.select('li')[0].text
    #             sourcename = detailtitle.select('li')[j].select('.red')[0].text
    #             sourceurl = host+detailtitle.select('li')[j].select('a')[0]['href']
    #             title2 = detailtitle.select('li')[j].select('a')[1].text
    #             title2url = host+detailtitle.select('li')[j].select('a')[1]['href']
    #             print sourcename,sourceurl,title2,title2url
    #***************今日哈工大左侧栏标题与连接存储到数据库中的一张表中***********************
    news = soup.select('.sidelist6')[0]
    span = news.select('span')
    a = news.select('a')
    slideLeft = []
    slidenew = []
    slidenew.append(str(1))
    title1 = '最新消息'
    slidenew.append(title1)
    title1url = 'http://today.hit.edu.cn/classList/1.html'
    slidenew.append(title1url)
    slideLeft.append(tuple(slidenew))
    for i in range(len(span)):
        slideL = []
        slideL.append(str(i+2))
        title1 = span[i].text
        slideL.append(title1)
        title1url = host+a[i]['href']
        slideL.append(title1url)
        slideLeft.append(tuple(slideL))
        print title1,title1url

    try:
        sql.insert('slideLeft', slideLeft)
    except:
        print 'error!!!'

def spiderArtitle(data):
    slideRTitle = {}
    res = requests.get(data[2],headers = header)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res.text, 'html.parser')
    
    detailtitle = soup.select('.sidelist7')[0]
    Dt = detailtitle.select('li')
    slideRight = []
    for j in range(len(Dt)):
        # time = detailtitle.select('li')[0].text
        slideR = []
        slideR.append(str(j+1))
        sourcename = detailtitle.select('li')[j].select('.red')[0].text
        sourceurl = host+detailtitle.select('li')[j].select('a')[0]['href']
        title2 = detailtitle.select('li')[j].select('a')[1].text
        title2url = host+detailtitle.select('li')[j].select('a')[1]['href']
        slideRTitle[title2] = title2url
        slideR.append(title2)
        slideR.append(title2url)
        slideR.append(sourcename)
        slideR.append(sourceurl)
        slideR.append(str(data[0]))
        slideRight.append(tuple(slideR))
        # print sourcename,sourceurl,title2,title2url
    try:
        sql.insert('slideRight'+str(data[0]), slideRight)
    except:
        print 'error!!!'
    # t1 = random.randint(1,5)
    # print "休息%s秒"%t1
    # time.sleep(t1)

    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    # keys1 = slideRTitle.keys()
    # values1 = slideRTitle.values()
    dataDetail = sql.select('slideRight'+str(data[0]))
    #print dataDetail
    #sleep(14400)
    slideRightDetail = []
    for k in range(len(dataDetail)):
        slideRDetail = []
        slideRDetail.append(str(k+1))
        res = requests.get(dataDetail[k][2],headers = header)
        res.encoding = 'gbk'
        soup = BeautifulSoup(res.text,'html.parser')
        try:
            title = soup.select('.articleTitle')[0].text
            Time = soup.select('#date')[0].text
            news = soup.select('.articletext')[0].text
            slideRDetail.append(title)
            slideRDetail.append(Time[:24])
            slideRDetail.append(news)
            slideRDetail.append(dataDetail[k][2])
            slideRightDetail.append(tuple(slideRDetail))
            print Time[:24],title,news
        except:
            pass
        t2 = random.randint(1,3)
        print "休息%s秒"%t2
        time.sleep(t2)
    try:
        sql.insert('slideRightDetail'+str(data[0]), slideRightDetail)
    except:
        print 'error!!!'

sql = mysql()  # 连接数据库，并初始化游标
host = 'http://today.hit.edu.cn'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}
if __name__ == "__main__":
    # print "正在抓取今日哈工大左侧页面链接..."
    # spiderLeft()
    # print "抓取结束，开始抓取右侧文章..."
    while True:
        for i in range(15):
            sql.delete('slideRight'+str(i+1))
            sql.delete('slideRightDetail' + str(i+1))
        #t1 = time.clock()
        #dataSql = sql.select('slideLeft')
        # print dataSql[0]
        #pool = Pool(15)
        #print len(dataSql)
        #pool.map(spiderArtitle, dataSql)
        #pool.close()
        #t2 = time.clock()
        #print "所用时间为%s"%(t2-t1)
        #time.sleep(14400)

        t1 = time.clock()
        dataSql = sql.select('slideLeft')
        for i in range(15):
            spiderArtitle(dataSql[i])
        # print dataSql[0]
        # pool = Pool(15)
        # print len(dataSql)
        # pool.map(spiderArtitle, dataSql)
        # pool.close()
        t2 = time.clock()
        print "所用时间为%s"%(t2-t1)
        time.sleep(14400)

