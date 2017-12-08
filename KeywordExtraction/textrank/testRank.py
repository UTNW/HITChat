#-*- encoding:utf-8 -*-
import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import codecs
from textrank4zh import TextRank4Keyword
import MySQLdb

class mysql:
    def __init__(self):
        self.conn= MySQLdb.connect(
                host = '127.0.0.1',
                port = 3306,
                user = 'root',
                passwd = 'password',
                db = 'HITChat',
                )
        self.conn.set_character_set('utf8')

    def Cur(self):
        self.cur = self.conn.cursor()
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')

    def createTables(self):
        self.Cur()
        # 创建数据表
        self.cur.execute(
            "create table IF NOT EXISTS keyword( id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,title VARCHAR(100) NOT NULL,url VARCHAR(100) NOT NULL,key1 VARCHAR(50),key2 VARCHAR(50),key3 VARCHAR(50),key4 VARCHAR(50),key5 VARCHAR(50))")
        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def insert(self,table,valueduple):
        self.Cur()
        sql1 = "insert into "+table+"(title,url,key1,key2,key3,key4,key5) values(%s,%s,%s,%s,%s,%s,%s)"
        print valueduple
        self.cur.executemany(sql1,valueduple)
        self.cur.close()
        self.conn.commit()
        # self.conn.close()

    def select(self, table):
        self.Cur()
        aa = self.cur.execute("select * from "+table)
        # 获取表中的所有数据
        info = self.cur.fetchmany(aa)
        self.cur.close()
        self.conn.commit()
        # self.conn.close()
        return info
     
    def selectold(self,table,url):
        self.Cur()
        print url
        sql1 = "SELECT * FROM "+ table+" WHERE title = '%s'"%(url)
        aa = self.cur.execute(sql1)
        #获取所有记录列表
        results = self.cur.fetchall()
        self.cur.close()
        self.conn.commit()
        return results

    #修改查询条件的数据
    def delete(self, table):
        self.Cur()
        # 删除查询条件的数据
        self.cur.execute("delete from "+table)
        self.cur.close()
        self.conn.commit()

class articleKey:
    def generator(self,text):
        tr4w = TextRank4Keyword(stop_words_file='./stopword.txt')  # 导入停止词
        #使用词性过滤，文本小，窗口为3
        tr4w.train(text=text, speech_tag_filter=False, lower=True, window=3)
        key = []
        for word in tr4w.get_keywords(10, word_min_len=2):
            key.append(word)
        return key
        
if __name__ == '__main__':
    sql = mysql()
    #sql.createTables()
    #text = codecs.open('./text/05.txt', 'r', 'utf-8').read()
    tr4w = TextRank4Keyword(stop_words_file='./stopword.txt')  # 导入停止词
    for i in range(15):
        keyword = []
        data = sql.select('sliderightdetail' + str(i+1))
        for j in range(len(data)):
            key = []
            if sql.selectold('keyword',data[j][1]):
                continue
            text = data[j][3]+data[j][1]
            key.append(data[j][1])
            key.append(data[j][4])
            #使用词性过滤，文本小，窗口为3
            tr4w.train(text=text, speech_tag_filter=False, lower=True, window=3)

            #print '关键词：'
            # 10个关键词且每个的长度最小为2
            for word in tr4w.get_keywords(5, word_min_len=2):
                key.append(word)
            for k in range(7-len(key)):
                key.append('')
            keyword.append(tuple(key))
        try:
            sql.insert('keyword',keyword)
        except:
            print "error!!!"
    sql.conn.close()
