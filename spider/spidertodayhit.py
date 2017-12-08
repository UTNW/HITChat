# -*- coding: utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: todayhit.py
@time: 2017/11/8 20:28
@desc:
'''
import requests
import time
from multiprocessing import Pool
import random
from bs4 import BeautifulSoup
from mysqlconnectortodayhit import mysql
import sys
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
        sql.insert('slideleft', slideLeft)
    except:
        print 'error!!!'

def spiderArtitle(dataindex,data,SR):
    #slideRTitle = {}
    print "开始抓取 "+data[1]+" 文章标题..."
    res = requests.get(data[2],headers = header)
    res.encoding = 'gbk'
    soup = BeautifulSoup(res.text, 'html.parser')

    detailtitle = soup.select('.sidelist7')[0]
    Dt = detailtitle.select('li')
    slideRight = []
    for j in range(len(Dt)):
        # time = detailtitle.select('li')[0].text
        slideR = []
        
        sourcename = detailtitle.select('li')[j].select('.red')[0].text
        sourceurl = host+detailtitle.select('li')[j].select('a')[0]['href']
        title2 = detailtitle.select('li')[j].select('a')[1].text
        title2url = host+detailtitle.select('li')[j].select('a')[1]['href']
        #slideRTitle[title2] = title2url
        slideR.append(str(j+1))
        slideR.append(title2)
        slideR.append(title2url)
        slideR.append(sourcename)
        slideR.append(sourceurl)
        slideR.append(str(data[0]))
        slideRight.append(tuple(slideR))
        # print sourcename,sourceurl,title2,title2url
    try:
        sql.insert('slideright'+str(data[0]), slideRight)
    except:
        print 'error!!!'
    # t1 = random.randint(1,5)
    # print "休息%s秒"%t1
    # time.sleep(t1)
    flag = True
    print "开始抓取 "+data[1]+" 详细文章："
    # keys1 = slideRTitle.keys()
    # values1 = slideRTitle.values()
    dataDetail = sql.select('slideright'+str(data[0]))
    slideRightDetail1 = []
    slideRightDetail2 = []
    maxid = sql.selectmaxid('sliderightdetail'+str(data[0]))
    for k in range(len(dataDetail)):
        k1 = (maxid+k)

        slideRDetail2 = []
        res = requests.get(dataDetail[k][2],headers = header)
        res.encoding = 'gbk'
        soup = BeautifulSoup(res.text,'html.parser')
        if dataDetail[k][2] == SR[dataindex]:
            flag = False
        try:
            title = soup.select('.articleTitle')[0].text
            Time = soup.select('#date')[0].text
            print dataDetail[k][2]
            print SR[dataindex]
            print flag
            if flag and (dataDetail[k][2] != SR[dataindex]):
                news = soup.select('.articletext')[0].text
                slideRightDetail1 = []
                slideRDetail1 = []
                slideRDetail1.append(str(k1+1))
                slideRDetail1.append(title)
                slideRDetail1.append(Time[:24])
                slideRDetail1.append(news)
                slideRDetail1.append(dataDetail[k][2])
                slideRightDetail1.append(tuple(slideRDetail1))
                sql.insert('sliderightdetail'+str(data[0]), slideRightDetail1)
            else:
                flag = False
                pass
            news = soup.select('.articletext')[0]
            l = news.select('p')
            for i in range(len(l)):
                tag1 = l[i].img
                tag2 = l[i].a
                try:
                    pre1 = tag1['src']
                    tag1['src'] = "http://today.hit.edu.cn"+pre1
                except:
                    pass
                try:
                    pre2 = tag2['href']
                    tag2['href'] = "http://today.hit.edu.cn"+pre2
                except:
                    pass
            l = news.select('div')
            for i in range(len(l)):
                tag1 = l[i].img
                tag2 = l[i].a
                try:
                    pre1 = tag1['src']
                    tag1['src'] = "http://today.hit.edu.cn"+pre1
                except:
                    pass
                try:
                    pre2 = tag2['href']
                    tag2['href'] = "http://today.hit.edu.cn"+pre2
                except:
                    pass
            slideRDetail2.append(str(k+1))
            slideRDetail2.append(title)
            slideRDetail2.append(Time[:24])
            slideRDetail2.append(news)
            slideRDetail2.append(dataDetail[k][2])
            slideRightDetail2.append(tuple(slideRDetail2))
            #print Time[:24],title,news
        except:
            pass
        t2 = random.randint(1,3)
        print "休息%s秒"%t2
        time.sleep(t2)
    try:
        sql.insert('sliderightdetailhtml'+str(data[0]), slideRightDetail2)
    except:
        print 'error!!!'

host = 'http://today.hit.edu.cn'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}
if __name__ == "__main__":
    # print "正在抓取今日哈工大左侧页面链接..."
    # spiderLeft()
    # print "抓取结束，开始抓取右侧文章..."
    #flag = sys.argv[1] # 参数为1 代表爬取text，为2代表爬取html
    Star = True
    SR = []
    while Star:
        sql = mysql()  # 连接数据库，并初始化游标
        for i in range(15):
            biaoshi = sql.select('slideright'+str(i+1))
            if biaoshi:
                SR.insert(i,biaoshi[0][2])
                print biaoshi[0][2]
                time.sleep(30)
            else:
                SR.insert(i,0)
            sql.delete('slideright'+str(i+1))
            sql.delete('sliderightdetailhtml' + str(i+1))
        # t1 = time.clock()
        # dataSql = sql.select('slideLeft')
        # # print dataSql[0]
        # pool = Pool(15)
        # print len(dataSql)
        # pool.map(spiderArtitle, dataSql)
        # pool.close()
        # t2 = time.clock()
        # print "所用时间为%s"%(t2-t1)
        # time.sleep(14400)
        t1 = time.clock()
        dataSql = sql.select('slideleft')
        for i in range(15):
            spiderArtitle(i,dataSql[i],SR)
        t2 = time.clock()
        print "所用时间为%s"%(t2-t1)
        sql.conn.close()
        print "正在休息(%s开始休息),预计休息12小时"%(time.ctime())
        Star = False
        #time.sleep(43200)
        '''for i in range(15):
            sql.delete('slideRight'+str(i+1))
            sql.delete('slideRightDetail' + str(i+1))'''
