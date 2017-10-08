# -*- coding: utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: config.py
@time: 2017/8/14 21:30
@desc:
'''
import os

HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'hitqa'
USERNAME = 'root'
PASSWORD = ''
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,
        HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True

SECRET_KEY = os.urandom(24)