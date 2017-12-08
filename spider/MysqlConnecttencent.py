# -*- coding: utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: Connect-mysql.py
@time: 2017/10/30 8:50
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
        self.cur.execute("create table IF NOT EXISTS tencentnews( id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,title VARCHAR(100) NOT NULL,titleurl VARCHAR(100) NOT NULL)") #腾讯新闻网新闻
        self.cur.close()
        self.conn.commit()
        #self.conn.close()

    def insert(self,table,valueduple):
        self.Cur()
        # 插入多条数据
        sql1 = "insert into "+table+" values(%s,%s,%s)"
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
    #修改查询条件的数据
    #cur.execute("update student set class='3 year 1 class' where name = 'Tom'")
    def delete(self, table):
        self.Cur()
        # 删除查询条件的数据
        self.cur.execute("delete from "+table)
        self.cur.close()
        self.conn.commit()

if __name__ == '__main__':
    sql = mysql()
    sql.createTables()
    sql.conn.close()
