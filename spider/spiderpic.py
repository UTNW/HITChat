# -*- coding: utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: spiderpic.py
@time: 2017/11/6 9:39
@desc:
'''
import requests
from bs4 import BeautifulSoup
import os

def getHtmlurl(url):         #获取网址
    try:
       r=requests.get(url)
       r.raise_for_status()
       r.encoding='gbk'
       print r.text
       return r.text
    except:
        return ""

def getpic(html): #获取图片地址并下载
    soup=BeautifulSoup(html,'html.parser')
    all_img=soup.find_all('img')
    all_file=soup.find_all('a')

    for img in all_img:
       src=img['src']
       img_url="http://today.hit.edu.cn/"+src
       print (img_url)
       root='D:/pic/'
       picname=img_url.split('/')[-1]
       if picname=='hui.jpg'or picname=='ic.gif':
           continue
       path=root + picname
       try:                              #创建或判断路径图片是否存在并下载
           if not os.path.exists(root):
               os.mkdir(root)
           if not os.path.exists(path):
               r=requests.get(img_url)
               with open(path, 'wb') as f:
                   f.write(r.content)
                   f.close()
                   print("文件保存成功")
           else:
               print("文件已存在")
       except:
           print("爬取失败")
    for file in all_file:
        src=file['href']
        if not 'uploadfiles' in src:
            continue
        file_url="http://today.hit.edu.cn/"+src
        print (file_url)
        root='D:/pic/'
        filename=file_url.split('/')[-1]
        path=root + filename
        try:                              #创建或判断路径图片是否存在并下载
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(path):
                r=requests.get(file_url)
                with open(path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                    print("文件保存成功")
            else:
                print("文件已存在")
        except:
            print("爬取失败")

def main():
    url='http://today.hit.edu.cn/news/2017/11-06/6841320111RL1.htm'
    html=(getHtmlurl(url))
    print(getpic(html))
main()