# -*- coding: utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: mysqlconnector.py
@time: 2017/11/8 20:23
@desc:
'''
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
        self.cur.execute("create table IF NOT EXISTS slideleft( id INT UNSIGNED PRIMARY KEY,title VARCHAR(100) NOT NULL,titleurl VARCHAR(100) NOT NULL)") #左侧链接
        for i in range(15): #右侧文章链接
            self.cur.execute("create table IF NOT EXISTS slideright" + str(i + 1) + "( id INT UNSIGNED PRIMARY KEY,title VARCHAR(100) NOT NULL,titleurl VARCHAR(100) NOT NULL,source VARCHAR(100) NOT NULL,sourceurl VARCHAR(100) NOT NULL,titleleft VARCHAR(100) NOT NULL)")
        for i in range(15): #具体文章
            self.cur.execute("create table IF NOT EXISTS sliderightdetail" + str(i + 1) + "( id INT UNSIGNED PRIMARY KEY,title VARCHAR(100) NOT NULL,time VARCHAR(100) NOT NULL,news MEDIUMTEXT NOT NULL,newsurl VARCHAR(100) NOT NULL)")
        self.cur.close()
        self.conn.commit()
        #self.conn.close()

    def createTableshtml(self):
        self.Cur()
        # 创建数据表
        #self.cur.execute("create table IF NOT EXISTS slideleft( id INT UNSIGNED PRIMARY KEY,title VARCHAR(100) NOT NULL,titleurl VARCHAR(100) NOT NULL)") #左侧链接
        #for i in range(15): #右侧文章链接
            #self.cur.execute("create table IF NOT EXISTS slideright" + str(i + 1) + "( id INT UNSIGNED PRIMARY KEY,title VARCHAR(100) NOT NULL,titleurl VARCHAR(100) NOT NULL,source VARCHAR(100) NOT NULL,sourceurl VARCHAR(100) NOT NULL,titleleft VARCHAR(100) NOT NULL)")
        for i in range(15): #具体文章
            self.cur.execute("create table IF NOT EXISTS sliderightdetailhtml" + str(i + 1) + "( id INT UNSIGNED PRIMARY KEY,title VARCHAR(100) NOT NULL,time VARCHAR(100) NOT NULL,news MEDIUMTEXT NOT NULL,newsurl VARCHAR(100) NOT NULL)")
        self.cur.close()
        self.conn.commit()
        #self.conn.close()

    def insert(self,table,valueduple):
        self.Cur()
        # 插入多条数据
        if len(valueduple[0]) == 3:
            sql1 = "insert into "+table+" values(%s,%s,%s)"
        elif len(valueduple[0]) == 5:
            sql1 = "insert into "+table+" values(%s,%s,%s,%s,%s)"
        else:
            sql1 = "insert into "+table+" values(%s,%s,%s,%s,%s,%s)"
        #print valueduple
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

    def selectTop10(self, table):
        self.Cur()
        aa = self.cur.execute("select * from "+table+" where id <= 10")
        # 获取表中的所有数据
        info = self.cur.fetchmany(aa)

        self.cur.close()
        self.conn.commit()
        # self.conn.close()
        return info

    def selectnews(self, table,id):
        self.Cur()
        aa = self.cur.execute("select * from " + table+" where id = "+id)
        # 获取表中的所有数据
        info = self.cur.fetchmany(aa)

        self.cur.close()
        self.conn.commit()
        # self.conn.close()
        return info
    def selectmaxid(self, table):
        self.Cur()
        #print table
        s = self.cur.execute("select * from " + table)
        info = self.cur.fetchmany(s)
        self.cur.close()
        self.conn.commit()
        try:
            return info[s-1][0]
        except:
            return 0
        
    def delete(self, table):
        self.Cur()
        # 删除查询条件的数据
        self.cur.execute("delete from "+table)
        self.cur.close()
        self.conn.commit()

if __name__ == '__main__':
    sql = mysql()
    #sql.createTables()
    sql.createTableshtml()
