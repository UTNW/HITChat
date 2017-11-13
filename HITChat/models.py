# -*- coding: utf-8 -*-
'''
@author: xinghuazhang
@license: (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
@contact: xing_hua_zhang@126.com
@software: PyCharm 2017.1.4
@file: models.py
@time: 2017/8/14 21:40
@desc:
'''
from exts import db
from datetime import datetime
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    salt = db.Column(db.String(50), nullable=False)

    realname = db.Column(db.String(50), nullable=True,default='未知')
    gender = db.Column(db.String(6), nullable=True,default='未知')
    birthyear = db.Column(db.String(6), nullable=True,default='未知')
    birthmonth = db.Column(db.String(6), nullable=True,default='未知')
    birthday = db.Column(db.String(6), nullable=True,default='未知')
    institude = db.Column(db.String(50), nullable=True,default='未知')
    contactway = db.Column(db.String(50), nullable=True,default='未知')
    motto = db.Column(db.String(100), nullable=True,default='未知')
    hobby = db.Column(db.String(100), nullable=True,default='未知')
    birthplace = db.Column(db.String(100), nullable=True,default='未知')
    liveplace = db.Column(db.String(100), nullable=True,default='未知')
    education = db.Column(db.String(20), nullable=True,default='未知')
    resume = db.Column(db.String(100), nullable=True,default='未知')
    picid = db.Column(db.Integer, default=0)
    isAdmin = db.Column(db.Integer, default=0)

class Question(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    label = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text,nullable=True)
    zan = db.Column(db.Integer, nullable=True, default=0)
    create_time = db.Column(db.DateTime,default=datetime.now)
    #now()获取的是服务器第一次运行的时间
    #now是每次创建一个模型时获取的当前时间
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref=db.backref('questions'))

class Answer(db.Model):
    __tablename__='answer'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.relationship('Question',backref=db.backref('answers',order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))

class Answer2(db.Model):
    __tablename__='answer2'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    answer_id = db.Column(db.Integer,db.ForeignKey('answer.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer = db.relationship('Answer',backref=db.backref('answers2',order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers2'))

class YX_Aiml(db.Model):
    __tablename__='yx_aiml'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content_p = db.Column(db.Text,nullable=True)
    content_r = db.Column(db.Text, nullable=True)

class Top(db.Model):
    __tablename__='top'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)

